# -*- coding: utf-8 -*-

global commonInfos
commonInfos = ["Title", "Artist", "Vocal", "Arrangement", "Lyric", "Circle", "Album", "Release Date", "Illustration", "Translation", "Original artist", "Original source", "Remix", "Website", "Background Image", "Guitar"]
seperators = ["：", ":"]


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

    # sRvtSH1_H0w
    line = line.replace("Released Date", "Release Date")

    # l4GQYBI4DBM
    line = line.replace("track name", "Title").replace("arranged by", "Arrangement").replace("album", "Album")

    # uSgHhzcvHfM
    line = line.replace("Vo", "Vocal").replace("Arrange", "Arrangement")

    # _lA8C48FlDw
    line = line.replace("( ", "(").replace(" )", ")")

    # -OzNzdlsocw
    line = line.replace("Vocals", "Vocal").replace("Lyrics", "Lyric").replace("Artwork", "Illustration")

    # mVYKcTxKro0
    line = line.replace("Arranger", "Arrangement").replace("Remixed by", "Remix").replace("Picture source", "Illustration")

    # 6zG5hmr-RvY
    line = line.replace("Image", "Illustration").replace("background image", "Background Image").replace("歌詞／Lyric", "")

    # l_rBFAJo1e0
    line = line.replace("Song", "Title")

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
    elif len(line.strip()) > 0:
      ret.append(line.strip())
    else:
      break
  return {keyword: ret} if len(ret) > 0 else {}


parsers = [
  lambda lines: commonDetection(lines, commonInfos),
  lambda lines: detectMultiline(lines, "Original")
]


def parseVideoInfo(info):
  info = info.split("\n")

  ret = {}
  for parser in parsers:
    ret = ret | parser(info)

  return ret
