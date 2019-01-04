# API Notify Script
This script was written to submit a notification from OP5 Monitor to another API such as a ticketing system.

To install this script.
1. Download the file to /opt/plugins/custom/api_notify.py
2. Run the following command `chmod a+x /opt/plugins/custom/api_notify.py`
3. Add the command to OP5 Monitor Name = `api_notify` Command Syntax = `$USER1$/custom/api_notify.pl --url http(s)://ADDRESS:PORT/YOUR/API/ENDPOINT --apikey APIKEY   --element hostalias:"$HOSTALIAS$" --element hostname:"$HOSTNAME$" --element hostaddress:"$HOSTADDRESS$" --element hoststate:"$HOSTSTATE$" --element hostoutput:"$HOSTOUTPUT$" --element shortdatetime:"$SHORTDATETIME$`"
4. Assign this notification method to a contact
5. assign the contact to a host
