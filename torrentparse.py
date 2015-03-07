#-*- coding:utf-8 -*-
from btdht.torrentparser import TorrentParser,ParsingError


#parse torrent file
def parse_torrent_file(file):
    tp = TorrentParser.get_instance()
    try:
        tp.parse_torrent(str(file))
        encoding = tp.get_encoding()
        return {
            "name": tp.get_torrent_name(),
            "file_list": tp.get_files_details(),
            "creation_date": tp.get_creation_date(),
            "tracker_url": tp.get_tracker_url(),
            "client_name": tp.get_client_name(),
            # TODO how to get torrent description?
            "description": None,
            "encoding": encoding,
            "parse_result": 'ok'
        }
    except ParsingError:
        print "torrent file(%s) seems broken." % file
    except Exception,e:
        print "unexpected error raised." + e.message

    return {"parse_result": 'bad'}

if __name__ == "__main__":
    #parser=Parser.Parser('./torrents/0c833da486a2fd7b8b16166c3c08180a86433295.torrent')

    result = parse_torrent_file('./torrents/3f93ec9f0aed0159fec3ef6ddaf9fc58e51dbd93.torrent')
    if result['parse_result'] == 'ok':
        #done = True
        print result['name']
        print result['description']
        print result['file_list']
        print result['creation_date']
        print result['tracker_url']
        print result['client_name']
        print result['encoding']

    # print parser.getName()
    # print parser.getEncoding()

