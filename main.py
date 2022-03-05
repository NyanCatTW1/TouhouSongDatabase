#!/usr/bin/python3
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), "lib"))
import api
import utils
import db
import parsing


def promptVideoId():
  try:
    return utils.parseVideoId(input("Video id or link (Ex. dQw4w9WgXcQ): "))
  except Exception:
    print("Invalid id or link!")
    raise ValueError


def promptPlaylistId():
  try:
    return utils.parsePlaylistId(input("Playlist id or link (Ex. PLi9drqWffJ9FWBo7ZVOiaVy0UQQEm4IbP): "))
  except Exception:
    print("Invalid id or link!")
    raise ValueError


def query():
  aliveOnly = "n" not in input("Exclude unavailable videos? (y) ").lower()

  attribs = utils.commonAttribs(api.videos, aliveOnly=aliveOnly)
  attribChose = utils.choose(attribs)

  while True:
    print("Choose query method:")
    print("0. List all kinds of value and let me choose one")
    print("1. Find everything that matches my following input")
    print("2. Let me enter Python code that queries the database")
    try:
      optionChose = int(input("Choose: "))
      assert optionChose in [0, 1, 2]
      break
    except Exception:
      print("Invalid option! Try again")

  if optionChose == 0:
    attribValues = utils.commonAttribValues(api.videos, attribs[attribChose][0], aliveOnly=aliveOnly)
    valueChose = utils.choose(attribValues)
    matches = utils.queryWithAttrib(api.videos, attribs[attribChose][0], attribValues[valueChose][0], aliveOnly=aliveOnly)
  elif optionChose == 1:
    target = input("Search for: ")
    matches = utils.queryWithAttrib(api.videos, attribs[attribChose][0], target, exact=False, aliveOnly=aliveOnly)
  elif optionChose == 2:
    print("Warning: This will **eval** the code you enter, which could cause damage to your system if you do anything strange.")
    print("Please only enter codes that you fully understand.")
    print("Available attributes:")
    print("[" + ", ".join([f'"{x}"' for x in parsing.commonInfos + ["Raw Description"]]) + "]")
    print("You might also want to check videos.json to see how the raw data looks like.")
    print("\nExample query:")
    print('"ayo" in video["Vocal"].lower() and "ayaponzu" in video["Vocal"].lower()\n')

    target = input("Enter your query: ")
    matches = utils.queryWithEval(api.videos, target, aliveOnly=aliveOnly)

  utils.printMatch(api.videos, matches)


def main():
  print("What would you like to do today?")
  while True:
    optionChose = -1
    while True:
      print("0. Query the database")
      print("1. Attempt to find the lyrics for a video in comment section (YouTube API key needed)")
      print("2. List info about a video in the database")
      print("3. List unavailable videos in a playlist")
      print("8. Database maintenance (You may come in if you wish)")
      print("9: Leave")
      try:
        optionChose = int(input("Choose: "))
        assert optionChose in [0, 1, 2, 3, 8, 9]
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
      api.listVideoInfo(videoId)
    elif optionChose == 3:
      try:
        playlistId = promptPlaylistId()
      except Exception:
        continue
      api.listUnavailVideos(playlistId)
    elif optionChose == 8:
      print("What drink would you like to have tonight?")
      while True:
        optionChose = -1
        print("0. Update the database (YouTube API key needed)")
        print("1. Update just the last added channel's info (YouTube API key needed, used to save API quota)")
        print("2. Search for missing raw desc datas on https://scarletdevil.org/youtube/")
        print("3. Search for missing raw desc datas on https://playboard.co/")
        print("4. Reparse all video descriptions")
        print("5. List database-missing channels in playlist")
        print("9. I'm just looking around (Leave)")
        try:
          optionChose = int(input("Choose: "))
          assert optionChose in [0, 1, 2, 3, 4, 5, 9]
          break
        except Exception:
          print("Invalid option! Try again")
      if optionChose == 0:
        api.updateDatabase()
      elif optionChose == 1:
        api.updateDatabase(True)
      elif optionChose == 2:
        if input("""Please notice that this will send hundreds of requests to someone's maybe self-hosted server, so please don't proceed if you found that bad.
(plus, Nyan Cat aka. The developer probably already tried every video against the archive, so it doesn't make sense to do it again)
Enter exactly 'Yes' to proceed: """) != "Yes":
          continue
        api.videos = utils.reparseAll(utils.findDescOnScarletDevil(api.videos))
        db.save(api.videos)
      elif optionChose == 3:
        if input("""Please notice that by scraping Playboard for raw descs, you're violating Playboard's ToS, which might not be acceptable for your taste.
(plus, Nyan Cat aka. The developer probably already tried every video against the website, so it doesn't make sense to do it again)
Enter exactly 'Yes' to proceed: """) != "Yes":
          continue
        api.videos = utils.reparseAll(utils.findDescOnPlayboard(api.videos))
        db.save(api.videos)
        pass
      elif optionChose == 4:
        api.videos = utils.reparseAll(api.videos)
        db.save(api.videos)
      elif optionChose == 5:
        try:
          playlistId = promptPlaylistId()
        except Exception:
          continue
        api.listMissingChannels(playlistId)
      elif optionChose == 9:
        print("Okay!")
    elif optionChose == 9:
      print("Goodbye.")
      break

    print()
    print()


if __name__ == "__main__":
  main()
