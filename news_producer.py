from typing import List
from kafka import KafkaProducer
import json
from alpaca_trade_api import REST
from alpaca_trade_api.common import URL
from alpaca.common import Sort

from alpaca_config.keys import config


def get_producer(brokers: List[str]):
    producer = KafkaProducer(
        bootstrap_servers = brokers,
        key_serializer = str.encode,
        value_serializer = lambda v: json.dumps(v).encode('utf-8'),
        api_version = (2, 0, 2)
    )
    return producer


def produce_historical_news(
        redpanda_client: KafkaProducer,
        start_date: str,
        end_date: str,
        symbols: List[str],
        topic: str
    ):
    key_id = config['key_id']
    secret_key = config['secret_key']
    base_url = config['base_url']

    api = REST(key_id=key_id, secret_key=secret_key, base_url=URL(base_url))

    for symbol in symbols:
        news = api.get_news(
            symbol=symbol,
            start=start_date,
            end=end_date,
            limit=5,
            sort=Sort.ASC,
            include_content=False,
        )

        print(news)

if __name__ == "__main__":
    produce_historical_news(
        get_producer(config['redpanda_brokers']),
        topic='market-news',
        start_date='2024-01-01',
        end_date='2024-09-10',
        symbols=['AAPL', 'Apple']
    )
