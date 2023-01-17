from flask import Flask, render_template, request, redirect, session
import tweepy
from dotenv import load_dotenv
import os
import requests
from datetime import timedelta
from requests_oauthlib import OAuth1Session
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

client = tweepy.Client(BEARER_TOKEN)

@app.route('/')
def index():
  name = 'Hello world'
  print(session['screen_name'])
  
  # response = client.get_user(username='PoporonPoyopoyo')
  # user_id = response.data.id
  # print(user_id)
  # print(response.data.name)
  # response = client.search_recent_tweets(f'#なぎのらいぶ from:{user_id}')
  # tweets = response.data
  # print(response.data)
    
  return render_template('index.html', name=name)

@app.route('/calender', methods=['POST'])
def calender():
  
  return redirect('/')

@app.route('/sign_in')
def sign_in():
  session_req = OAuth1Session(CONSUMER_KEY, CONSUMER_SECRET)
  response = session_req.post(OAUTH_REQUEST_TOKEN_URL, params={
    'oauth_callback': 'https://mashiro-calender.fly.dev'
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
  session['id'] = tokens['user_id']
  session['oauth_token'] = tokens['oauth_token']
  session['oauth_token_secret'] = tokens['oauth_token_secret']
  session['screen_name'] = tokens['screen_name']

  return redirect('/')

if __name__ == '__main__':
  app.run(debug=True)
