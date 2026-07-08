import os
from datetime import datetime, timezone
from urllib.parse import unquote
import hashlib

import functions_framework
from google.cloud import storage


@functions_framework.cloud_event
def process_uploaded_file(cloud_event):
    data = cloud_event.data

    print("Received event data:")
    print(data)

    bucket_name = None
    file_name = None
    file_size = "unknown"
    content_type = "unknown"
    time_created = "unknown"

    report_bucket_name = os.environ.get("REPORT_BUCKET")

    if not report_bucket_name:
        raise ValueError("REPORT_BUCKET environment variable is not set")

    # Case 1: Direct Cloud Storage finalized event format
    if "bucket" in data and "name" in data:
        bucket_name = data.get("bucket")
        file_name = data.get("name")
        file_size = data.get("size", "unknown")
        content_type = data.get("contentType", "unknown")
        time_created = data.get("timeCreated", "unknown")

    # Case 2: Audit Log format: storage.objects.create
    elif "protoPayload" in data:
        proto_payload = data.get("protoPayload", {})
        resource_name = proto_payload.get("resourceName", "")

        print(f"Audit log resourceName: {resource_name}")

        if "/buckets/" in resource_name and "/objects/" in resource_name:
            bucket_part = resource_name.split("/buckets/")[1]
            bucket_name = bucket_part.split("/objects/")[0]

            object_part = resource_name.split("/objects/")[1]
            file_name = unquote(object_part)

        time_created = data.get("timestamp", "unknown")

    if not bucket_name or not file_name:
        print("Could not find bucket name or file name. Stopping function.")
        return

    print(f"Bucket Name: {bucket_name}")
    print(f"File Name: {file_name}")

    # Safety 1: ignore report bucket events
    if bucket_name == report_bucket_name:
        print("Ignoring event from report bucket to avoid recursive trigger.")
        return

    # Safety 2: ignore already generated report files
    if (
        file_name.startswith("reports/")
        or file_name.startswith("reports_")
        or file_name.endswith("-report.txt")
        or "-report.txt" in file_name
    ):
        print("Ignoring generated report file to avoid duplicate loop.")
        return

    report_content = f"""
Cloud Storage File Processing Report

File Name: {file_name}
Source Bucket: {bucket_name}
File Size: {file_size} bytes
Content Type: {content_type}
File Created Time: {time_created}
Function Processed Time: {datetime.now(timezone.utc).isoformat()}

Event Type: File uploaded to Cloud Storage
Status: File received and processed successfully
"""

    storage_client = storage.Client()
    report_bucket = storage_client.bucket(report_bucket_name)

    # Short safe report name
    safe_file_name = file_name.replace("/", "_")
    short_hash = hashlib.md5(file_name.encode()).hexdigest()[:8]

    if len(safe_file_name) > 100:
        safe_file_name = safe_file_name[:100]

    report_file_name = f"reports/{safe_file_name}-{short_hash}-report.txt"

    report_blob = report_bucket.blob(report_file_name)
    report_blob.upload_from_string(report_content)

    print(f"Report created: gs://{report_bucket_name}/{report_file_name}")
