#!/usr/bin/python3
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), "lib"))
import api
from utils import commonAttribs, commonAttribValues, choose, printMatch, parseVideoId


def promptVideoId():
  try:
    return parseVideoId(input("Video id or link (Ex. dQw4w9WgXcQ): "))
  except Exception:
    print("Invalid id or link!")
    raise ValueError


def listVideoInfo(videoId):
  if videoId in api.videos:
    for attrib in api.videos[videoId]:
      value = api.videos[videoId][attrib]

      print("{}: {}".format(attrib, '\n'.join(value) if isinstance(value, list) else value))
  else:
    print("Error: Video id is not in the database :(")


def query():
  attribs = commonAttribs(api.videos)
  attribChose = choose(attribs)

  attribValues = commonAttribValues(api.videos, attribs[attribChose][0])
  valueChose = choose(attribValues)

  printMatch(api.videos, attribs[attribChose][0], attribValues[valueChose][0])


def main():
  print("What would you like to do today?")
  while True:
    optionChose = -1
    while True:
      print("0. Query the database")
      print("1. Attempt to find the lyrics for a video in comment section (YouTube API key needed)")
      print("2. List info about a video in the database")
      print("8. Update the database (YouTube API key needed)")
      print("9: Leave")
      try:
        optionChose = int(input("Choose: "))
        assert optionChose in [0, 1, 2, 8, 9]
        break
      except Exception:
        print("Invalid option! Try again")

    if optionChose == 0:
      query()
    elif optionChose == 1:
      try:
        videoId = promptVideoId()
      except Exception:
        continue
      print(api.findLyrics(videoId))
    elif optionChose == 2:
      try:
        videoId = promptVideoId()
      except Exception:
        continue
      listVideoInfo(videoId)
    elif optionChose == 8:
      api.updateDatabase()
    elif optionChose == 9:
      print("Goodbye.")
      break

    print()
    print()


if __name__ == "__main__":
  main()
