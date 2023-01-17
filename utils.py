def to_dict(str):
  return { x.split('=')[0]: x.split('=')[1]
          for x in str.split('&') }
