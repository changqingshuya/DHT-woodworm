# -*- coding: utf-8 -*-

import threading
import MySQLdb
import logging
import random
import bson
import time
from db.torrentInfo import TorrentInfo
'''
one hash_info conrresponds  many peers
'''
class HashTable(object):

    def __init__(self):
        self.hashes = {}
        #the mutex to access the critical resource
        self.lock = threading.Lock()

    def add_hash(self, hash):
        #利用with可以防止异常的问题
        with self.lock:
            if hash not in self.hashes:
                self.hashes[hash] = []
                logging.debug('inser a item into database')
                torrent_info = TorrentInfo.objects(hashInfo=hash.encode('hex'))
                if len(torrent_info) != 0:
                    torrent_info[0].hotCount = torrent_info[0].hotCount + 1
                    torrent_info[0].save()
                else:
                    TorrentInfo(hashInfo=hash.encode('hex'), hotCount=1,creation_date=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())),current_date=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))).save()
            else:
                torrent_info = TorrentInfo.objects(hashInfo=hash.encode('hex'))
                torrent_info[0].update(hotCount=torrent_info[0].hotCount + 1)

    def remove_hash(self, hash):
        with self.lock:
            if hash in self.hashes:
                del self.hashes[hash]

    #对某个资源添加一个peer
    def add_peer(self, hash, peer):
        with self.lock:
            if hash in self.hashes:
                if peer not in self.hashes[hash]:
                    self.hashes[hash].append(peer)

    #never remove any peer
    def remove_peer(self):
        return

    def count_hash_peers(self, hash):
        return len(self.hashes[hash])

    #获取某个hash值对应的所有peer值
    def get_hash_peers(self, hash):
        return self.hashes[hash]

    def count_hashes(self):
        return len(self.hashes)

    def get_hashes(self):
        return self.hashes

    def count_all_peers(self):
        tlen = 0
        for hash in self.hashes.keys():
            tlen += len(self.hashes[hash])
        return tlen

    def closeDataBase(self):
        try:
            self.cur.close()
            self.conn.close()
        except MySQLdb.Error,e:
            print 'mysql error %d:%s'%(e.args[0],e.args[1])


    def saveHashInfo(self,name):
        '''
        with open(name+"_hash_info.txt",'a') as file:
            for hash in self.hashes.keys():
                file.write(hash.encode('hex')+"\n\r")
        '''
        try:
            conn=MySQLdb.connect(host='127.0.0.1',user='root',passwd='mysql',port=3306,charset="UTF8")
            cur=conn.cursor()
            conn.select_db('dht')
            for hash in self.hashes.keys():
                hash_hex=(hash.encode('hex'))
                sql="insert into hash_info(hash,info) values('%s','%s')"%(hash_hex,"")
                try:
                    cur.execute(sql)
                    conn.commit()
                except MySQLdb.Error,e:
                    print 'mysql error %d:%s'%(e.args[0],e.args[1])
            cur.close()
            conn.close()
        except MySQLdb.Error,e:
            print 'mysql error %d:%s'%(e.args[0],e.args[1])
