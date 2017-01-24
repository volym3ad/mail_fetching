# mail_fetching
**Service for fetching sent mail from Yandex**

To use this script change *EMAIL_ACCOUNT* and *password* variables to your own.    
Result is written to main.csv

If you want to specify other imap service than Yandex, change parameter in imaplib.IMAP4_SSL('imap.yandex.com') and EMAIL_FOLDER.   
For example, if you want Google - imaplib.IMAP4_SSL('imap.gmail.com') and EMAIL_FOLDER = "Sent".   

Unfortunately, Yandex uses strange hash definitions to its Mailboxes (except INBOX). Because it is russian service ¯\_(ツ)_/¯
