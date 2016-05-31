# This is query file with all the query operations
from elasticsearch import Elasticsearch
import mmh3
import time

class Query(object):
    def __init__(self, es):
        self.es = es


    def search_missing_field(self, field_name):
        res = self.es.search(   index="deltadb",
                                doc_type="data",
                                body = {
                                    "filter": {
                                        "missing": {
                                            "field": field_name
                                        }
                                    }
                                })
        return res


    def search_exist_field(self, field_name):
        res = self.es.search(   index="deltadb",
                                doc_type="data",
                                body = {
                                    "filter": {
                                        "exists": {
                                            "field": field_name
                                        }
                                    }
                                })
        return res


    def search_match_field(self, field_name, data):
        res = self.es.search(   index="deltadb",
                                doc_type="data",
                                body = {
                                    "query": {
                                        "match": {
                                            field_name: data
                                        }
                                    }
                                })
        return res


    def search_exist_field_a_and_b(self, field_name1, field_name2):
        res = self.es.search(   index="deltadb",
                                doc_type="data",
                                body = {
                                    "filter": {
                                        "and": [
                                            {
                                                "exists": {
                                                    "field": field_name1
                                                }
                                            },
                                            {
                                                "exists": {
                                                    "field": field_name2
                                                }
                                            }
                                        ]
                                    }
                                })
        return res


    def search_exist_field_a_or_b(self, field_name1, field_name2):
        res = self.es.search(   index="deltadb",
                                doc_type="data",
                                body = {
                                    "filter": {
                                        "or": [
                                            {
                                                "exists": {
                                                    "field": field_name1
                                                }
                                            },
                                            {
                                                "exist": {
                                                    "field": field_name2
                                                }
                                            }
                                        ]
                                    }
                                })
        return res


    def search_exist_field_a_missing_b(self, field_name1, field_name2):
        res = self.es.search(   index="deltadb",
                                doc_type="data",
                                body = {
                                    "filter": {
                                        "and": [
                                            {
                                                "exists": {
                                                    "field": field_name1
                                                }
                                            },
                                            {
                                                "missing": {
                                                    "field": field_name2
                                                }
                                            }
                                        ]
                                    }
                                })
        return res


    def search_match_field_value_a_and_b(self, field_name1, data1, field_name2, data2):
        res = self.es.search(   index="deltadb",
                                doc_type="data",
                                body = {
                                    "query": {
                                        "bool": {
                                            "must": [
                                                {
                                                    "match": {
                                                        field_name1: data1
                                                    }
                                                },
                                                {
                                                    "match": {
                                                        field_name2: data2
                                                    }
                                                }
                                            ]
                                        }
                                    }
                                })
        return res


    def search_match_field_value_a_or_b(self, field_name1, data1, field_name2, data2):
        res = self.es.search(   index="deltadb",
                                doc_type="data",
                                body = {
                                    "query": {
                                        "bool": {
                                            "should": [
                                                {
                                                    "match": {
                                                        field_name1: data1
                                                    }
                                                },
                                                {
                                                    "match": {
                                                        field_name2: data2
                                                    }
                                                }
                                            ],
                                            "minimum_number_should_match": 1
                                        }
                                    }
                                })
        return res


    def search_match_field_value_a_not_b(self, field_name1, data1, field_name2, data2):
        res = self.es.search(   index="deltadb",
                                doc_type="data",
                                body = {
                                    "query": {
                                        "bool": {
                                            "must": [
                                                {
                                                    "match": {
                                                        field_name1: data1
                                                    }
                                                }
                                            ],
                                            "must_not": [
                                                {
                                                    "match": {
                                                        field_name2: data2
                                                    }
                                                }
                                            ]
                                        }
                                    }
                                })
        return res


    def search_match_and_exist_field(self, field_name1, data1, field_name2):
        res = self.es.search(   index="deltadb",
                                doc_type="data",
                                body = {
                                    "query": {
                                        "filtered": {
                                           "query": {
                                               "match": {
                                                    field_name1: data1
                                               }
                                           },
                                           "filter": {
                                               "exists": {
                                                    "field": field_name2
                                               }
                                           }
                                        }
                                    }
                                })
        return res


    def search_three_exist_fields(self, field_name1, field_name2, field_name3):
        res = self.es.search(   index="deltadb",
                                doc_type="data",
                                body = {
                                    "filter": {
                                        "and": [
                                            {
                                                "exists": {
                                                    "field": field_name1
                                                }
                                            },
                                            {
                                                "exists": {
                                                    "field": field_name2
                                                }
                                            },
                                            {
                                                "exists": {
                                                    "field": field_name3
                                                }
                                            }
                                        ]
                                    }
                                })
        return res


    def search_two_match_one_exist_field(self, field_name1, data1, field_name2, data2, field_name3):
        res = self.es.search(   index="deltadb",
                                doc_type="data",
                                body = {
                                    "query": {
                                        "filtered": {
                                           "query": {
                                               "bool": {
                                                   "must": [
                                                      {
                                                          "match": {
                                                             field_name1: data1
                                                          }
                                                      },
                                                      {
                                                          "match": {
                                                             field_name2: data2
                                                          }
                                                      }
                                                   ]
                                               }
                                           },
                                           "filter": {
                                               "exists": {
                                                  "field": field_name3
                                               }
                                           }
                                        }
                                    }
                                })
        return res


    def delete_all_data(self):
        try:
            res = self.es.indices.delete(index="deltadb")
            res = self.es.indices.delete(index="lookup")
            print "\nSuccessfully delete all the data."
            return True
        except:
            print "\nData not found"
            return False



