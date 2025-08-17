import base64
import os


def hello(file):
  print("Hello!")

with open("D:\hlag\mylib\img2.png", "rb") as image_file:
  #https://stackoverflow.com/questions/17615414/how-to-convert-binary-string-to-normal-string-in-python3
  print(base64.b64encode(image_file.read()).decode('ascii'))
  pass

filename = "D:\hlag\mylib\img2.png"
print(os.stat(filename))