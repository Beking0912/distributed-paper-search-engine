# baidu_paper_spider

## 技术选型 scrapy vs requests+beautifulsoup
1. requests 和 beautifulsoup 都是库，scrapy 是框架；
2. scrapy 框架中可以加入requests 和 beautifulsoup；
3. scrapy 基于 twisted，性能是最大优势；
4. scrapy 方便扩展，提供了很多内置的功能；
5. scrapy 内置的 css 和 xpath selector 非常方便，beautifulsoup 最大的缺点就是慢。

## 深度优先和广度优先
深度优先（递归实现）
```python
def depth_tree(tree_node):
    if tree_node is not None:
        print (tree_node._data)
        if tree_node._left is not None:
            return depth_tree(tree_node._left)
        if tree_node._right is not None:
            return depth_tree(tree_node._right)
```

广度优先（队列实现）
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

## URL去重策略
1. 将访问过的URL保存到数据库中；
2. 将访问过的URL保存到set中，只需要O(1)的代价就可以查询URL；
3. URL经过md5等方法哈希后保存到set中；
4. 用bitmap方法将访问过的URL通过hash函数映射到某一位；
5. bloomfilter方法对bitmap进行改进，多重hash函数降低冲突。

## 字符串编码 encode decode
1. 计算机只能处理数字，文本转换为数字才能处理。计算机中8个bit作为一个字节，所以一个字节能表示最大的数字就是255；
2. ASCII(一个字节)编码就成为美国人的标准编码；
3. ASCII处理中文是不够的，中国制定了GB2312编码，用两个字节表示一个汉字；
4. unicode的出现将所有语言统一到一套编码里；
5. 乱码问题解决了，但是如果内容全是英文，unicode编码比ASCII需要多一倍的存储空间，同时如果传输需要多一倍的传输；
6. 可变长的编码utf-8的出现，把英文变长一个字节，汉字三个字节。特别生僻的变成4-6字节，如果传输大量的英文，utf-8作用就很明显了。

## scrapy
scrapy 是 Python 开发的一个快速高层次的屏幕抓取和web抓取框架，用于抓取web站点并从页面中提取结构化的数据。优点：高并发(底层是异步IO框架 时间循环+回调)。

[官方文档](https://docs.scrapy.org/en/latest/)

1. 下载：`pip install Scrapy`
2. 新建：`scrapy startproject namexxx`

## xpath 语法 res.xpath('').extract_first('')
1. xpath 使用路径表达式在xml和html中进行导航；
2. xpath 包含标准函数库；
3. xpath 是一个w3c的标准。

## 分布式爬虫的优点
1. 充分利用多机器的带宽加速爬取；
2. 充分利用多机的IP加速爬取速度。

## 单机爬虫 => 分布式爬虫 需要解决的问题
1. request 队列集中管理：scheduler 以队列形式存储在内存中，而其他服务器无法拿到当前服务器内存中的内容；
2. 去重集中管理。
解决方法：将 request 队列和去重 放到第三方组件中，采用 Redis(内存数据库，读取速度更快)。

## Redis
Redis 是 key-value 存储系统，数据存在内存中。

## Redis 数据类型
字符串 散列/哈希 列表 集合 可排序集合

## Scrapy-Redis 编写爬虫需要注意的点 
1. 继承 RedisSpider；
2. 所有 request 不再由本地 schedule 来完成，而是 Scrapy-Redis 的 schedule；
3. 需要 push 起始 url。

## session 和 cookie 的区别
1. cookie 以 key-value 形式存储

## 下载包失败时
1. `pip install wheel`
2. `pip install -r requirements.txt`

## 集成 Redis
## 集成 BloomFilter

## 爬虫的增量爬取
1. 如何快速发现新的数据
   1. 全量的爬虫仍然在继续
      1. 重新启动一个爬虫：一个负责全量抓取，一个负责增量抓取
      2. 采用优先级队列(利于维护)
   2. 爬虫已结束
      1. 爬虫已关闭
         1. 如何发现已经有新的URL待抓取，一旦有URL则需要脚本启动爬虫
      2. 爬虫等待：继续push URL
2. 如何解决已经抓取过的数据(scrapy 自带去重机制)
   1. 列表数据已经抓取过之后还要继续抓取
   2. 已经抓取过的条目是否还要继续抓取(涉及更新问题)

最优方案：修改 scrapy-redis 源码可以达到目的。

## 通过修改 scrapy-redis 完成增量爬取

## 爬虫的数据更新
会更新的字段：被引用量

## 搜索引擎需求
1. 高效
2. 零配置 完全免费
3. 能够简单通过json和http与搜索引擎交互
4. 搜索服务器稳定
5. 能够简单的将一台服务器扩展到上百台

## elasticsearch 介绍
1. 基于 Lucene 的搜索服务器
2. 提供了一个分布式多用户能力的全文搜索引擎
3. 基于 RESTful web 接口
4. 是用 Java 开发的，并作为 Apache 许可条款下的开放源码发布

## 关系数据搜索缺点
1. 无法打分 -> 无法排序
2. 无分布式
3. 无法解析搜索请求
4. 效率低
5. 分词

## elasticsearch 安装
1. 安装 elasticsearch-rtf
2. head 插件和 kibana 的安装

## 跨域配置
```
http.cors.enabled: true
http:cors.allow-origin: "*"
http.cors.allow-methods: OPTIONS, HEAD, GET, POST, PUT, DELETE
http.cors.allow-headers: "X-Requested-With, Content-Type, Content-Type, Content-Length, X-User"
```

## elasticsearch 概念
1. 集群：一个或多个节点组织在一起
2. 节点：一个节点是集群中的一个服务器，由一个名字来标识，默认是一个随机的漫画角色的名字
3. 分片：将索引划分为多份的能力，允许水平分割和扩展容量，多个分片响应请求，提高性能和吞吐量
4. 副本：创建分片的一份或多份的能力，在一个节点失败时其余节点可以顶上

## elasticsearch vs mysql
1. index(索引) => 数据库
2. type(类型) => 表
3. document(文档) => 行
4. fields => 列

## 倒排索引
倒排索引源于实际应用中需要根据属性的值来查找记录。这种索引表中的每一项都包括一个属性值和具有该属性值的各记录的地址。由于不是由记录来确定属性值，而是由属性值来确定记录的位置，因而称为倒排索引(inverted index)。带有倒排索引的文简称倒排文件(inverted file)。

## TF-IDF

## 倒排索引待解决问题
1. 大小写转换问题，如 python 和 PYTHON 应该为一个词
2. 词干抽取，looking 和 look 应该处理为一个词
3. 分词
4. 倒排索引文件过大，压缩编码

elasticsearch 可以全部完成以上问题。

## elasticsearch 基本的索引

## 映射(mapping)
映射：创建索引时，可以预先定义字段的类型以及相关属性。

es会根据 JSON 源数据的基础类型猜测你想要的字段映射。将输入的数据转变为可搜索的索引项。mapping 就是我妈自己定义的字段的数据类型，同时告诉 es 如何索引数据以及是否可以被搜索。

作用：会让索引建立的更加细致和完善。

## es 查询
1. 基本查询：使用 es 内置查询条件进行查询
2. 组合查询：把多个查询组合在一起进行复合查询
3. 过滤：查询同时通过 filter 条件在不影响打分的情况下筛选数据

## 编辑距离
编辑距离是一种字符串之间相似程度的计算方法。即两个字符串之间的编辑距离等于使一个字符串变成另一个字符串而进行的 插入/删除/替换/相邻字符串交换位置 进行操作的最少次数。

关于编辑距离的求法，普遍采用的是动态规划。

## 环境迁移
1. pip freeze > requirements.text
2. pip install -r requirement.txt

## 资料
[Elasticsearch中ik_max_word和 ik_smart的区别](https://blog.csdn.net/weixin_44062339/article/details/85006948)

[相关度评分背后的理论](https://www.elastic.co/guide/cn/elasticsearch/guide/current/scoring-theory.html)

[Elasticsearch搜索中文分词优化](https://www.jianshu.com/p/914f102bc174)

## Elasticsearch 中文搜索时遇到几个问题
1. 检索葡萄糖关键字，希望结果仅包含葡萄糖，不包含葡萄；检索葡萄，希望结果包含葡萄糖。
2. 搜索“RMB”时只会匹配到包含“RMB”关键词的内容，实际上，“RMB”和“人民币”是同义词，我们希望用户搜索“RMB”和“人民币”可以相互匹配，ES同义词怎么配置？
3. 用户搜索拼音: 如"baidu",或者拼音首字母"bd",怎么匹配到"百度"这个关键词,又如用户输入"摆渡"这个词也能匹配到"百度"关键词,中文拼音匹配怎么做到?
4. 怎么保证搜索关键词被正确分词,通常我们会采用自定义词典来做,那么怎么获取自定义词典?

## ik 分词器
1. ik_max_word：将文本做最细粒度的拆分，比如会将“中华人民共和国人民大会堂”拆分为“中华人民共和国、中华人民、中华、华人、人民共和国、人民、共和国、大会堂、大会、会堂等词语。
2. ik_smart：会做最粗粒度的拆分，比如会将“中华人民共和国人民大会堂”拆分为中华人民共和国、人民大会堂。

## 最佳实践
两种分词器使用的最佳实践是：索引时用ik_max_word，在搜索时用ik_smart。

即：索引时最大化的将文章内容分词，搜索时更精确的搜索到想要的结果。索引时，为了提供索引的覆盖范围，通常会采用ik_max_word分析器，会以最细粒度分词索引，搜索时为了提高搜索准确度，会采用ik_smart分析器，会以粗粒度分词。

## ES 分词流程之分析（analysis）和分析器（analyzer）
1. character filter 字符过滤器：在分词前处理字符串，去除HTML标记；
2. tokenizer 分词器：英文分词可以根据空格将单词分开，中文分词比较复杂，可以采用机器学习算法来分词；
3. token filters 表征过滤器：修改大小写，停用词，增加同义词，增加词等；
4. ES分词流程：character filter-->>tokenizer-->>token filters
5. 自定义analyzer
6. 分词mapping设置
```
"content": {
    "type": "string",
    "analyzer": "ik_max_word",
    "search_analyzer": "ik_smart"
}
```

## 同义词
## Suggest分词
suggest词需要对拼音前缀，全拼，中文进行前缀匹配，例如：“百度”一词，键入"baidu","bd","百"都必须匹配到，因此在索引的时候需要一词分多个分词器来索引保存，中文采用单字分词，拼音首字母和全拼需要自定义analyzer来索引。


