from pyyoutube import Api
from math import ceil
import utils
import parsing
import db

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
            "UC9-rPU1iBlhZZhaftiez0qA", "UC0eulKoXGBeZORzk5-N6n0A", "UCU-QbDlDekATodksv-CNMbg",
            "UCC22yriBfflJdSSBqdLItxQ", "UCKhgKi54I4NlLyyzdLAEbhg", "UCAXFRF9HF0TM2KBnDD-ENhQ",
            "UCx7IooUYRipwOIVJSK0e5ug", "UC7eotbkZxg1GDJT6-8xSOCg", "UC0INc3mUY3QG6-8nnnz7yXA",
            "UCyNA3mQpMAQ59wn0A4uMb5w", "UC4VV8oMlE1A7HEm-hLL5jOg", "UCEddH3sFwOD0AUohA7S06Gg",
            "UC2pRD-iKpUas0o1PSlRLKPg", "UCXUd33vRPGZcfb8pngQpVlQ", "UCVODOPBpytFipYx8iFVZfJA",
            "UC3Cmic0GwevYwxJv96_oUNw", "UCvBZoxNTEr9558Kxzd_QnRg", "UClGm4dxaLMmb2MkNueaoCaw",
            "UCTSKhJyHFTdR8IVpUktctTw", "UCxG8IWOc_Go_51HmAUIvpBA", "UCipByvDWfTaGHgXxADbczkw",
            "UCuKWnqGUu17b6zCj1_vU4cQ", "UC0vDI17CAL84tAHmUbmd7DQ", "UCf-pXI7JffTY0ggPr74dvqw",
            "UC-TgSyKEraAAdNgBtpY8V4g", "UCzwmuzDOmQ6NwfFKd8qrulg", "UCWqMUzeLAF5RUHKYQTD3nMw",
            "UCOLsNL5bC-DHRo3UkjvChvg", "UCy7NVLcZfAu0_trdf-RVzUw", "UCJH1AAMIoDqp0Fp9MDfYO4g",
            "UCLhmehsjp86fVEfVj5PiT7A", "UCBByZNXMUzz-0qrLwMk9bYg", "UCCfuUsRqZcIAkq-9YEg2e2w",
            "UC8sD3GQrTbJTMMp_NU9sdag", "UCIRjbgsjh_iu_vSl9dtwIDg", "UCG-Gza8DUZOTGVp1ZYqKqjQ",
            "UCqfxtogFDBa6QzsuhG9mFbw", "UCgY9jsdQQa0DkCx07cGR8yA", "UCA54HCOWOdw7uZgMy3XJg4Q",
            "UCxup3fupRQvocZixof9Y7Vg", "UCatxW9eXbvzkCTgySV-Pkmg", "UCsh5TdVoO51_DjGyCFIhZsg",
            "UC_Xwjtx2RaFFgSsTHKoNJZw", "UCH5eXZroElnUOU1OzDJ5kpA", "UCPXfv8dD8nb1wMrODHBUiCQ",
            "UC9kKbLwjNc77YtDXST2dQoA", "UCFohkT_899sWXxwF8XS9vrg", "UCycjmrRpDoLY0p_rHeLDCRw",
            "UCko4y6fHRBhMhi0K-yJkRtA", "UCZMUB-dbevPjtPKyYkdMBHw", "UCM-3e8i702nLqVGNTblCNBg",
            "UCNiFJB7rnZvFkFalFVvuTpg", "UC1OJqJdDeGywaN_TttPlG4A", "UChPsCwzLIghlUKodG5zijfA",
            "UClCoOKHdiUZJ3sBV3Wj0n-w", "UC2-DHbDj_X6oUR4brWm9sIg", "UCOS4OtvY59wq6kHIdIJVMkg",
            "UCZOl5e0tSXhBXIDBaNw5olg", "UCgBPVgZ1E-YvjWv3REWN8cQ", "UCJU4Xqsjk_yOJ8Zzk71s9YA",
            "UCcEY6zn99AdeaZyVQzdnTjQ"]


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


def getVideoInfo(videoId, mode="description"):
  ret = {}

  if mode == "isUnavailable":
    for vid in videoId:
      ret[vid] = True

  count = 0
  splits = ceil(len(videoId) / 50)

  for i in range(splits):
    videosToCheck = videoId[i * 50:(i + 1) * 50]
    response = api.get_video_by_id(video_id=videosToCheck, parts="snippet,status")

    for item in response.to_dict()["items"]:
      if mode == "description":
        ret[item["id"]] = item["snippet"]["description"]
        ret[item["id"]] += "\nTitle:{}".format(item["snippet"]["title"])
      elif mode == "isUnavailable":
        ret[item["id"]] = item["status"]["uploadStatus"] in ["rejected", "deleted"]
      elif mode == "snippet":
        ret[item["id"]] = item["snippet"]

    count += len(videosToCheck)
    print("Progress {}/{}".format(count, len(videoId)))

  return ret


def parseVideoInfos(videoInfos, channelName):
  ret = {}
  for id in videoInfos.keys():
    ret[id] = parsing.parseVideoInfo(videoInfos[id], channelName)

  return ret


def refreshChannel(channelId, channelName):
  playlistId = getUploadsPlaylist(channelId)
  playlistVideos = getPlaylistVideos(playlistId, count=None)

  videoInfo = getVideoInfo(playlistVideos)

  global videos
  parsedInfo = parseVideoInfos(videoInfo, channelName)
  beforeAttribs = utils.sumAttribs(videos)
  videos = {**videos, **parsedInfo}
  attribs = utils.sumAttribs(videos)
  print("{} attribute{}".format(attribs - beforeAttribs, utils.s(attribs - beforeAttribs)))
  utils.dbStatus(videos)

  return parsedInfo


def refreshChannels(justLast):
  deadVids = set(videos.keys())
  for i in range(len(channels) - 1 if justLast else 0, len(channels)):
    channel = channels[i]
    print("Channel {}/{}".format(i + 1, len(channels)))
    try:
      channelName = getChannelName(channel)
      print("Refreshing channel: {}".format(channelName))
    except Exception:
      print("ERROR: Cannot get the name of a channel at all, rest in pepperoni.")
      print("The victim is: {}".format(channel))
      print()
      continue

    deadVids -= set(refreshChannel(channel, channelName).keys())
    print()
  if not justLast:
    print("Marking {} videos as dead videos :(".format(len(deadVids)))
    videos["deadVids"] = sorted(list(deadVids))


def updateDatabase(justLast=False):
  ensureAPI()
  refreshChannels(justLast)
  db.save(videos)


def getVideoComment(videoId):
  response = api.get_comment_threads(video_id=videoId, order="relevance", count=100, limit=100)
  ret = []
  for comment in response.to_dict()["items"]:
    ret.append(comment["snippet"]["topLevelComment"]["snippet"]["textOriginal"].replace("\r\n", "\n").split("\n"))
  return ret


def findLyrics(videoId):
  ensureAPI()
  comments = getVideoComment(videoId)
  if utils.romkanAvail:
    return "\n".join(map(utils.toRomaji, max(comments, key=len)))
  else:
    print("WARNING: Romkan is not installed, keeping the gojuons as-is.")
    return "\n".join(max(comments, key=len))


def listUnavailVideos(playlistId):
  ensureAPI()
  print("Loading playlist")
  playlistVideos = getPlaylistVideos(playlistId)
  isUnavailable = getVideoInfo(playlistVideos, "isUnavailable")
  for videoId in playlistVideos:
    if isUnavailable[videoId]:
      print()
      print(videoId)
      listVideoInfo(videoId)


def listVideoInfo(videoId):
  if videoId in videos:
    if "Raw Description" in videos[videoId]:
      print("Raw Description:")
      print("\n".join(videos[videoId]["Raw Description"]))
      print("\n\n", end="")
      print("--- End of raw description ---")
      print("\n\n", end="")

    print("Extracted Infos:\n")
    for attrib in parsing.commonInfos:
      if attrib in videos[videoId]:
        value = videos[videoId][attrib]

        print("{}: {}".format(attrib, '\n'.join(value) if isinstance(value, list) else value))
  else:
    print("Error: Video id is not in the database :(")


def listMissingChannels(playlistId):
  ensureAPI()
  print("Loading playlist")
  playlistVideos = getPlaylistVideos(playlistId)
  missingVideos = [vid for vid in playlistVideos if vid not in videos]
  missingVideoInfos = getVideoInfo(missingVideos, "snippet")
  missingChannels = {}
  for video in missingVideos:
    missingChannel = missingVideoInfos[video]["channelTitle"]
    if missingChannel in missingChannels:
      missingChannels[missingChannel].append(video)
    else:
      missingChannels[missingChannel] = [video]

  missingChannels = sorted(list(missingChannels.items()), key=lambda x: len(x[1]), reverse=True)
  for i in range(len(missingChannels) - 1, -1, -1):
    channel = missingChannels[i]
    print(f"\n{missingVideoInfos[channel[1][0]]['channelId']} ({channel[0]}) with {len(channel[1])} entries:")
    for video in channel[1]:
      print(f"{video}: {missingVideoInfos[video]['title']}")


videos = db.load()
if __name__ == "__main__":
  # updateDatabase()
  pass
