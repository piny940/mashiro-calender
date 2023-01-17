from flask import Flask, render_template, request
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)

@app.route('/')
def index():
  name = 'Hello world'
  return render_template('index.html', name=name)

@app.route('/calender', methods=['POST'])
def calender():
  if request.method == 'POST':
    print(request.form)
    print(request.form['username'])
  
  return render_template('index.html', name='form successful?')

if __name__ == '__main__':
  app.run(debug=True)
