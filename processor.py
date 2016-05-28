from cursor import Cursor
from config import *
import sys
import json
import csv
import mmh3
import time


class CSVData(object):
    def __init__(self, data_file):
        self.data_file = data_file
    def read_data(self):
        data_json = []
        with open(self.data_file, 'r') as f:
            data_csv = csv.reader(f)
            for row in data_csv: 
                single_json = {}
                single_json["url_base"] = row[0]
                single_json["url_parameters"] = row[1]
                data_json.append(single_json)
        return data_json


class Processor(object):
    def __init__(self, es, data_file, data_from):
        self.es = es
        self.data_file = data_file
        self.data_from = data_from
        # setup deltab in elastic search
        if not self.es.indices.exists(index="deltadb"):
            self.setup_deltadb_in_es()

    # load data from data_file
    def load(self):
        if self.data_file.endswith('.json'):
            with open(self.data_file, 'r') as f:
                data_json = json.load(f)
            return data_json
        elif self.data_file.endswith('.csv'):
            csv_data = CSVData(self.data_file)
            return csv_data.read_data()
        else:
            print "not supported file format. Json and CSV only"
            return {}

    def update_node(self, node, cursor_num):
        localtime = time.localtime(time.time())
        node["updated"] = "%s-%s-%s" % (localtime.tm_year, localtime.tm_mon, localtime.tm_mday)
        if self.data_from not in node:
            node[self.data_from] = [cursor_num]
        if node[self.data_from][-1] < cursor_num:
            node[self.data_from].append(cursor_num)
        return node


    def create_node(self, each_data, cursor):
        # add new data
        new_node = {}
        new_node["url_base"] = each_data["url_base"]
        new_node["url_parameters"] = each_data["url_parameters"]
        new_node["http_header"] = ""
        # http_body is post body
        new_node["http_body"] = ""
        new_node["http_method"] = "GET"
        localtime = time.localtime(time.time())
        new_node["created"] = "%s-%s-%s" % (localtime.tm_year, localtime.tm_mon, localtime.tm_mday)
        new_node["updated"] = new_node["created"]
        new_node[self.data_from] = [cursor]
        # tag is used for form submission
        new_node["tag"] = ""
        return new_node


    # id is the hash value of base url
    def process(self):
        # load data
        data = self.load()
        # index to elastic search
        cursor = Cursor(self.es, self.data_from)
        cursor_num = cursor.get_new_cursor()
        for each_data in data:
            key_string = ''
            for each_key_string in key_value:
                key_string += each_data[each_key_string]
            hashkey = mmh3.hash(key_string)
            print "parsing id: ", hashkey
            # try to read record
            try:
                res = self.es.get(   index="deltadb", 
                                doc_type="data", 
                                id=hashkey)
                if res["found"]:
                    node = self.update_node(res["_source"], cursor_num)
                else:
                    node = self.create_node(each_data, cursor_num)
            except:
                node = self.create_node(each_data, cursor_num)
            # insert back to es
            try:
                res = self.es.index(index="deltadb", 
                                    doc_type="data", 
                                    id=hashkey, 
                                    body=node)
            except:
                continue

    def setup_deltadb_in_es(self):
        delta_create_body = '''
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

        delta_mapping_body = '''
        {
          "data": {
            "properties": {
              "url_base" : {
                  "type" : "string",
                  "store" : true,
                  "index" : "analyzed"
              },
              "url_parameters": {
                  "type": "string",
                  "store" : true,
                  "index" : "analyzed"
              },
              "http_method": {
                  "type": "string",
                  "store" : true,
                  "index" : "analyzed"
              },
              "http_headers": {
                  "type": "string",
                  "store" : true,
                  "index" : "analyzed"
              },
              "http_body": {
                  "type": "string",
                  "store" : true,
                  "index" : "analyzed"
              },
              "created": {
                  "type": "date",
                  "store" : true,
                  "index" : "not_analyzed"
              },
              "updated": {
                  "type": "date",
                  "store" : true,
                  "index" : "not_analyzed"
              },
              "tag": {
                  "type": "string",
                  "store" : true,
                  "index" : "analyzed"
              }
            }
          }
        }
        '''

        self.es.indices.create(index="deltadb", body=delta_create_body)
        self.es.indices.put_mapping(index="deltadb", doc_type="data", body=delta_mapping_body)


