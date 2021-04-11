from pyyoutube import Api
from math import ceil
from utils import s, sumAttribs, dbStatus, toRomaji
from parser import parseVideoInfo
from db import load, save

global api

global videos
videos = {}

global channels
channels = ["UCshG1-oUuFknWjXp5U1P9xw", "UCjchy66Q6XBGOTSj-jwNy1Q", "UCmC13e647V-fq4w1nwN-w-A",
            "UCNvmLRL3gdL1SH0tmCMAm5Q", "UCRgDMAlG7PEdwx7qSyHCwhQ", "UCdCbB4LwMiSnDZrKsJK-xBw",
            "UCpBHPjz8vl9ARUC5lR3w_HQ", "UCGN2wIddSBJtjQMqtj9TRQg", "UC995j0fLaZb4RHACU149w1Q",
            "UCRfCpDlKXvg3Sos0VO23tjg", "UC2w7ZUP1bjvgsRdH32wnFHg", "UC_6ZDrRqQ-tDHiOnEfAlCOA",
            "UCys2Yei-zmfEoIv27eRP55A", "UCRBTBlfAM2BmiXUsLOfZjkg", "UC_ybU5XoOleMJREJyHGwErQ",
            "UCmGMR_bG6xx9AAiPbxTr_RQ", "UCqVuUveXk-y__p19d_Uh_TA", "UCRYlptIEWcbBx5pLJ4GMq3A",
            "UCE-SRK6zlmTMWkhewnH5D_Q", "UCa99OmuuhnOQNxTsWlA4Erw", "UCxasUyz_GaQta-2NZWcQJCA",
            "UC-Go2i8mhsKiuL04TS_FDlQ", "UCgVCYnM3oT2QLrPiq6V2y9Q", "UCD8ANO8i8JKwPBqOoWjzjHA",
            "UC9-rPU1iBlhZZhaftiez0qA", "UC0eulKoXGBeZORzk5-N6n0A"]


def ensureAPI():
  global api
  try:
    api
    print("API key in place, continuing...")
  except NameError:
    api = Api(api_key=input("Please enter a valid YouTube API key: "))


def getPlaylistVideos(playlistId, count=None):
  ret = []

  response = api.get_playlist_items(playlist_id=playlistId, parts="contentDetails", count=count)
  for item in response.to_dict()["items"]:
    ret.append(item["contentDetails"]["videoId"])

  return ret


def getChannelName(channelId):
  response = api.get_channel_info(channel_id=channelId, parts="snippet")
  return response.items[0].to_dict()["snippet"]["title"]


def getUploadsPlaylist(channelId):
  response = api.get_channel_info(channel_id=channelId, parts="contentDetails")
  return response.items[0].to_dict()["contentDetails"]["relatedPlaylists"]["uploads"]


def getVideoInfo(videoId):
  ret = {}
  count = 0
  splits = ceil(len(videoId) / 50)

  for i in range(splits):
    response = api.get_video_by_id(video_id=videoId[i * 50:(i + 1) * 50], parts="snippet")
    for item in response.to_dict()["items"]:
      ret[item["id"]] = item["snippet"]["description"]
      ret[item["id"]] += "\nTitle:{}".format(item["snippet"]["title"])
    count += len(response.to_dict()["items"])
    print("Progress {}/{}".format(count, len(videoId)))

  return ret


def parseVideoInfos(videoInfos):
  ret = {}
  for id in videoInfos.keys():
    ret[id] = parseVideoInfo(videoInfos[id])

  return ret


def refreshChannel(channelId):
  print("Acquiring channel playlist id")
  playlistId = getUploadsPlaylist(channelId)
  print("Received {}".format(playlistId))

  print("Listing video in playlist")
  playlistVideos = getPlaylistVideos(playlistId, count=None)
  print("Received {} id{}".format(len(playlistVideos), s(len(playlistVideos))))

  print("Receiving video description{}".format(s(len(playlistVideos))))
  videoInfo = getVideoInfo(playlistVideos)

  print("Parsing video description{}".format(s(len(videoInfo))))
  parsedInfo = parseVideoInfos(videoInfo)

  print("Updating database")
  global videos
  beforeAttribs = sumAttribs(videos)
  videos = {**videos, **parsedInfo}
  attribs = sumAttribs(videos)
  print("{} attribute{} added".format(attribs - beforeAttribs, s(attribs - beforeAttribs), ))
  dbStatus(videos)


def refreshChannels():
  for channel in channels:
    try:
      print("Refreshing channel: {}".format(getChannelName(channel)))
    except Exception:
      print("ERROR: Cannot get the name of a channel at all, rest in pepperoni.")
      print("The victim is: {}".format(channel))
      continue

    refreshChannel(channel)
    print()


def updateDatabase():
  ensureAPI()
  refreshChannels()
  save(videos)


def getVideoComment(videoId):
  response = api.get_comment_threads(video_id=videoId, order="relevance", count=100, limit=100)
  ret = []
  for comment in response.to_dict()["items"]:
    ret.append(comment["snippet"]["topLevelComment"]["snippet"]["textOriginal"].replace("\r\n", "\n").split("\n"))
  return ret


def findLyrics(videoId):
  ensureAPI()
  comments = getVideoComment(videoId)
  return "\n".join(map(toRomaji, max(comments, key=len)))


videos = load()

if __name__ == "__main__":
  # updateDatabase()
  pass
