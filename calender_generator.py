from PIL import Image, ImageFont, ImageDraw

FONT_PATH = 'assets/fonts/mplus-2p-medium.otf'
FONT_SIZE = 40
NAME_COLOR = '#000080'

class CalenderGenerator():
  def __init__(self):
    self.base = Image.open('assets/images/mashiro-calender.png')
    self.base_with_namebox = Image.open(
        'assets/images/mashiro-calender-with-namebox.png')
    self.stamp = Image.open('assets/images/mashiro-stamp.png')
  
  def create_calender(self, stamp_dates, name=''):
    base = self.base_with_namebox if name else self.base
    for date in stamp_dates:
      self.__stamp_calender(base, date)
    
    if name:
      self.__embed_name(base, name)
    
    base.save('assets/images/calender.png')
  
  def __stamp_calender(self, image, date):
    image.paste(self.stamp, self.__date_coordinates(date), self.stamp)
  
  def __embed_name(self, image, name):
    font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
    draw = ImageDraw.Draw(image)
    draw.text((1472, 1024), name, font=font, fill=NAME_COLOR)
  
  def __date_coordinates(self, date):
    if date == 19:
      return (648, 409)
    elif date == 20:
      return (968, 409)
    elif date == 21:
      return (1286, 407)
    elif date == 22:
      return (1604, 403)
    elif date == 23:
      return (326, 795)
    elif date == 24:
      return (650, 789)
    elif date == 25:
      return (968, 783)
    elif date == 26:
      return (1286, 785)
    elif date == 27:
      return (1604, 787)
    else:
      return None
