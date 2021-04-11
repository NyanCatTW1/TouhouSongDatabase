# -*- coding: utf-8 -*-

global commonInfos
commonInfos = ["Title", "Artist", "Vocal", "Arrangement", "Lyric",
               "Circle", "Album", "Release Date", "Translation", "Original artist",
               "Original source", "Remix", "Website", "Background Image", "Guitar",
               "Source", "Length", "Event", "Genre", "Character"]
seperators = ["：", ":", " - "]


def patchInfo(info):
  # sRvtSH1_H0w
  info = info.replace("Released Date", "Release Date")

  # l4GQYBI4DBM
  info = info.replace("track name", "Title").replace("arranged by", "Arrangement").replace("album", "Album")

  # uSgHhzcvHfM
  info = info.replace("Vo:", "Vocal:").replace("Arrange", "Arrangement")

  # _lA8C48FlDw
  info = info.replace("( ", "(").replace(" )", ")")

  # -OzNzdlsocw
  info = info.replace("Vocals", "Vocal").replace("Lyrics", "Lyric").replace("Artwork", "Illustration")

  # mVYKcTxKro0
  info = info.replace("Arranger", "Arrangement").replace("Remixed by", "Remix").replace("Picture source", "Illustration")

  # 6zG5hmr-RvY
  info = info.replace("Image", "Illustration").replace("background image", "Background Image").replace("歌詞／Lyric", "")

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
  info = info.replace("TITLE:", "Title:").replace("lyrics:", "Lyrics:").replace("Original title:", "Original:")

  # hRmrbi8wDb0
  info = info.replace("Vocals by:", "Vocal:").replace("Lyrics by:", "Lyrics:").replace("Arrangement by:", "Arrangement:")\
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

  return info


def stripKeyword(line, keyword):
  for seperator in seperators:
    if seperator in line:
      return seperator.join(line.split(seperator)[1:]).strip()

  return keyword.join(line.split(keyword)[1:]).strip()


def commonDetection(lines, keywords):
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
        ret[keyword] = stripKeyword(line, keyword)

  return ret


def detectMultiline(lines, keyword):
  ret = []
  begin = False
  for line in lines:
    if not begin:
      if keyword in line:
        begin = True
        ret.append(stripKeyword(line, keyword))
    elif len(line.strip()) > 0 and not any(sep in line for sep in seperators):
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
  lambda lines: commonDetection(lines, commonInfos),
  lambda lines: detectMultiline(lines, "Original"),
  lambda lines: illustrationParser(lines)
]


def parseVideoInfo(info):
  info = patchInfo(info).split("\n")

  ret = {}
  for parser in parsers:
    ret = ret | parser(info)

  return ret
