from flask import Flask, render_template, request
import tweepy
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)

consumer_key = os.getenv('API_KEY')
consumer_secret = os.getenv('API_KEY_SECRET')
access_token = os.getenv('ACCESS_TOKEN')
access_token_secret = os.getenv('ACCESS_TOKEN_SECRET')
bearer_token = os.getenv('BEARER_TOKEN')

client = tweepy.Client(bearer_token)

@app.route('/')
def index():
  name = 'Hello world'
  response = client.get_user(username='PoporonPoyopoyo')
  user_id = response.data.id
  print(user_id)
  print(response.data.name)
  response = client.search_recent_tweets(f'#なぎのらいぶ from:{user_id}')
  tweets = response.data
  print(response.data)
    
  return render_template('index.html', name=name)

@app.route('/calender', methods=['POST'])
def calender():
  
  return render_template('index.html', name='form successful?')

if __name__ == '__main__':
  app.run(debug=True)
