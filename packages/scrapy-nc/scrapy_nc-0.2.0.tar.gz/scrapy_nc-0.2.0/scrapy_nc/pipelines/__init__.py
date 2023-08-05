from .amqp_pipeline import AMQPPipeline
from .mongo_pipeline import MongoPipeline
from .item_check_pipeline import ItemCheckPipeline
from .request import RequestPipeline
from .flow_pipeline import FlowPipeline


ITEM_CHECK_PIPELINE = 'scrapy_nc.pipelines.ItemCheckPipeline'
AMQP_PIPELINE = 'scrapy_nc.pipelines.AMQPPipeline'
MONGO_PIPELINE = 'scrapy_nc.pipelines.MongoPipeline'
REQUEST_PIPELINE = 'scrapy_nc.pipelines.RequestPipeline'
FLOW_PIPELINE = 'scrapy_nc.pipelines.FlowPipeline'

DEFAULT_PIPELINES = {
    ITEM_CHECK_PIPELINE: 500,
    MONGO_PIPELINE: 700,
    REQUEST_PIPELINE: 760,
}
