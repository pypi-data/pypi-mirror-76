## scrapy_nc

### 安装

```
pip install scrapy_nc
```

### 使用

目前提供以下基础数据:

- scrapy_nc.item.BaseItem 基础 item
- scrapy_nc.pipelines.MongoPipeline 保存 数据到mongo pipeline
- scrapy_nc.middlewares.ProxyDownloaderMiddleware 代理下载器


### BaseItem

目前由以下三个 Field 是默认包含的

```

crawled_at = scrapy.Field()  # 爬虫时间, 不用设置，由mongodb pipeline 自动设置
unique_id = scrapy.Field()   # 资源唯一id（当前爬虫到 collection 中）
```

示例：

```

from scrapy_nc.item import BaseItem

class XiaoyusanItem(BaseItem):
    pass
```

### MongoPipeline

安装 pymongo

```
pip install pymongo
```

MongoPipeline 初始化会读取以下  mongodb 连接设置

```
MONGO_HOST = os.environ.get('CRAWLAB_MONGO_HOST')
MONGO_PORT = int(os.environ.get('CRAWLAB_MONGO_PORT', '27017'))
MONGO_DB = os.environ.get('CRAWLAB_MONGO_DB')
MONGO_USERNAME = os.environ.get('CRAWLAB_MONGO_USERNAME')
MONGO_PASSWORD = os.environ.get('CRAWLAB_MONGO_PASSWORD')
MONGO_AUTHSOURCE = os.environ.get('CRAWLAB_MONGO_AUTHSOURCE')
```

collection_name 是 spider 的 name

手动获取 mongodb collection 操作数据：

```
self.collection
```

获取任意的 colleciotn


```
from scrapy_nc.db import mongo_db
spider_collection = mongo_db.get_collection(name) if mongo_db else None # name 可以设置任何 collecton 的名称操作数据
```


保存数据逻辑：

1. unique_id 唯一索引，重复写入会覆盖更新
2. **数据有效期默认90天，如果需要永久存储，settings 中指定 DATA_TTL: -1,必须是 -1. 如果需要修改有效期， DATA_TTL 指定任意整数，单位 秒**


```
class ConsistencyEvaluationDrugsSpider(scrapy.Spider):
    name = 'spider_name'
    custom_settings = {
        'ITEM_PIPELINES': {
            'scrapy_nc.pipelines.ItemCheckPipeline': 100,
            'scrapy_nc.pipelines.MongoPipeline': 800
        },
    }
```

### FlowPipeline

安装 request


settings 配置

```
ITEM_PIPELINES = {
    'scrapy_nc.pipelines.FlowPipeline': 700,
}
```

在 spider 的 custom_settings 中配置

```
FLOW_URLS: str or slice

```

示例
```python
class NmpaDrugNewsSpider(scrapy.Spider):
    name = 'nmpa_drug_news'
    custom_settings = {
        'FLOW_URLS': f'{os.environ.get("MEDICAL_BASE_FLOW_HOST")}/medicalbase/flow/cfdaDrugNews',
    }

```


### ProxyDownloaderMiddleware

安装 requests

```
pip install requests
```

setting 配置

```
DOWNLOADER_MIDDLEWARES = {
        'scrapy_nc.middlewares.ProxyDownloaderMiddleware': 100,
        'scrapy_splash.SplashCookiesMiddleware': 723,
        'scrapy_splash.SplashMiddleware': 725,
        'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
}
```

如果也使用了 splash，ProxyDownloaderMiddleware 需要在它提供的 middlewares 之前执行。即，数值比它的要小。

公网服务地址 https://spider-proxy.nocode-tech.com
内网服务地址 http://spider-proxy-rest-svc.backend-base:21030

### 报警通知

安装 request


spider 继承 NotifierSpider
```
from scrapy_nc.spiders import NotifierSpider

class NotifyTestSpider(NotifierSpider):
    name = 'notify_test_spider'
```

默认在爬虫结束后如果有 0 个 item 就会报警,可以通过覆盖一下午方法修改默认行为
```

    # 方法会传入所有统计数据的dict, 含义同下面示例中的参数名称
    def notify(self, stats):
        return stats.get('item_scraped_count', 0) < 1

```
stats 内容， 默认不存在的数据 key 不存在， 读取使用 get(key, default_value) 形式避免报错
```
        #    {'downloader/exception_count': 1,
        #  'downloader/exception_type_count/twisted.internet.error.TimeoutError': 1,
        #  'downloader/request_bytes': 197438,
        #  'downloader/request_count': 510,
        #  'downloader/request_method_count/GET': 510,
        #  'downloader/response_bytes': 12368745,
        #  'downloader/response_count': 509,
        #  'downloader/response_status_count/200': 411,
        #  'downloader/response_status_count/301': 7,
        #  'downloader/response_status_count/302': 53,
        #  'downloader/response_status_count/404': 2,
        #  'downloader/response_status_count/429': 6,
        #  'downloader/response_status_count/500': 30,
        #  'dupefilter/filtered': 170,
        #  'elapsed_time_seconds': 267.276458,
        #  'finish_reason': 'finished',
        #  'finish_time': datetime.datetime(2020, 7, 17, 7, 34, 38, 810636),
        #  'httperror/response_ignored_count': 12,
        #  'httperror/response_ignored_status_count/404': 2,
        #  'httperror/response_ignored_status_count/500': 10,
        #  'item_scraped_count': 129,
        #  'log_count/ERROR': 10,
        #  'log_count/INFO': 10414,
        #  'log_count/WARNING': 107,
        #  'memusage/max': 134623232,
        #  'memusage/startup': 64512000,
        #  'request_depth_max': 1,
        #  'response_received_count': 422,
        #  'retry/count': 27,
        #  'retry/max_reached': 10,
        #  'retry/reason_count/429 Unknown Status': 6,
        #  'retry/reason_count/500 Internal Server Error': 20,
        #  'retry/reason_count/twisted.internet.error.TimeoutError': 1,
        #  'scheduler/dequeued': 510,
        #  'scheduler/dequeued/memory': 510,
        #  'scheduler/enqueued': 510,
        #  'scheduler/enqueued/memory': 510,
        #  'start_time': datetime.datetime(2020, 7, 17, 7, 30, 11, 534178)}
```


##本地开发

```
pip uninstall -y  scrapy_nc && python setup.py install
```
