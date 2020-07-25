import os
from notion.client import NotionClient
from flask import Flask
from flask import request
import re
from datetime import datetime, timedelta

app = Flask(__name__)

def createCalendarEvent(TOKEN, collectionURL, description, event_begins, event_ends, location, summary, duration_mins, event_begins_pretty,id):
    # notion
    
    print("Entered createCalendarEvent for "+summary )
    client = NotionClient(TOKEN)
    cv = client.get_collection_view(collectionURL)
    row = cv.collection.add_row()
    
    row.Action_Item = summary
    row.Status = "Active"
    row.Priority = "Scheduled"
    row.Note =  (("Location: "+location) if (location!=None) else "" ) + "Description: "+str(description)
    #handle start time:
    print("Received event with timestamp of " +str(event_begins)+'\n')
    event_start_params = re.split('[-T:+]',event_begins)
    event_start_params=[int(i) for i in event_start_params]
    esp = event_start_params
    if len(esp) == 8:
        event_start = datetime(esp[0],esp[1],esp[2],esp[3],esp[4],esp[5]) - timedelta(hours = int(esp[6]))
    else:
        event_start = datetime(esp[0],esp[1],esp[2])

    row.Do_Date = event_start
    
    print("Finished createCalendarEvent for "+summary )


@app.route('/import_calendar', methods=['GET'])
def CalendarImport():
    print("Entered CalendarImport")
    description = request.args.get('description')
    event_begins = request.args.get('event_begins')   # Returns datetime in the following format: 2020-06-27T16:54:19+03:00
    event_ends = request.args.get('event_ends')
    location = request.args.get('location')
    summary = request.args.get('summary')
    id = request.args.get('id')
    duration_mins = request.args.get('duration_mins')
    event_begins_pretty = request.args.get('event_begins_pretty')
    TOKEN_v2 = os.environ.get("TOKEN")
    collectionURL = os.environ.get("collectionURL")
    createCalendarEvent(TOKEN_v2, collectionURL, description, event_begins, event_ends, location, summary, duration_mins, event_begins_pretty,id)
    print("Finished CalendarImport for event"+ summary)
    return f'added {summary} event to Notion'

if __name__ == '__main__':
    TOKEN_v2 = os.environ.get("TOKEN")
    app.debug = True
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
