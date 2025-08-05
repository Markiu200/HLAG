import base64
import os

def hello(file):
  print("Hello!")

with open("D:\hlag\lib\img2.png", "rb") as image_file:
  # print(base64.b64encode(image_file.read()))
  pass

filename = "D:\hlag\lib\img2.png"
print(os.stat(filename))