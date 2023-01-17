from gyazo import Api
import os

class GyazoSender():
  @classmethod  
  def send(cls, filename):
    client = Api(access_token=os.getenv('GYAZO_ACCESS_TOKEN'))
    with open(filename, 'rb') as f:
      image = client.upload_image(f)
      return image
