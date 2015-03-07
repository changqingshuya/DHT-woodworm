# _*_ coding: utf-8 _*_
'''
    https://zoink.it
'''

import urllib,urllib2,os,MySQLdb,gzip
from io import BytesIO
from btdht import Parser
from db.torrentInfo import TorrentInfo
from torrentparse import parse_torrent_file
import datetime


def save(filename, content):

    try:
        file = open(filename, 'wb')
        file.write(content)
        file.close()
    except IOError,e:
        print e

            

def getTorrents(info_hash):


    url="https://zoink.it/torrent/%s.torrent"%info_hash.upper()
    #url="http://torrage.com/torrent/%s.torrent"%info_hash.upper()
    #print url
    
    try:
        torrent=urllib2.urlopen(url,timeout=30)
        buffer = BytesIO(torrent.read())
        gz = gzip.GzipFile(fileobj=buffer)
        raw_data=gz.read()
        save(".\\torrents\\"+info_hash+".torrent",raw_data)
    except IOError,e:
        print e
        #print "downloading+"+info_hash+".torrent failed"
        return False
    #print "downloading+"+info_hash+".torrent success"
    return True

def getAllTorrents():

    try:
        os.mkdir("torrents")
    except Exception,e:
        print e

    try:
        from mongoengine import connect
        from pymongo import ReadPreference
        connect('torrentinfo-db', host='127.0.0.1:27001', replicaSet='rs', read_preference=ReadPreference.SECONDARY)
        #connect('torrentinfo-db')
        #conn=MySQLdb.connect(host='127.0.0.1',user='root',passwd='mysql',port=3306,charset="UTF8")
        #cur=conn.cursor()
        #conn.select_db('dht')
        #sql="select * from "+table + " where hash_info.info = ''"
        #count=cur.execute(sql)
        #print "thers are %s row in table"% count
        #result=cur.fetchall()
        result = TorrentInfo.objects(name=None,status=None)
        print len(result)
        i=0
        for r in result:
            try:
                #设置是否已经爬取过该资源
                r.status = 1
                r.save()
                #the torrent info is empty
                if r.name!=None and r.status != None:
                    print 'torrent exist'
                    continue

                #download the torrent file success
                print r.hashInfo
                state=getTorrents(r.hashInfo)

                if state:
                    #count the torrent file
                    i=i+1
                    try:
                        print ".\\torrents\\"+r.hashInfo+".torrent"
                        result = parse_torrent_file(".\\torrents\\"+r.hashInfo+".torrent")
                        print result['name']
                        print result['description']
                        print result['file_list']
                        print result['creation_date']
                        print result['tracker_url']
                        print result['client_name']
                    except Exception,e:
                        print 'bt file error'+e.message
                        r.save()
                        continue
                    name=result['name']
                    description = result['description']
                    file_list = str(result['file_list'])
                    files = ""
                    for f in result['file_list']:
                        print f[0]
                        files += str(f[0])
                    print files

                    creation_date = result['creation_date']
                    tracker_url = result['tracker_url']
                    client_name = result['client_name']
                    print r.hashInfo
                    encoding = result['encoding']
                    if encoding is not None:
                        try:
                            if name:
                                r.name = name.encode(encoding)
                            if description:
                                r.description = description.encode(encoding)
                            if file_list:
                                r.file_list = file_list
                            if creation_date:
                                r.creation_date = datetime.datetime.strptime(creation_date, "%Y-%m-%dT%H:%M:%S")
                            if tracker_url:
                                r.tracker_url = tracker_url.encode(encoding)
                            if client_name:
                                r.client_name = client_name.encode(encoding)
                            r.files = files
                            r.save()
                        except Exception,e:
                            print 'mongodb or decode error'+e.message
                            r.save()
                            continue
                    else:
                        try:
                            if name:
                                r.name = name
                            if description:
                                r.description = description
                            if file_list:
                                r.file_list = file_list
                            if creation_date:
                                r.creation_date = datetime.datetime.strptime(creation_date, "%Y-%m-%dT%H:%M:%S")
                            if tracker_url:
                                r.tracker_url = tracker_url
                            if client_name:
                                r.client_name = client_name
                            r.files = files
                            r.save()
                        except Exception,e:
                            print 'mongodb or decode error'+e.message
                            continue
                else:
                    print 'error'
            except Exception,e:
                    print 'error2'
        
    except Exception,e:
        print 'mongodb error : '+e.message

        
    print 'the torrent files :'+str(i)    
if __name__=="__main__":

    getAllTorrents()

    #info_hash="640FE84C613C17F663551D218689A64E8AEBEABE"
    #getTorrents(info_hash)

