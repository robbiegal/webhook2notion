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
    row.id = id
    row.description = description
    
    #handle start time:
    event_start_params = re.split('[-T:+]',event_begins)
    event_start_params=[int(i) for i in event_start_params]
    esp = event_start_params
    if len(esp) == 8:
        event_start = datetime(esp[0],esp[1],esp[2],esp[3],esp[4],esp[5])+ timedelta(hours=-int(esp[6]))
    else:
        event_start = datetime(esp[0],esp[1],esp[2])+ timedelta(hours=-int(esp[6]))
    row.event_begins_timestamp = int(event_start.timestamp()) * 1000
    
    #handle end time:
    event_end_params = re.split('[-T:+]',event_ends)
    event_end_params=[int(i) for i in event_end_params]
    eep = event_end_params
    if len(eep) == 8:
        event_end = datetime(eep[0],eep[1],eep[2],eep[3],eep[4],eep[5])+ timedelta(hours=-int(esp[6]))
    else:
        event_end = datetime(eep[0],eep[1],eep[2])+ timedelta(hours=9)+ timedelta(hours=-int(esp[6]))
    row.event_ends_timestamp = int(event_end.timestamp()) * 1000
    
    row.date1 = [["d",{"type": "datetime", "start_date": event_start.strftime("%Y-%m-%d"), "start_time": event_start.strftime("%H:%M"), "end_time": event_end.strftime("%H:%M") }]]
    row.date2 = ["d",{"type": "datetime", "start_date": event_start.strftime("%Y-%m-%d"), "start_time": event_start.strftime("%H:%M"), "end_time": event_end.strftime("%H:%M") }]
    row.date3 = {"type": "datetime", "start_date": event_start.strftime("%Y-%m-%d")}
    row.date4 = event_start
    row.location = location
    row.summary = summary
    row.duration_mins = int(duration_mins.split('.')[0])
    row.event_begins_pretty = event_begins_pretty
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
