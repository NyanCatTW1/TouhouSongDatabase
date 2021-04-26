try:
  import romkan
  romkanAvail = True
except ImportError:
  romkanAvail = False
import urllib.parse as urlparse
from urllib.parse import parse_qs
import pyperclip
from random import shuffle

global deadChannels
deadChannels = ["Alice Margatroid"]


def deadVideo(videoId, videos):
  return "Channel" not in videos[videoId] or videos[videoId]["Channel"] in deadChannels


def s(num, suffix="s"):
  return suffix if num > 1 else ""


def sumAttribs(dict):
  ret = 0
  for value in dict.values():
    ret += len(value)
  return ret


def dbStatus(videos):
  attribs = sumAttribs(videos)
  print("Storing {} attribute{} of {} video{} in the database".format(attribs, s(attribs), len(videos), s(len(videos))))


def descendingDict(dict):
  return sorted(list(dict.items()), key=lambda x: x[1], reverse=True)


def commonAttribs(videos, aliveOnly=True):
  count = {}
  for videoId in videos.keys():
    if aliveOnly and deadVideo(videoId, videos):
      continue

    for attrib in videos[videoId]:
      if attrib not in count:
        count[attrib] = 1
      else:
        count[attrib] += 1
  return descendingDict(count)


def commonAttribValues(videos, target, aliveOnly=True):
  count = {}
  for videoId in videos.keys():
    if aliveOnly and deadVideo(videoId, videos):
      continue

    video = videos[videoId]
    if target in video:
      if isinstance(video[target], list):
        for value in video[target]:
          if value not in count:
            count[value] = 1
          else:
            count[value] += 1
      else:
        if video[target] not in count:
          count[video[target]] = 1
        else:
          count[video[target]] += 1
  return descendingDict(count)


def printMatch(videos, attrib, value, exact=True, aliveOnly=True):
  matches = []
  for video in videos.keys():
    if aliveOnly and deadVideo(video, videos):
      continue

    if attrib in videos[video]:
      match = False
      if isinstance(videos[video][attrib], list):
        if value in videos[video][attrib]:
          match = True
        elif not exact and any(value.lower() in line.lower() for line in videos[video][attrib]):
          match = True
      else:
        if videos[video][attrib] == value:
          match = True
        elif not exact and value.lower() in videos[video][attrib].lower():
          match = True

      if match:
        if len(matches) == 0:
          print("\nResults:")
        print("https://youtu.be/{} - {}".format(video, videos[video]["Title"]))
        matches.append(video)
  if len(matches) > 50:
    print("WARNING: There are more than 50 matches, the playlist below will include 50 random videos from the matches.")
  elif len(matches) == 0:
    print("No matches.")
    return
  print()
  print("Sometimes the playlist wouldn't work because the first video is unavailable.\nIn that case, remove the first video id from the link and try again.")

  shuffle(matches)
  playlistURL = "https://www.youtube.com/watch_videos?video_ids={}".format(",".join(matches[:50]))
  print("Playlist:\n{}".format(playlistURL))
  if "y" in input("Copy the playlist URL above to the clipboard? (n) ").lower():
    pyperclip.copy(playlistURL)
    print("Copied to clipboard.")


def toRomaji(line):
  return romkan.to_hepburn(line)


def choose(items):
  while True:
    try:
      print("Please choose the target:")
      for i in range(len(items) - 1, -1, -1):
        print("{}: {} ({})".format(i, items[i][0], items[i][1]))
      choose = int(input("Choose (0~{}): ".format(len(items) - 1)))
      assert choose >= 0 and choose < len(items)
      return choose
    except Exception:
      print("Invalid option! Try again")


def parseVideoId(url):
  url = url.strip()
  try:
    parsed = parse_qs(urlparse.urlparse(url).query)['v'][0]
    return parsed
  except Exception:
    url = url.split('/')[-1]
    if len(url) == 11:
      return url
    else:
      raise ValueError
