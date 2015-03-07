#_*_ coding: utf-8 _*_
from .import torrentInfo
def insertTorrentInfo(object):
    torrent_info = torrentInfo.TorrentInfo(hashInfo=object.hashInfo)
    torrent_info.save()

def updateTorrentInfoByHashInfo(object):
    torrent_info = torrentInfo.TorrentInfo(hashInfo=object.hashInfo)
    torrent_info.name = object.name
    torrent_info.creation_date = object.creation_date
    torrent_info.file_list = object.file_list
    torrent_info.tracker_url = object.tracker_url
    torrent_info.hotCount = 1
    torrent_info.save()

def updateTorrentInfoHotCount(object):
    torrent_info = torrentInfo.TorrentInfo(hashInfo=object.hashInfo)



