import sys
from datetime import datetime, timezone, timedelta
from oauth2client import client
from googleapiclient import sample_tools

def main(argv):
    # Authenticate and construct service.
    service, flags = sample_tools.init(
        argv, 'calendar', 'v3', __doc__, __file__,
        scope='https://www.googleapis.com/auth/calendar.readonly')

    # Global Variable Definitions
    email = 'USER@DOMAIN.COM'           #T his should be your gmail address tied to your calendar
    domain = (email.split("@",1))[1]
    meanSalary = 100000                 #  Modify this to match your company/team's mean salary
    meanSalaryPeour = round(meanSalary/2080,2)
    totalMeetings = 0
    totalHours = 0
    totalCost = 0
    today = datetime.now(timezone.utc).astimezone().replace(microsecond=0)
    start = (today - timedelta(7)).isoformat()
    end = (today + timedelta(7)).isoformat()

    try:
        page_token = None

        while True:
            # Connect via google API and query all meeting events within start and end dates in global variables
            calendar = service.calendars().get(calendarId=email).execute()
            events = service.events().list(calendarId=calendar['summary'], pageToken=page_token, showDeleted=False, timeMin=start, timeMax=end, singleEvents=True, orderBy='startTime').execute()

            for event in events['items']:
                # Cancelled meetings don't show a summary and throw an error, so check that the event has the summary property
                if 'summary' in event:
                    # Timey Wimey stuff
                    eventStartObj = datetime.strptime((event['start'].get('dateTime', event['start'].get('date'))), '%Y-%m-%dT%H:%M:%S%z')
                    eventEndObj = datetime.strptime((event['end'].get('dateTime', event['end'].get('date'))), '%Y-%m-%dT%H:%M:%S%z')
                    eventDur = round((eventEndObj - eventStartObj).total_seconds()/3600,3)
                    
                    # Initialize variable to track Company Employees that have Accepted the meeting request for the current meeting event
                    acceptedAttendees = 0

                    # Solo event/placeholders in the calendar doesn't have an attendees property, so check for that
                    if 'attendees' in event:
                        for i in event['attendees']:
                            # Iterate the number of Company Employees that have Accepted the meeting request
                            if i['responseStatus'] == 'accepted':
                                if '@' + domain in i['email']:
                                    acceptedAttendees+=1
                                else: exit
                            else: exit
                        #Print each event title, its duration in hours, the number of Company Employees that accepted, and calculate the cost of that meeting based on the meanSalaryPeour global variable
                        print(event['summary'] + ", " + str(eventDur) + " Hours, " + str(acceptedAttendees) + " " + domain + " Attendees, COST: ${:,.2f}".format(float(acceptedAttendees)*meanSalaryPeour*float(eventDur)))
                        
                        # Iterate total number of meetings used to calculate cost
                        totalMeetings += 1
                    else:
                        # Don't track time or cost for solo events
                        exit
                    # Calculate Hours and Cost of meetings against global variables
                    totalHours += (acceptedAttendees * eventDur)
                    totalCost += (float(acceptedAttendees) * meanSalaryPeour)
                else:
                    exit
            # If you have a shit ton of meetings, the google API paginates the responses.  This moves to the next batch of meeting events.
            page_token = events.get('nextPageToken')
            if not page_token:
                break
        # Dump the global variables for total time and cost pissed away in meeting events
        print ("TOTAL MEETINGS: " + str(totalMeetings) + "   TOTAL MEETING HOURS: " + str(round(totalHours,2)) + "   TOTAL COST: ${:,.2f}".format(float(totalCost)))
    # If your token has expired, it should pop up a browser and ask you to authenticate the app, but just in case throw the exception
    except client.AccessTokenRefreshError:
        print('The credentials have been revoked or expired, please re-run'
              'the application to re-authorize.')

if __name__ == '__main__':
    main(sys.argv)