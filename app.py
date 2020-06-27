import os
from notion.client import NotionClient
from flask import Flask
from flask import request

app = Flask(__name__)


def trackWeather(TOKEN, URL, weather):
    # notion
    client = NotionClient(TOKEN)
    block = client.get_block(URL)
    block.title = weather

def createTweet(TOKEN, collectionURL, tweet, author, followers):
    # notion
    client = NotionClient(TOKEN)
    cv = client.get_collection_view(collectionURL)
    row = cv.collection.add_row()
    row.tweet = tweet
    row.author = author
    row.followers = followers


def createTask(TOKEN, collectionURL, content):
    # notion
    client = NotionClient(TOKEN)
    cv = client.get_collection_view(collectionURL)
    row = cv.collection.add_row()
    row.task = content


def createReceipt(TOKEN, collectionURL, product, content, url, date):
    # notion
    client = NotionClient(TOKEN)
    cv = client.get_collection_view(collectionURL)
    row = cv.collection.add_row()
    row.product = product
    row.content = content
    row.url = url
    row.date = date

def createCalendarEvent(TOKEN, collectionURL, description, event_begins, event_ends, location, summary, duration_mins, event_begins_pretty):
    # notion
    print("Entered createCalendarEvent for "+summary )
    client = NotionClient(TOKEN)
    cv = client.get_collection_view(collectionURL)
    row = cv.collection.add_row()
    row.description = description
    row.event_begins = event_begins
    row.event_ends = event_ends
    row.location = location
    row.summary = summary
    row.duration_mins = duration_mins
    row.event_begins_pretty = event_begins_pretty
    print("Finished createCalendarEvent for "+summary )



def createEvent(TOKEN, collectionURL, product, content, url, date):
    # notion
    client = NotionClient(TOKEN)
    cv = client.get_collection_view(collectionURL)
    row = cv.collection.add_row()
    row.product = product
    row.content = content
    row.url = url
    row.date = date


def createEmail(TOKEN, collectionURL, sender, subject, message_url):
    # notion
    client = NotionClient(TOKEN)
    cv = client.get_collection_view(collectionURL)
    row = cv.collection.add_row()
    row.sender = sender
    row.subject = subject
    row.message_url = message_url


@app.route('/twitter', methods=['GET'])
def twitter():
    tweet = request.args.get('tweet')
    author = request.args.get('author')
    followers = request.args.get('followers')
    TOKEN_v2 = os.environ.get("TOKEN")
    url = os.environ.get("URL")
    createTweet(TOKEN_v2, url, tweet, author, followers)
    return f'added {tweet} to Notion'


@app.route('/tasks', methods=['GET'])
def tasks():
    todo = request.args.get('task')
    TOKEN_v2 = os.environ.get("TOKEN")
    url = os.environ.get("URL")
    createTask(TOKEN_v2, url, todo)
    return f'added {todo} to Notion'


@app.route('/gmailreceipts', methods=['GET'])
def gmailReceipt():
    product = request.args.get('product')
    content = request.args.get('content')
    message_url = request.args.get('url')
    date = request.args.get('date')
    TOKEN_v2 = os.environ.get("TOKEN")
    url = os.environ.get("URL")
    createCalendarEvent(TOKEN_v2, url, product, content, message_url, date)
    return f'added {product} receipt to Notion'

@app.route('/import_calendar', methods=['GET'])
def CalendarImport():
    print("Entered CalendarImport")
    description = request.args.get('description')
    event_begins = request.args.get('event_begins')
    event_ends = request.args.get('event_ends')
    location = request.args.get('location')
    summary = request.args.get('summary')
    duration_mins = request.args.get('duration_mins')
    event_begins_pretty = request.args.get('event_begins_pretty')
    TOKEN_v2 = os.environ.get("TOKEN")
    collectionURL = os.environ.get("collectionURL")
    createCalendarEvent(TOKEN_v2, collectionURL, description, event_begins, event_ends, location, summary, duration_mins, event_begins_pretty)
    print("Finished CalendarImport for event"+ summary)
    return f'added {summary} event to Notion'


@app.route('/createemail', methods=['GET'])
def gmailUrgentEmail():
    sender = request.args.get('sender')
    subject = request.args.get('subject')
    message_url = request.args.get('url')
    TOKEN_v2 = os.environ.get("TOKEN")
    url = os.environ.get("URL")
    createEmail(TOKEN_v2, url, sender, subject, message_url)
    return f'added email from {sender} to Notion'

@app.route('/getweather', methods=['GET'])
def getWeather():
    weather = str(request.args.get('weather'))
    TOKEN_v2 = os.environ.get("TOKEN")
    url = os.environ.get("URL")
    trackWeather(TOKEN_v2, url, weather)
    return f'added {weather} to Notion'


if __name__ == '__main__':
    TOKEN_v2 = os.environ.get("TOKEN")
    app.debug = True
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
