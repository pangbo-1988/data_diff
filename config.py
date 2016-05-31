from elasticsearch import Elasticsearch

# Config elastic search IP and port here:
es = Elasticsearch("192.168.57.20:9200", timeout=600, max_retries=10, revival_delay=0)


# Set key values here. 
# The unique id of each data will be the hash value of key strings combination
# Example: key_value = ["key1", "key2"]
key_value = ["url_base", "url_parameters"]