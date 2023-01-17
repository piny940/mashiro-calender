from PIL import Image

class CalenderGenerator():
  def __init__(self):
    self.base = Image.open('assets/images/mashiro-calender.png')
    self.stamp = Image.open('assets/images/mashiro-stamp.png')
  
  def create_calender(self, stamp_dates):
    for date in stamp_dates:
      self.__stamp_calender(self.base, date)
    
    self.base.save('static/images/calender.png')
  
  def __stamp_calender(self, image, date):
    image.paste(self.stamp, self.__date_coordinates(date), self.stamp)
  
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

CalenderGenerator().create_calender([19, 24])
