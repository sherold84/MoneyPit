# MoneyPit
Determine how much time and money is spent in the company meetings you attend that are managed by Google Calendar
## Required Python libaries
- pip install datetime 
- pip install oauth2client 
- pip install google-api-python-client
## Configuration
1. Open client_secrets.json and modify client_email to your company address
   - I don't know that this actually matters...
2. open MoneyPit.py and modify:
   - The email global variable for your account
   - The Mean Salary for your Company/Team
   - startDays and endDays to determine how many days Back in time to start, and how far into the future to look
