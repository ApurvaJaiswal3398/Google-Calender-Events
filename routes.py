from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from flask import render_template, redirect, request
from Calender import app

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

creds = None
if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)

if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    
    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)

service = build('calendar', 'v3', credentials=creds)

def getevents(s,e):
    eventsResult = service.events().list(calendarId='primary', timeMin=s, timeMax=e, singleEvents=True, orderBy='startTime').execute()
    events = eventsResult.get('items', [])
    return events
    
@app.route('/')
def home():
    return redirect('/daily_event_view')

def weekview(s_week, day):
    s_date = s_week + 'T00:00:00Z'
    start_date = datetime.datetime.strptime(s_date,'%Y-%m-%dT%H:%M:%SZ')
    week = datetime.timedelta(days=day)
    end_date = start_date + week
    e_date = end_date.isoformat() + 'Z'
    return s_date,e_date

@app.route('/daily_event_view', methods=['GET','POST'])
def daily():
    events=s=None
    if request.method == 'POST':
        s = request.form.get('sdate')
        s,e = weekview(s,1)
        events = getevents(s,e)
    return render_template('dailyview.html', events=events, s=s)

@app.route('/weekly_event_view', methods=['GET','POST'])
def weekly():
    events=s=e=None
    if request.method == 'POST':
        s = request.form.get('sdate')
        s,e = weekview(s,7)
        events = getevents(s,e)
    return render_template('weeklyview.html', events=events, s=s, e=e)