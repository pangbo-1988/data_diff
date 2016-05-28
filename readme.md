# delta
This tool is able to show the difference of multiple data sets.

---
## Particular Use case:
Track the changes of a website.  

User first crawls a website using given webcrawler or any other crawling methods.  
Save the results in json format, then process the results with this tool.  

After the website is updated with new url and features.
User crawl the website again, and process the results in the same way.

Then this tool is able to show the changes of the website by checking the difference of each data pair.  

---

### Example commands for comparing two data sets:

`python delta.py -p examples/simple_data_set1.json mytestdata`  
`python delta.py -p examples/simple_data_set2.json mytestdata`  

`python delta.py -l`  
```
key                              source        version     time   
6b00c11eff167ff6363e6bff04700a72 mytestdata       1       2016-xx-xx  
ee2f75941d7cef41113df1a8b7166cd9 mytestdata       2       2016-xx-xx  
```

`python delta.py -o 6b00c11eff167ff6363e6bff04700a72 ee2f75941d7cef41113df1a8b7166cd9`  

```
This shows the overlap of data_set1 and data_set2  
```

`python delta.py -m 6b00c11eff167ff6363e6bff04700a72 ee2f75941d7cef41113df1a8b7166cd9`  

```
This shows the values in data_set1 but not in data_set2
( The order of the key matters )
```

`python delta.py -c 6b00c11eff167ff6363e6bff04700a72 ee2f75941d7cef41113df1a8b7166cd9`  

```
This shows all the value in either data_set1 or data_set2  
```

### Example website tracking command line:
Setup a test DVWA server, assume the IP address is `192.168.57.30`  

Then crawl the website:  
`scrapy crawl dvwa_login -o dvwa_scanned_origin.json -t json`

Now let's change the website, by adding a new url into any exist page  
`http://192.168.57.30/newurl.php`  

Then we crawl the website again:  
`scrapy crawl dvwa_login -o dvwa_scanned_updated_add_newurl.json -t json`

We process the results into our program.

`python delta.py -p examples/dvwa_scanned_origin.json dvwa`  
`python delta.py -p examples/dvwa_scanned_updated_add_newurl.json dvwa`  

`python delta.py -l`
```
key                              source        version     time 
9861669f702eafe46e6914b4c4d58030 dvwa             1       2016-xx-xx
fece3c53b81ceab8397be5ef12ab22da dvwa             2       2016-xx-xx
```

`python delta.py -m fece3c53b81ceab8397be5ef12ab22da 9861669f702eafe46e6914b4c4d58030`
```
The results will show the new added url link  
http://192.168.57.30/newurl.php  
```

---

## Installation  
* Elastic Search 1.7.2
* Python 2.7  
  * pip install elasticsearch (2.2.0)
  * pip install Scrapy (1.0.6)
  * pip install mmh3 (2.3.1)
  * pip install urllib3 (1.14)

( The versions listed pass the tests. Other versions need more investigation. )

## Config Settings
##### delta.py
Set Elastic Search IP address and port in `delta/config.py`

Key value:
The key value in the json data determines whether two data are same.
The default values are 'url_base' and 'url_parameters', and can be configed in `delta/config.py`.


##### webcrawler
Set website login url, username and password in  
`webcrawler/webcrawler/spiders/dvwa_spider.py`  
Visit [scrapy tutorial](http://doc.scrapy.org/en/latest/intro/tutorial.html) for more info about crawling a website.  


## Unique index name in Elastic Search  
We use index names 'lookup' and 'deltadb' for data storage in Elastic Search  
The index names should be unique in Elastic Search.  
If not, there may be problems when processing data.

---

## Usage
```
Usage: delta.py [options]  

Options:
  -h, --help            show this help message and exit  
  -l, --list            list all available data sets  
  -p FILE data_source, --process=FILE data_source  
                        process file into data base  
  -o [HASH 1] [HASH 2], --diff-overlap=[HASH 1] [HASH 2]  
                        find the overlap of 2 data sets  
  -m [HASH 1] [HASH 2], --diff-minus=[HASH 1] [HASH 2]  
                        find the data in data set 1 but excluded from data set
                        2  
  -c [HASH 1] [HASH 2], --diff-combine=[HASH 1] [HASH 2]  
                        find the combined data set from data set 1 and data
                        set 2  
```

## Version
version 1.0

-- First beta version.


## Code Quality ##

More tests will be released.

## Coding Style

Will format the coding style in the next version.


## Output format

Currently the output data is json format, as is same with Elastic Search output. This helps process data.


## Future upgrade plan

This program will allow more kinds of input format and be able to delete processed data.  


