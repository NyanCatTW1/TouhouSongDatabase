try:
  import romkan
  romkanAvail = True
except ImportError:
  romkanAvail = False
import urllib.parse as urlparse
from urllib.parse import parse_qs
import pyperclip
from random import shuffle
import parsing
import requests
from bs4 import BeautifulSoup
import traceback
import tqdm


global metaKeys
metaKeys = ["deadVids"]


def deadVideo(videoId, videos):
  return videoId in videos["deadVids"]


def s(num, suffix="s"):
  return suffix if abs(num) > 1 else ""


def sumAttribs(dict):
  ret = 0
  for value in dict.values():
    ret += len(value)
  return ret


def dbStatus(videos, useTqdm=False):
  attribs = sumAttribs(videos)

  toPrint = "Storing {} attribute{} of {} video{} in the database".format(attribs, s(attribs), len(videos), s(len(videos)))
  if useTqdm:
    tqdm.tqdm.write(toPrint)
  else:
    print(toPrint)


def descendingDict(dict):
  return sorted(list(dict.items()), key=lambda x: x[1], reverse=True)


def commonAttribs(videos, aliveOnly=True):
  count = {}
  for videoId in videos.keys():
    if videoId in metaKeys:
      continue
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
    if videoId in metaKeys:
      continue
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


def queryWithAttrib(videos, attrib, value, exact=True, aliveOnly=True):
  matches = []
  i = 0
  for video in videos.keys():
    i += 1
    if video in metaKeys:
      continue
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
        matches.append(video)

      if i % 10000 == 0:
        print(f"On video {i}...")
  return matches


def queryWithEval(videos, code, aliveOnly=True):
  matches = []
  i = 0
  errors = 0
  for videoId in videos.keys():
    i += 1
    if videoId in metaKeys:
      continue
    if aliveOnly and deadVideo(videoId, videos):
      continue

    video = videos[videoId]

    try:
      if eval(code, locals()):
        matches.append(videoId)
    except Exception:
      if errors == 0:
        traceback.print_exc()
        print("Further errors will be hidden")
      errors += 1

    if i % 10000 == 0:
      print(f"On video {i}...")
  print(f"{errors} error{s(errors)}")
  return matches


def printMatch(videos, matches):
  if len(matches) == 0:
    return

  print("\nResults:")
  for video in matches:
    try:
      print("https://youtu.be/{} - {}".format(video, videos[video]["Title"]))
    except Exception:
      print("https://youtu.be/{} - (Failed to get title)".format(video))
  print("Found {} match{}".format(len(matches), s(len(matches), "es")))
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


def parsePlaylistId(url):
  url = url.strip()
  try:
    parsed = parse_qs(urlparse.urlparse(url).query)['list'][0]
    return parsed
  except Exception:
    url = url.split('=')[-1]
    if len(url) == 34:
      return url
    else:
      raise ValueError


def reparseAll(videos):
  print("Before reparse:")
  dbStatus(videos)

  i = 1
  for videoId in videos.keys():
    if i % 1000 == 0:
      print("Parsing video {}".format(i))
    i += 1
    if "Raw Description" not in videos[videoId]:
      if videoId not in metaKeys and "Channel" not in videos[videoId]:
        videos[videoId]["Channel"] = "Alice Margatroid"
      continue
    videos[videoId] = parsing.parseVideoInfo("\n".join(videos[videoId]["Raw Description"]), videos[videoId]["Channel"])

  print("After reparse:")
  dbStatus(videos)
  return videos


def vidsWithoutRawDesc(videos):
  ret = []
  for videoId in videos:
    if videoId not in metaKeys and "Raw Description" not in videos[videoId]:
      ret.append(videoId)
  return ret


def findDescOnScarletDevil(videos):
  todos = vidsWithoutRawDesc(videos)
  i = 0
  win = 0
  lose = 0
  for videoId in todos:
    url = "https://scarletdevil.org/youtube/video.php?v={}".format(videoId)
    print("Fetching {} ({:.1f}%)".format(url, i / len(todos) * 100))
    i += 1

    try:
      page = requests.get(url)
      soup = BeautifulSoup(page.content, 'html.parser')
      tables = soup.find_all("table")
      if len(tables) >= 2:
        desc = tables[1].find_all("td")[-1].decode_contents()
        desc = desc.replace("<br/>", "").replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
        videos[videoId]["Raw Description"] = desc.split("\n")
        print("Bravo!")
        win += 1
      else:
        print("No record here! :(")
        lose += 1
    except Exception:
      traceback.print_exc()
      print("Maybe next time...")
      lose += 1

    print("{} win{} and {} lose{} ({:.1f}% success rate)\n".format(win, s(win), lose, s(lose), win / (win + lose) * 100))
  return videos


def findDescOnPlayboard(videos):
  todos = vidsWithoutRawDesc(videos)
  i = 0
  win = 0
  lose = 0
  for videoId in todos:
    url = "https://playboard.co/en/video/{}".format(videoId)
    print("Fetching {} ({:.1f}%)".format(url, i / len(todos) * 100))
    i += 1

    try:
      page = requests.get(url)
      soup = BeautifulSoup(page.content, 'html.parser')
      divs = soup.findAll('div', {'class': 'detail__desc'})
      if len(divs) > 0:
        desc = divs[0].find_all("pre")[0].decode_contents()
        desc = desc.replace("<br/>", "").replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
        videos[videoId]["Raw Description"] = desc.split("\n")
        print("Bravo!")
        win += 1
      else:
        print("No record here! :(")
        lose += 1
    except Exception:
      traceback.print_exc()
      print("Maybe next time...")
      lose += 1

    print("{} win{} and {} lose{} ({:.1f}% success rate)\n".format(win, s(win), lose, s(lose), win / (win + lose) * 100))
  return videos
