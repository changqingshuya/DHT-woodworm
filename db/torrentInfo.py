#_*_ coding: utf-8 _*_
from mongoengine.document import Document
from mongoengine.fields import *
import time
class TorrentInfo(Document):
    name = StringField()
    creation_date = DateTimeField()
    file_list = StringField()
    tracker_url = StringField()
    client_name = StringField()
    hashInfo = StringField()
    hotCount = IntField()
    clickCount = IntField()
    current_date = DateTimeField()
    files = StringField()
    status = IntField()

#fileList = ['hello','haha']
#TorrentInfo(name='xizhongzi',creation_date="2014-07-15",file_list=fileList,tracker_url='url',client_name='client',hashInfo='hash',hotCount=12,clickCount=12).save()







