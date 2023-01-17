import os
from datetime import timedelta, datetime

import requests
import tweepy
from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request, session
from requests_oauthlib import OAuth1Session

from calender_generator import CalenderGenerator
from gyazo_sender import GyazoSender
from utils import to_dict

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv('APP_SECRET_KEY')
app.permanent_session_lifetime = timedelta(days=20)

CONSUMER_KEY = os.getenv('API_KEY')
CONSUMER_SECRET = os.getenv('API_KEY_SECRET')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')
BEARER_TOKEN = os.getenv('BEARER_TOKEN')

TWITTER_API_HOST = 'https://api.twitter.com'
OAUTH_REQUEST_TOKEN_URL = TWITTER_API_HOST + '/oauth/request_token'
OAUTH_AUTHENTICATE_URL = TWITTER_API_HOST + '/oauth/authenticate'
OAUTH_ACCESS_TOKEN_URL = TWITTER_API_HOST + '/oauth/access_token'

CALENDER_DATES = range(19, 28)
QUERY = '#なぎのらいぶ'

client = tweepy.Client(BEARER_TOKEN)

@app.route('/')
def index():
  data = {
    'alert': request.args.get('alert'),
    'notice': request.args.get('notice'),
    'username': session.get('screen_name'),
    'user_id': session.get('user_id'),
    'image': request.args.get('image'),
    'dates': session.get('dates'),
  }
  return render_template('index.html', **data)

@app.route('/calender', methods=['POST'])
def calender():
  response = client.search_recent_tweets(
    f'{QUERY} from:{session.get("user_id")}',
    max_results=100,
    tweet_fields=['created_at'],
  )
  tweets = response.data
  
  dates = set(session.get('dates') or [])
  for tweet in tweets:
    if tweet.created_at.day in CALENDER_DATES:
      dates.add(tweet.created_at.day)

  dates = list(dates)
  session['dates'] = dates

  CalenderGenerator().create_calender(dates)
  image = GyazoSender.send('assets/images/calender.png')
  
  return redirect(f'/?image={image.url}')

@app.route('/add_dates', methods=['POST'])
def add_dates():
  link = request.form.get('tweet')
  tweet_id = link.split('/')[-1]
  response = client.get_tweet(
    tweet_id,
    expansions=['author_id'],
    tweet_fields=['created_at']
  )

  user_id = response.includes.get('users')[0].id
  created_at = response.data.created_at.day
  
  dates = set(session.get('dates') or [])
  
  if str(user_id) == session.get('user_id') and created_at in CALENDER_DATES:
    dates.add(created_at)
  
  dates = list(dates)
  session['dates'] = dates

  CalenderGenerator().create_calender(dates)
  image = GyazoSender.send('assets/images/calender.png')

  return redirect(f'/?image={image.url}')

@app.route('/sign_in')
def sign_in():
  session_req = OAuth1Session(CONSUMER_KEY, CONSUMER_SECRET)
  response = session_req.post(OAUTH_REQUEST_TOKEN_URL, params={
    'oauth_callback': 'https://mashiro-calender.fly.dev/sign_in_callback'
  })
  tokens = to_dict(response.text)
  return redirect(f'{OAUTH_AUTHENTICATE_URL}?oauth_token={tokens["oauth_token"]}')

@app.route('/sign_in_callback')
def sign_in_callback():
  oauth_token = request.args.get('oauth_token')
  oauth_verifier = request.args.get('oauth_verifier')

  response = requests.post(OAUTH_ACCESS_TOKEN_URL, params={
    "oauth_verifier": oauth_verifier,
    "oauth_token": oauth_token
  })

  tokens = to_dict(response.text)
  session['user_id'] = tokens['user_id']
  session['oauth_token'] = tokens['oauth_token']
  session['oauth_token_secret'] = tokens['oauth_token_secret']
  session['screen_name'] = tokens['screen_name']

  return redirect('/')

@app.route('/logout')
def logout():
  session.clear()
  return redirect('/')

if __name__ == '__main__':
  app.run(debug=True)
