from elasticsearch import Elasticsearch

es = Elasticsearch("192.168.57.20:9200", timeout=600, max_retries=10, revival_delay=0)

key_value = ["url_base", "url_parameters"]