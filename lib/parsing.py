# -*- coding: utf-8 -*-

global commonInfos
commonInfos = ["Title", "Channel", "Artist", "Vocal", "Arrangement",
               "Lyric", "Circle", "Album", "Release Date", "Translation",
               "Original artist", "Original source", "Remix", "Website", "Original",
               "Illustration", "Guitar", "Bass", "Drum", "Source",
               "Length", "Event", "Genre", "Character"]
seperators = ["：", ":", " - "]


def patchInfo(info):
  # sRvtSH1_H0w
  info = info.replace("Released Date", "Release Date")

  # l4GQYBI4DBM
  info = info.replace("track name", "Title").replace("arranged by", "Arrangement").replace("album:", "Album:")

  # uSgHhzcvHfM
  info = info.replace("Vo:", "Vocal:").replace("Arrange:", "Arrangement:").replace("Arrange：", "Arrangement：")

  # _lA8C48FlDw
  info = info.replace("( ", "(").replace(" )", ")")

  # -OzNzdlsocw
  info = info.replace("Vocals", "Vocal").replace("Lyrics", "Lyric").replace("Artwork", "Illustration")

  # mVYKcTxKro0
  info = info.replace("Arranger", "Arrangement").replace("Remixed by", "Remix").replace("Picture source", "Illustration")

  # 6zG5hmr-RvY
  info = info.replace("image", "Image").replace("Image", "Illustration").replace("歌詞／Lyric", "")

  # l_rBFAJo1e0
  info = info.replace("Song:", "Title:")

  # jTgYtkc4kgg
  info = info.replace("Song title", "Title").replace("Original song", "Original").replace("Translated by", "Translation")\
             .replace("HP:", "Website:")

  # l_rBFAJo1e0
  info = info.replace("Original theme:", "Original:")

  # yI-5_nAJNpI
  info = info.replace("title:", "Title:").replace("length:", "Length:").replace("arrangement:", "Arrangement:")\
             .replace("vocal:", "Vocal:").replace("original:", "Original:").replace("source:", "Source:")\
             .replace("PV:", "Illustration:")

  # XO3JH6NdyDQ
  info = info.replace("Released:", "Release Date:")

  # FyVXpCSjApg
  info = info.replace("Pic source:", "Illustration:").replace("original Title:", "")

  # Qu_OzBsgRcI
  info = info.replace("Album Genre:", "Genre:").replace("Illustration Source:", "Illustration:")

  # lCQ7WuYXIHg
  info = info.replace("TITLE:", "Title:").replace("lyrics:", "Lyric:").replace("Original title:", "Original:")

  # hRmrbi8wDb0
  info = info.replace("Vocals by:", "Vocal:").replace("Lyrics by:", "Lyric:").replace("Arrangement by:", "Arrangement:")\
             .replace("Album name:", "Album:").replace("Circle name:", "Circle:").replace("Original Song", "Original")\
             .replace("Picture by:", "Illustration:")

  # _Zjhu4OfY6s
  info = info.replace("Release:", "Release Date:")

  # Ko7KQi6O3uk
  info = info.replace("Sources:", "Source:").replace("Picture Artist", "Illustration")

  # Jn8V7rWKfzA
  info = info.replace("Illustration Credit:", "Illustration:")

  # rwZIRobKIic
  info = info.replace("Song Titel:", "Title:")

  # CURT6c73UZY
  info = info.replace("Illustration Source：", "Illustration：").replace("Original Title：", "Original：")

  # -56E9ABZmtY
  info = info.replace("Original theme:", "Original:").replace("Picture:", "Illustration:")

  # Ak8AFx3pWSA
  info = info.replace("Picture artist:", "Illustration:")

  # jq77hb2OVOs
  info = info.replace("Imagen de:", "Illustration:")

  # 0QtGIK1fS4k
  info = info.replace("Publisher：", "Circle：").replace("Album Genre：", "Genre：").replace("Picture Artist：", "Illustration：")

  # 4m5q-NMfYIE
  info = info.replace("circle:", "Circle:").replace("translation:", "Translation:")

  # y30xoRA25jM
  info = info.replace("Release event:", "Event:").replace("Pics:", "Illustration:")

  # jSjUwprO0ok
  info = info.replace("Site:", "Website:").replace("Illust:", "Illustration:")

  # T6rFlUUKumY
  info = info.replace("Illust：", "Illustration：").replace("Original Composer:", "").replace("Original Composer：", "")

  # R8keaV4EDp8
  info = info.replace("illustration：", "Illustration：")

  # 3FWwrKVc3Pc
  info = info.replace("Titre :", "Title :")

  return info


def stripKeyword(line, keyword):
  for seperator in seperators:
    if seperator in line:
      return seperator.join(line.split(seperator)[1:]).strip()

  return keyword.join(line.split(keyword)[1:]).strip()


def commonDetection(lines, keywords, channelName):
  ret = {}
  mengYueWorkaround = "這是" in lines[0]
  for i in range(len(lines)):
    line = lines[i]

    # eVyR48O26BA
    if "Track List" in line:
      return {}

    for keyword in keywords:
      if keyword not in ret and keyword in line:
        if mengYueWorkaround and i < 2:
          continue
        parsed = stripKeyword(line, keyword)
        if len(parsed) > 0:
          ret[keyword] = parsed

  return ret


def detectMultiline(lines, keyword):
  ret = []
  begin = False
  for line in lines:
    if not begin:
      if "Original" in line and any(sep in line for sep in seperators):
        begin = True
        ret.append(stripKeyword(line, keyword))
    elif len(line.strip()) > 0 and ((not any(sep in line for sep in seperators)) or "Original" in line):
      ret.append(line.strip())
    else:
      break
  return {keyword: ret} if len(ret) > 0 else {}


def illustrationParser(lines):
  ret = []
  for i in range(len(lines)):
    if "Illustration" in lines[i]:
      ret.append(stripKeyword(lines[i], "Illustration"))
      try:
        while "http" in lines[i + 1]:
          ret.append(lines[i + 1])
          i += 1
      except Exception:
        pass
      finally:
        break
  return {"Illustration": ret} if len(ret) > 0 else {}


parsers = [
  lambda lines, channelName: commonDetection(lines, commonInfos, channelName),
  lambda lines, channelName: detectMultiline(lines, "Original"),
  lambda lines, channelName: illustrationParser(lines),
  lambda lines, channelName: {"Channel": channelName, "Raw Description": lines}
]


def parseVideoInfo(info, channelName):
  info = patchInfo(info).split("\n")

  ret = {}
  for parser in parsers:
    ret = {**ret, **parser(info, channelName)}

  return ret
