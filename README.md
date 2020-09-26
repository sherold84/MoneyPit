# MoneyPit
Determine how much time and money is spent in the Red Hat meetings you attend
## Required Python libaries
- pip install datetime 
- pip install oauth2client 
- pip install google-api-python-client
## Configuration
1. Open client_secrets.json and modify client_email to your redhat.com address
   - If this fails, it may require tying my account to the client ID and Secret, so set to sherold@redhat.com
2. open MoneyPit.py and modify the email global variable for your account
