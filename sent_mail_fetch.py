#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys
import imaplib
import getpass
import email
import email.header
import datetime

EMAIL_ACCOUNT = "mail"
EMAIL_FOLDER = "&BB4EQgQ,BEAEMAQyBDsENQQ9BD0ESwQ1-"
password = "password"

raw2_file = open('mail.csv', 'w')
raw2_file.seek(0)
raw2_file.truncate()
raw2_file.write("Message-ID,Subject,Date,From,To\n")

def process_mailbox(M):

    rv, data = M.search(None, '(SINCE "01-Sep-2016")')
    if rv != 'OK':
        print "No messages found!"
        return

    for num in data[0].split():
        rv, data = M.fetch(num, '(RFC822)')
        if rv != 'OK':
            print "ERROR getting message", num
            return

        msg = email.message_from_string(data[0][1])
        decode = email.header.decode_header(msg['Subject'])[0]
        subject = unicode(decode[0], errors='ignore')
        print 'Message %s: %s' % (num, subject)
        print 'Raw Date:', msg['Date']
	print 'From:', msg['From']
	print 'To:', msg['To']

	# if you want to print body of the message
	body = ""
	if msg.is_multipart():
    		for part in msg.walk():
        		ctype = part.get_content_type()
        		cdispo = str(part.get('Content-Disposition'))

        		# skip any text/plain (txt) attachments
        		if ctype == 'text/plain' and 'attachment' not in cdispo:
            			body = part.get_payload(decode=True)  # decode
            			break

	else:
		body = msg.get_payload(decode=True)


	raw2_file.write(num+"&"+subject+"&"+msg['Date']+"&"+msg['From']+"&"+msg['To']+"\n")

	# Now convert to local date-time
        date_tuple = email.utils.parsedate_tz(msg['Date'])
        if date_tuple:
            local_date = datetime.datetime.fromtimestamp(
                email.utils.mktime_tz(date_tuple))
            print "Local Date:", \
                local_date.strftime("%a, %d %b %Y %H:%M:%S")
	print ''

# or you can define any imap service that you want to
M = imaplib.IMAP4_SSL('imap.yandex.com')

try:
    rv, data = M.login(EMAIL_ACCOUNT, password)
except imaplib.IMAP4.error:
    print "LOGIN FAILED!!! "
    sys.exit(1)

print rv, data

rv, mailboxes = M.list()
if rv == 'OK':
    print "Mailboxes:"
    print mailboxes

rv, data = M.select(EMAIL_FOLDER)
if rv == 'OK':
    print "Processing mailbox...\n"
    process_mailbox(M)
    M.close()
else:
    print "ERROR: Unable to open mailbox ", rv

raw2_file.close()
M.logout()
