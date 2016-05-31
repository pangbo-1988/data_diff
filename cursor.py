# This is cursor file with all the cursor operations
import hashlib
import time
import mmh3

class Cursor(object):
    def __init__(self, es, data_from):
        self.es = es
        self.data_from = data_from
        if not es.indices.exists(index="lookup"):
            self.setup_cursor_in_es()

    def first_cursor(self):
        first_cursor = {}
        first_cursor["key"] = []
        first_cursor["source"] = self.data_from
        first_cursor["version"] = []
        first_cursor["time"] = []
        return first_cursor

    def read_cursor(self):
        cursor_id = mmh3.hash(self.data_from)
        try:
            res = self.es.get(  index="lookup",
                                doc_type="data",
                                id=cursor_id)
            return res["_source"]
        except:
            return None

    def save_cursor(self, cursor_data):
        cursor_id = mmh3.hash(self.data_from)
        res = self.es.index(index="lookup", 
                            doc_type="data", 
                            id=cursor_id, 
                            body=cursor_data)
        return

    def get_new_cursor(self):

        # read cursor data
        cursor_data = self.read_cursor()
        if cursor_data is None:
            cursor_data = self.first_cursor()
        
        # set current data
        all_version = cursor_data["version"]
        version_num = len(all_version) + 1
        cursor_data["version"].append(version_num)
        localtime = time.localtime(time.time())
        cursor_data["time"].append( "%s-%s-%s" % (localtime.tm_year, localtime.tm_mon, localtime.tm_mday))
        key = hashlib.md5( str(cursor_data["source"]) + str(version_num)).hexdigest()
        cursor_data["key"].append(key)

        # save new cursor
        self.save_cursor(cursor_data)
        return version_num

    def list(self):
        res = self.es.search(index="lookup", 
                            doc_type="data", 
                            body={"query": { "match_all": {}}})
        print "key\t\t\t\t   source\t version\ttime"
        for hit in res["hits"]["hits"]:
            single_cursor =  hit["_source"]
            for i in range(len(single_cursor["version"])):
                key = hashlib.md5( str(single_cursor["source"]) + str(single_cursor["version"][i])).hexdigest()
                print "%15s %10s\t%5d\t\t%10s" % (key, single_cursor["source"], single_cursor["version"][i], single_cursor["time"][i])
        pass

    def search_by_key(self, key):
        res = self.es.search(   index="lookup",
                                doc_type="data",
                                body = {
                                    "query": {
                                        "match": {
                                            "key": key
                                        }
                                    }
                                })
        cursor = res["hits"]["hits"][0]["_source"]
        ret_source = cursor["source"]
        ret_version = 0
        for i in range(len(cursor["key"])):
            if cursor["key"][i] == key:
                ret_version = cursor["version"][i]
                break
        return (ret_source, ret_version)

    def setup_cursor_in_es(self):
        lookup_create_body = '''
        {
          "settings": {
            "index": {
              "store": {
                "type": "default"
              },
              "number_of_shards": 1,
              "number_of_replicas": 1
            },
            "analysis": {
              "analyzer": {
                "a0": {
                  "type": "english"
                }
              }
            }
          }
        }
        '''

        lookup_mapping_body = '''
        {
          "data": {
            "properties": {
              "key": {
                  "type": "string",
                  "store" : true,
                  "index" : "analyzed"
              },
              "source": {
                  "type": "string",
                  "store" : true,
                  "index" : "analyzed"
              },
              "version": {
                  "type": "integer",
                  "store" : true,
                  "index" : "analyzed"
              },
              "time": {
                  "type": "date",
                  "store" : true,
                  "index" : "analyzed"
              }
            }
          }
        }
        '''
        self.es.indices.create(index="lookup", body=lookup_create_body)
        self.es.indices.put_mapping(index="lookup", doc_type="data", body=lookup_mapping_body)


