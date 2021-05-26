#!/usr/bin/python3
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), "lib"))
import api
from utils import commonAttribs, commonAttribValues, choose, printMatch, parseVideoId, reparseAll
from parsing import commonInfos
from db import save


def promptVideoId():
  try:
    return parseVideoId(input("Video id or link (Ex. dQw4w9WgXcQ): "))
  except Exception:
    print("Invalid id or link!")
    raise ValueError


def listVideoInfo(videoId):
  if videoId in api.videos:
    if "Raw Description" in api.videos[videoId]:
      print("Raw Description:")
      print("\n".join(api.videos[videoId]["Raw Description"]))
      print("\n\n", end="")
      print("--- End of raw description ---")
      print("\n\n", end="")

    print("Extracted Infos:\n")
    for attrib in commonInfos:
      if attrib in api.videos[videoId]:
        value = api.videos[videoId][attrib]

        print("{}: {}".format(attrib, '\n'.join(value) if isinstance(value, list) else value))
  else:
    print("Error: Video id is not in the database :(")


def query():
  aliveOnly = "n" not in input("Exclude unavailable videos? (y) ").lower()

  attribs = commonAttribs(api.videos, aliveOnly=aliveOnly)
  attribChose = choose(attribs)

  while True:
    print("Choose query method:")
    print("0. List all kinds of value and let me choose one")
    print("1. Find everything that matches my following input")
    try:
      optionChose = int(input("Choose: "))
      assert optionChose in [0, 1]
      break
    except Exception:
      print("Invalid option! Try again")

  if optionChose == 0:
    attribValues = commonAttribValues(api.videos, attribs[attribChose][0], aliveOnly=aliveOnly)
    valueChose = choose(attribValues)

    printMatch(api.videos, attribs[attribChose][0], attribValues[valueChose][0], aliveOnly=aliveOnly)
  elif optionChose == 1:
    target = input("Search for: ")
    printMatch(api.videos, attribs[attribChose][0], target, exact=False, aliveOnly=aliveOnly)


def main():
  print("What would you like to do today?")
  while True:
    optionChose = -1
    while True:
      print("0. Query the database")
      print("1. Attempt to find the lyrics for a video in comment section (YouTube API key needed)")
      print("2. List info about a video in the database")
      print("8. Database maintenance (You may come in if you wish)")
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
      print("What drink would you like to have tonight?")
      while True:
        optionChose = -1
        print("0. Update the database (YouTube API key needed)")
        print("1. Update just the last added channel's info (YouTube API key needed, used to save API quota)")
        print("5. Reparse all video descriptions")
        print("9. I'm just looking around (Leave)")
        try:
          optionChose = int(input("Choose: "))
          assert optionChose in [0, 1, 5, 9]
          break
        except Exception:
          print("Invalid option! Try again")
      if optionChose == 0:
        api.updateDatabase()
      elif optionChose == 1:
        api.updateDatabase(True)
      elif optionChose == 5:
        api.videos = reparseAll(api.videos)
        save(api.videos)
      elif optionChose == 9:
        print("Okay!")
    elif optionChose == 9:
      print("Goodbye.")
      break

    print()
    print()


if __name__ == "__main__":
  main()
