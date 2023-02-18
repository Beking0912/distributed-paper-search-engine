# Distributed Document Search Engine
This is an open-source project for a paper search engine, which includes a Scrapy-Redis distributed crawler, an Elasticsearch search engine, and a Django frontend. The project was designed to provide a platform for users to easily search and access research papers.

## Features
- Scrapy-Redis distributed crawler using CSS Selectors.
- Centralized deduplication with Redis for distribution.
- Text search engine implemented with ElasticSearch.
- Full-stack web application built using Django.

## Technology Stack
The main technology stack used in this project includes:
- Scrapy-Redis
- Elasticsearch
- Django
<br />
<br /> 

**👉👉👉 More technical details that help to understand my project as follows.**
[中文版本](https://github.com/Beking0912/Distributed-Document-Search-Engine/blob/master/README_zh.MD)

## Technical selection scrapy vs requests+beautifulsoup
1. Both requests and beautifulsoup are libraries, and scrapy is the framework;
2. Requests and beautifulsoup can be added to the scrapy framework;
3. Scrapy is based on twisted, performance is the biggest advantage;
4. Scrapy is convenient for expansion and provides many built-in functions;
5. The built-in css and xpath selector of scrapy is very convenient, and the biggest disadvantage of beautifulsoup is slow.

## Depth first and breadth first
Depth first (recursive implementation)
```python
def depth_tree(tree_node):
    if tree_node is not None:
        print (tree_node._data)
        if tree_node._left is not None:
            return depth_tree(tree_node._left)
        if tree_node._right is not None:
            return depth_tree(tree_node._right)
```

Breadth first (queue implementation)
```python
def level_queue(root):
    if root is None:
        return
    my_queue = []
    node = root
    my_queue.append(node)
    while my_queue:
        node = my_queue.pop(0)
        print (node.elem)
        if node.lchild is not None:
            my_queue.append(node.lchild)
        if node.rchild is not None:
            my_queue.append(node.rchild)
```

## URL deduplication strategy
1. Save the visited URL in the database;
2. Save the visited URL in the set, and query the URL only at the cost of O(1);
3. The URL is saved in the set after being hashed by md5 and other methods;
4. Use the bitmap method to map the visited URL to a certain bit through the hash function;
5. The bloomfilter method improves bitmap, and multiple hash functions reduce conflicts.

## String encoding encode decode
1. Computers can only process numbers, and text can only be processed by converting text to numbers. 8 bits in the computer are regarded as a byte, so the largest number that a byte can represent is 255;
2. ASCII (one byte) encoding has become the standard encoding for Americans;
3. ASCII is not enough to handle Chinese. China has developed GB2312 encoding, which uses two bytes to represent a Chinese character;
4. The emergence of unicode unifies all languages into a set of codes;
5. The garbled problem is solved, but if the content is all in English, unicode encoding requires twice the storage space than ASCII, and at the same time, if the transmission requires twice the transmission;
6. The emergence of variable-length encoding utf-8 has changed the length of English to one byte and Chinese characters to three bytes. Especially uncommon ones become 4-6 bytes. If a large amount of English is transmitted, the effect of utf-8 will be obvious.

## scrapy
scrapy is a fast and high-level screen scraping and web scraping framework developed by Python to scrape web sites and extract structured data from pages. Advantages: high concurrency (the bottom layer is asynchronous IO frame time loop + callback).
[Official document](https://docs.scrapy.org/en/latest/)

1. download：`pip install Scrapy`
2. new：`scrapy startproject namexxx`

## xpath syntax res.xpath('').extract_first('')
1. xpath uses path expressions to navigate in xml and html;
2. xpath contains standard function library;
3. xpath is a w3c standard.

## Advantages of distributed crawlers
1. Make full use of the bandwidth of multiple machines to accelerate crawling;
2. Make full use of the IP of multiple machines to accelerate the crawling speed.

## Stand-alone crawler => distributed crawlers problems that need to solve
1. Centralized management of request queue: The scheduler is stored in memory in the form of a queue, and other servers cannot get the contents of the current server's memory;
2. De-duplicate centralized management. Solution: Put the request queue and de-replay into third-party components, using Redis (memory database, faster reading speed).

## Redis
Redis is a key-value storage system, and data is stored in memory.

## Redis data type
String hash/hash list collection, sortable collection

## needs to pay attention to writing crawlers using Scrapy-Redis
1. Inherit RedisSpider;
2. All requests are no longer completed by the local schedule, but the schedule of Scrapy-Redis;
3. Need to push the starting url.

## The difference between session and cookie
1. Cookies are stored in the form of key-value

## When downloading the package fails
1. `pip install wheel`
2. `pip install -r requirements.txt`

## Integrate Redis
## Integrate BloomFilter

## Incremental crawling of crawlers
1. How to quickly discover new data
   1. The full amount of crawlers is still going on
      1. Restart a crawler: one is responsible for full crawling, and the other is responsible for incremental crawling
      2. Use priority queue (conducive to maintenance)
   2. Crawler is over
      1. Crawler is closed
         1. How to find that there is a new URL to be crawled, once there is a URL, a script is required to start the crawler
      2. Crawler waiting: continue to push URL
2. How to solve the data that has been crawled (scrapy comes with a deduplication mechanism)
   1. After the list data has been crawled, continue crawling
   2. Whether to continue crawling the items that have been crawled (involving update issues)
Optimal solution: Modify the scrapy-redis source code to achieve the goal.

## Complete incremental crawling by modifying scrapy-redis

## Crawler data update
Fields that will be updated: cited amount

## Search engine requirements
1. Efficient
2. Zero configuration is completely free
3. Able to interact with search engines simply through json and http
4. Search server is stable
5. Able to easily expand one server to hundreds

## Introduction to elasticsearch
1. Lucene-based search server
2. Provides a full-text search engine with distributed multi-user capabilities
3. Based on RESTful web interface
4. Developed in Java and released as open source under the terms of the Apache license

## Disadvantages of relational data search
1. Unable to score -> Unable to sort
2. No distributed
3. Unable to parse search request
4. low efficiency
5. Participle

## elasticsearch installation
1. Install elasticsearch-rtf
2. Installation of head plugin and kibana

## Cross-domain configuration
```
http.cors.enabled: true
http:cors.allow-origin: "*"
http.cors.allow-methods: OPTIONS, HEAD, GET, POST, PUT, DELETE
http.cors.allow-headers: "X-Requested-With, Content-Type, Content-Type, Content-Length, X-User"
```

## elasticsearch concept
1. Cluster: One or more nodes are organized together
2. Node: A node is a server in the cluster, identified by a name, the default is the name of a random comic character
3. Fragmentation: The ability to divide the index into multiple parts, allowing horizontal partitioning and capacity expansion, multiple shards responding to requests, improving performance and throughput
4. Replica: The ability to create one or more copies of a shard, and the rest of the nodes can be on top when one node fails


## elasticsearch vs mysql
1. index => database
2. type => table
3. document => line
4. fields => columns

## Inverted index
The inverted index comes from the need to find records based on the value of attributes in practical applications. Each item in this index table includes an attribute value and the address of each record with the attribute value. Since the attribute value is not determined by the record, but the position of the record is determined by the attribute value, it is called an inverted index. A text with an inverted index is referred to as an inverted file.

## TF-IDF

## Inverted index pending issues
1. Case conversion issues, such as python and PYTHON should be a word
2. Stemming, looking and look should be treated as one word
3. Participle
4. The inverted index file is too large, compression encoding
Elasticsearch can complete all of the above problems.

## elasticsearch basic index

## Mapping
Mapping: When creating an index, you can predefine the field type and related attributes.

ES will guess the field mapping you want based on the basic type of the JSON source data. Turn the entered data into searchable index items. Mapping is the data type of the field defined by my mother. It also tells es how to index the data and whether it can be searched.

Role: It will make the index creation more detailed and perfect.

## es query
1. Basic query: use es built-in query conditions to query
2. Combined query: Combine multiple queries together for compound query
3. Filtering: the query passes the filter condition to filter the data without affecting the scoring

## Edit distance
Edit distance is a calculation method of similarity between strings. That is, the edit distance between two character strings is equal to the minimum number of operations for insert/delete/replace/swap positions of adjacent character strings to make one character string become another character string.

Regarding the calculation of edit distance, dynamic programming is commonly used.

## Environment migration
1. pip freeze > requirements.text
2. pip install -r requirement.txt

## References
[Elasticsearch中ik_max_word和 ik_smart的区别](https://blog.csdn.net/weixin_44062339/article/details/85006948)

[相关度评分背后的理论](https://www.elastic.co/guide/cn/elasticsearch/guide/current/scoring-theory.html)

[Elasticsearch搜索中文分词优化](https://www.jianshu.com/p/914f102bc174)

## Several problems encountered in Elasticsearch Chinese search
1. Search for the glucose keyword, hope that the result contains only glucose, not grapes; search for grapes, hope that the result contains glucose.
2. Searching for "RMB" will only match the content that contains the keyword "RMB". In fact, "RMB" and "RMB" are synonyms. We hope that users can search for "RMB" and "RMB" to match each other. How to configure ES synonyms ?
3. User search pinyin: such as "baidu", or the first letter of pinyin "bd", how to match the keyword "百度", and if the user enters the word "摆渡", it can also match the keyword "Baidu", how does the Chinese pinyin match? Do it?
4. How to ensure that the search keywords are correctly segmented, usually we will use a custom dictionary to do it, so how to get a custom dictionary?

## ik tokenizer
1. ik_max_word: Split the text at the finest granularity, such as splitting the "Great Hall of the People of the People's Republic of China" into "People's Republic of China, Chinese People, Chinese, Chinese, People's Republic, People, Republic, Great Hall, Assembly, Words such as hall.
2. ik_smart: Will do the most coarse-grained split, such as splitting the "Great Hall of the People of the People's Republic of China" into the People's Republic of China and the Great Hall of the People.

## Best Practices
The best practice for the use of the two tokenizers is: use ik_max_word for indexing, and ik_smart for search.

That is: the content of the article is segmented to the maximum when indexing, and the desired result is more precise when searching. When indexing, in order to provide the coverage of the index, the ik_max_word analyzer is usually used, which will index with the most fine-grained word segmentation. In order to improve the search accuracy, the ik_smart analyzer will be used for coarse-grained word segmentation.

## ES word segmentation process analysis and analyzer
1. character filter: process the string before word segmentation and remove HTML tags;
2. tokenizer: English word segmentation can separate words according to spaces, Chinese word segmentation is more complicated, and machine learning algorithms can be used to segment words;
3. token filters characterize filters: modify capitalization, stop words, add synonyms, add words, etc.;
4. ES word segmentation process: character filter-->>tokenizer-->>token filters
5. Custom analyzer
6. Word segmentation mapping settings
```
"content": {
    "type": "string",
    "analyzer": "ik_max_word",
    "search_analyzer": "ik_smart"
}
```

## Synonym
## Suggest participle
Suggest words need to match the prefix of Pinyin, Quanpin, and Chinese. For example: "百度", type "baidu", "bd", "百" must be matched, so it needs to be divided into multiple words when indexing A word segmenter is used to index and save. Chinese uses single-character word segmentation. Pinyin first letter and Quanpin require a custom analyzer to index.

