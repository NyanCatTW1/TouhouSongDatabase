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
            "UCcEY6zn99AdeaZyVQzdnTjQ", "UCOxvBvlRGKjf0ZWfVEdneKA", "UCmzieQGdu7fTXaPqi2AuXyg",
            "UCXPZV8w2XFt7AB-09Vv6HRA", "UCluuXfMJnQNP-kVVUiSJFjA", "UCOYm_W5mJpuGiXP1Js5iWKg",
            "UCK3dyS7DXjL2DkdoY2S14qA", "UCTkYivm5YbMEgKxBkVcFMxA", "UCcWmtIyfqR1W1YM6s6mkJrg",
            "UCXjYACN9b8gFDjktdoM6Vsg", "UCw2dzq4tmOfmdlJ4BcqdB-g", "UC4eeT9Tk17WecKmB3IptMTw",
            "UCH8oqutMsRDNEhjHUEg1byQ", "UC1oG3SdlNPj_WrokDgtpljQ", "UCs4mPLlKyNtcy9D5re7SiAg",
            "UCCvXKzGv2_ty6w63HlzRpXg", "UCDIynh-WsLUBvXPsuTanAyA", "UC12mhuWNxrKqfXp9gtuc9AQ",
            "UCifpQcwydJ29yy4SUIEze7A", "UCLFHojnludnHhDPD3Pd9D5w", "UC9w1XHM5bgcSjWkatRFALVQ",
            "UCXf7VjJBX-kdKirgPB75k-Q", "UCHYr4LIVJMQOhbASKEcEB4A", "UCobQWeFdIl30jL22LhgVlXw",
            "UCDtfZsfsS0051YaZZq7_Kvg", "UCZaFfDBBCqmYdfp6DJl0cRw", "UCliG2TPBFMc6zweohklZxFQ",
            "UClryipE7m83IsRzMZIFYZog", "UCwxJHsVS3AbmhtaHPiKL5LA", "UC41_taiskgxKxIahMh9tkDQ",
            "UClyS_I-vg5bDhVyNKiLMmRg", "UCWUscGy-Om5tF4Qzgqw5RkQ", "UCL2pzDHH5R4SBseer6LzZgQ",
            "UCH_OIt0LOq6tzMFCWPklzfA", "UCzeXtGfstqeyVlBarK5py6w", "UCTm6zEcFMSwg0YIHz_kHWUQ",
            "UCGYS2uHZDe7OrWMHGALyMBA", "UCYVjEJTsWwyVMj4PlNiqw-Q", "UCKED5Effuo4JBLMcCFz3f7A",
            "UC-4rnwopoXPfAxjGNne7Qdw", "UCJXLJItr-Df2kEzjw9zK9Zw", "UCePhgw937vNfaEsiOanRwrg",
            "UCBbTjim6kQjev2cINipTGqQ", "UCPbBNbVA__M26QNPcZpmEFw", "UC-5KkXAuPHXdH_INNLuUrzQ",
            "UCMuD7BbrFB37Bgz_WD-x3sg", "UC6KkUgqpzEawrar09X8I7Kg", "UCF986nFCHZOyAVAsDaws1aw",
            "UCAa6VsGtCS-Lp1rkI71D87w", "UCR42ReY4PBLQ_ikQEDLtkyA", "UC8JphMRO2l5YG4AOqORIWoQ",
            "UCxQoSFjwhkgiX4SB1KHJ3HA", "UCRlg4rOfcd9qNHl-b8Lo3mA", "UCdBld4m6Fmf-w_awu6z7uwg",
            "UC6YbCZ_7Tpu-vDMtLXuawUg", "UCOGH61XggnYbpi3L_8GG9AA", "UCXcyBpIiPEOHEIASwzXOCaQ",
            "UCOW6lZ4HIgDvf-7PKGZw_2Q", "UCbkVNxi7A8ML3XSjjzAjV4w", "UC7NPav4TGitQ3uaSSwdeAcg",
            "UCX32-dV-qPstLofHlFlXRJg", "UCgBbQxdGcWYp8j6R37TOP_w", "UCmy1plJtTEZTh9gfazDKmmA",
            "UCtqb6o4ZJtaiiYs8jWQv3KA", "UCReJoGphaRP9d14fHC6eu0g", "UCrDiWiURNUf79KyDXmozZGA",
            "UCpS6NLfH0oEeUcxBGBqFOag", "UC6A4DERfqf1L_Pn0fOcIwHQ", "UCcyiw_47etTV7P92tw7-alw",
            "UC3JYZ_oIMLGauc1yOAjfVgQ", "UCofqT4H0_QEMEJB0lGwaL_A", "UC63uMcsj1SrvY888zE1_jRw",
            "UCeh7_R0iecRMpZTCBOx19XQ", "UCP1F4RFaopR2jNLjnLQG3Gw", "UCh5Dxz2HEE-Iuwc1cHhtl7g",
            "UCJgxWX7TJV5quBr49d_MqIg", "UC14G5tdSndPhP47RTVgMXcg", "UC3ZeGZLTV6VaKh2yx1VRbAQ",
            "UC463VG2kjGikqlJRPzCCh2g", "UCK5WLZQn5GZO9odKd1oUAhQ", "UC1r9uqAI99qJfa2lj3usFSQ",
            "UCwFpvQ9GPigjxX2B8Jru0zQ", "UCXdi-J2w2f_wxjIBL9ZrbRw", "UC6HQbj-37w2Jow67wDVn_vg",
            "UC3VU58V9zwfgWqDoPt1s5AA", "UCIbh42ATHgD3ODWWyt7P7Xg", "UCVQr6MoZCqQIwTl1TwpKnTA",
            "UCiPe1meneF3eVCZbMiMtc1g", "UC2WQonFKaZC2i5-_wPYSGYg", "UCeygl8F6T5k9q7MmdY9X65w",
            "UC4OmX_nlQRwJPj4y3UYkN1g", "UCs9oFe-kzczjIecbYcfN-bw", "UCEGwLdIdeCIjHnVERq746Gw",
            "UCUG7Z3ozKOZzcCqMh_A1O-w", "UCLOsEGB9duVUZv8q3PaI_2Q", "UCiCYykHUOUjJkFlGI_i-DPQ",
            "UCLnTA9VdFeIT0QSTHfIQGNw", "UCrWU3gAVf9Fym_FubxVTw0Q", "UCa189ED1RFOLfR-R0zAOAkg",
            "UCzopDs3umvneOr451NF7nSw", "UCqTyUF9P4Vk3ay8IAeo8c0w", "UCD7oZ0qW7fqjoBRJG0cCUsg",
            "UCSd7ccLUkv6qcn87V_Kt1jg", "UCmZcxSP36QJUwIbvSvHdwfA", "UC5DECrDVnJ-QpRT4NzSYd-Q",
            "UC591n3CAjupKnHsiwSdoWBA", "UCAYiUxZMQDndWg-kimBA29w", "UCSr5v0JxAcxpSAf9chFWOjQ",
            "UCs6zEQqRBPhM73iA8EapfNg", "UCYswMnCSVAKg4cfIU4syiSA", "UCcCQvI0oKj5imADP7mJ0ZQg",
            "UCen4sbgvxLuBZAMtg_TQCxA", "UCifClZHixbW0vSictyLA7SQ", "UCBj8s04R5oBJuGfw7JJWs7g",
            "UCv3Jwi7q83fZOEnkUEZImmw", "UCoPvwNQwMw5NkXRYpbz7Pdw", "UCJz43jy4gRpS4oIaZaqJJ5Q",
            "UCyIIb5XcpLXXjnncIkDn66A", "UCLf5H3XCoPFZLfQC5Bs0wIQ", "UCAoOjtXrfbuJBAi_IZ7HKHA",
            "UCreek7glsOcf2N39KU5jqVw", "UCcnmMvyAC5JvTixmyhRkaDw", "UCVryTXmHWqjFn4kWTDhr6SQ",
            "UCHdlmPC9SSAPG235-LS40zg", "UCC6WApQ-zTtdRJzav_HjYtA", "UC_Bx6Wk4RT6rziVAbY8m2PQ",
            "UCSjsU1EClnUefsrEA22OFVw", "UCAivv9aNt0CkPdAOP1klo6w", "UCHdyugDq1itT-vXgh10m4og",
            "UCEa3dfRiraKzprddMukaR4g", "UColNv-n4PTIj92065IlVEHQ", "UC7c_LFgZMAZvAwvlSs3ELgg",
            "UCiWeDUcMkwZVXH6dSPFR52w", "UCZOU4fqAcTCcK8Qw3P7WADA", "UCRcdpNGSmZuDV8lkHUdBQ1g",
            "UCVySjaO3SrmyTWfos6uRp3w", "UCDiqn-ylh1wtPjX0PUE5QDw", "UCnA0zvPnznbO3VR59CK7CGA",
            "UCnntWYn5ZCOUzS4o16TFa5g", "UCWz82fO4huvZzbyQj2lx4AA", "UC7KQ8VFWSjHfFLF81DUfJMA",
            "UC_FwGXTh7fnS2EuDCtG6M3g", "UCMw08t4waZniQ4knQxW7J9g", "UCAnMJr9tHnvRlWHS4AdJ_vQ",
            "UCMW6LPAo_8AjsQ0sXIC37dw", "UCowjNOBEk7l5zZd5jV92t_g", "UCMIeqmpXxRukOZcZkcfiXbw",
            "UC-GK-y1OSPYze1hFLlGn-RQ", "UCz9Lx_m6XjKLxdtpOb1lUEA", "UC9HL7Z1L6Y6AOtBbneq8xPw",
            "UCYXu1-TpwHiWLZL__xvEozQ", "UC6NdySmxURBpAe-R7eb7DRQ", "UCdhONd6VbXlOn_4WQmWNkUQ",
            "UCEjX8BAq9aOjcv5iWkTdqQA", "UCnV29g1yx68QBcYDwgw1r0g", "UCB8M-AYVYDdILQzxEZ4275w",
            "UCGFU3gA5U5Xnh-RFiuhGrhA", "UCDSwgKofPaI2VdNbwtVmQkw", "UCl1JtIGlroqe3QDKqdsZhAA",
            "UCPovzIif8nd2Pdf3uA5RLjw", "UCwQ4T2ek4cVteMIPdPBTetQ", "UC6f0cEEzUvNkWe0TEfX17ig",
            "UCln8cPlELXlF3OOtoh_OL2w", "UC_x7Tur1KRO9xv_BKtJdpWQ", "UCgXEKwmwxeAw9W9W-x60IRQ",
            "UCwatDtLh8_bi0PyWJwOAevg", "UCv8Jg3cB2_gG5cks2hp0dKA", "UC_9Zcjk97DOs7la67xAKk_g",
            "UCTuEKrpwGXKCA3xwCQLdU3g", "UCRhGAquCakhpCGtKejQBmzA", "UC6jNKaitSOC056LcIkYU03w",
            "UCeerukkGl5vcGLImVuu93pQ", "UCYbitrkXRXEdjrGddF9QzHw", "UCxBnDJ9lDONE8jtoWLkxP0A",
            "UCMQZsV95kBnwV3K8S081V8w", "UCyCpL5mXy4u-v4jgFXmeV2A", "UCcm6e4JxyDHZXI08T7eHfsg",
            "UCo_SResbauNJzb0r3mV6gzw", "UCQo-7lyQnDdGw7BBUp8GkSw", "UC3B2aF-PAZTVEK7QHyckFqg",
            "UCbfNO47deTMvTmOXpD4An1A", "UCwYaz87bqztuYppZOCbOcdg", "UC7BepxxYVhaO2-FwIewHfog",
            "UCpuj3e81wCrs5GnnusPwKCw", "UCIBbq-lHCQgNVEcaSFG0xEA", "UCJvBFPywyGag0DSDiU1mdYg",
            "UC7D8eGJ3qvhyZcmRXayILTw", "UCpUbaJ8ptuNscnoRuVpW19g", "UCK3hjbTeAfLzhhJG6dv_jKQ",
            "UCrOxGHS-Qpf_al0e7k8Ri9Q", "UCnD8BvElDV_qT77yluT0BIw", "UCBoa2RN-qkTdK_e6jfjfM6g",
            "UCmAHXT-xknqEkAsVMGUEwMw", "UCneFRe-GYie3SCKml2OYaPA", "UCCk2IHYtEEEcF1yhT3fSJ4g",
            "UCkj6LN8MHRGt0zDTnW_LG-Q", "UCWvQIAF-sKUXSd9Rhan5pcw", "UCbuo6sPQ-ZWU7lrF2O76Jqg",
            "UCmbGUsUceTr2Cz8m_7OjwMg", "UC5dgy2UFUqmVY7maEz3BrLg"]


def ensureAPI():
  global api
  try:
    api
    print("API key in place, continuing...")
  except NameError:
    api = Api(api_key=input("Please enter a valid YouTube API key: "))


def getPlaylistVideos(playlistId, count=None):
  ret = []

  try:
    response = api.get_playlist_items(playlist_id=playlistId, parts="contentDetails", count=count)
    for item in response.to_dict()["items"]:
      ret.append(item["contentDetails"]["videoId"])
  except Exception:
    print("Failed to get playlist videos, is the list empty?")

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
  foundUnavail = False
  for videoId in playlistVideos:
    if isUnavailable[videoId]:
      foundUnavail = True
      print()
      print(videoId)
      listVideoInfo(videoId)

  if not foundUnavail:
    print("No unavailable video :)")


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
    try:
      missingChannel = missingVideoInfos[video]["channelTitle"]
      if missingChannel in missingChannels:
        missingChannels[missingChannel].append(video)
      else:
        missingChannels[missingChannel] = [video]
    except Exception:
      # We hit an unavilable video
      pass

  missingChannels = sorted(list(missingChannels.items()), key=lambda x: len(x[1]), reverse=True)
  for i in range(len(missingChannels) - 1, -1, -1):
    print(f"\n{i + 1}/{len(missingChannels)}")
    channel = missingChannels[i]
    print(f"{missingVideoInfos[channel[1][0]]['channelId']} ({channel[0]}) with {len(channel[1])} entries:")
    for video in channel[1]:
      print(f"{video}: {missingVideoInfos[video]['title']}")

  code = ""
  for i in range(len(missingChannels)):
    if i % 3 == 0:
      code += " " * 12
    code += f'"{missingVideoInfos[missingChannels[i][1][0]]["channelId"]}",'
    if i % 3 != 2:
      code += " "
    else:
      code += "\n"
  print(code)


videos = db.load()
if __name__ == "__main__":
  # updateDatabase()
  pass
