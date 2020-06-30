# -*- coding: utf-8 -*-
import requests
import json
import os

clubId =  # Set your club id
folderName =  # Set folder name

mainUrl = "http://club.cyworld.com/club/board/PhotoViewer/index.asp?club_id=%d" % clubId

header = {
    "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
    "charset": "utf=8",
    "Referer": "http://club.cyworld.com/club/board/PhotoViewer/index.asp?club_id=%d" % clubId
}
session = requests.Session()

session.get("http://club.cyworld.com/club/board/PhotoViewer/index.asp?club_id=%d" % clubId)


def download_file(url, local_filename):
    image = session.get(url, stream=True)
    if not os.path.exists(local_filename):
        with open(local_filename, 'wb') as file:
            for chunk in image.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)
    return local_filename


if not os.path.exists(folderName):
    os.mkdir(folderName)

lastSeq = ""

while 1:
    response = session.get(
        "http://club.cyworld.com/CLUB/Board/PhotoViewer/GetPhotoListByDateJson.asp?lastseq=" + lastSeq + "&imgcount=30",
        headers=header)

    data = json.loads(response.text)

    if "msg" in data:
        break

    from collections import OrderedDict

    od = OrderedDict(sorted(data.items(), reverse=True))

    for d in od:
        for img in od[d]["items"]:
            date = img["writeDate"]  # 게시글 작성일자
            date = date.replace('-', '')
            title = img["title"].replace('?', '').replace('<', '(').replace('>', ')').replace('"', '\'')\
                .replace("/", "-").replace('*', 'o').replace(':', '').replace('&amp;', '&').replace('gt;', ')')\
                .replace('lt;', '(')  # 게시글 이름 (파일 이름 규칙에 맞게 수정)
            split = img["photoUrl"].split('%2E')  # 확장자 분리
            fileExt = split[1]

            fileName = os.path.join(folderName, date + u") " + title + u"-" + str(img["itemSeq"]) + "." + fileExt)

            print(download_file(img["photoUrl"], fileName))
            lastSeq = str(img["itemSeq"])
