This is event based 



create two buckdets


one is for file incoming




one is for processing



If any file upload to incoming bucket then automatically it will process in another bucket using cloud fucntion..



env variables:




REPORT_BUCKET: processed bucekt





sample for git purpose


| Your requirement                                                    | Recommended class        | Reason                                                         |
| ------------------------------------------------------------------- | ------------------------ | -------------------------------------------------------------- |
| Customers regularly download files from your application            | **Standard**             | No retrieval fee and no minimum duration                       |
| Application frequently reads configuration or media files           | **Standard**             | Designed for active application data                           |
| Store daily backups but restore approximately once a month          | **Nearline**             | Lower storage price with a 30-day commitment                   |
| Store monthly backups and restore only during major incidents       | **Coldline**             | Suitable for quarterly or rare access                          |
| Retain audit logs for seven years                                   | **Archive**              | Lowest storage cost for long-term retention                    |
| Store tax records accessed during a yearly audit                    | **Archive**              | Data is accessed less than once a year                         |
| Keep a disaster-recovery copy that might be needed every few months | **Coldline**             | Lower storage cost while keeping immediate accessibility       |
| Unsure how frequently objects will be accessed                      | **Autoclass**            | Google automatically moves objects between appropriate classes |
| Temporary files that may be deleted within a few days               | **Standard**             | No early-deletion charge                                       |
| CI/CD artifacts used for current deployments                        | **Standard**             | Frequently downloaded and replaced                             |
| Old application releases retained for rollback                      | **Nearline or Coldline** | Depends on how frequently rollback occurs                      |
| CCTV footage retained for 30–90 days                                | **Nearline**             | Usually retained but not regularly watched                     |
| CCTV footage retained for several years                             | **Archive**              | Long retention and very rare access                            |

