# src/api/client.py
import requests
import numpy as np
from src.utils.logger import logger


class BinanceClient:
    """Binance API客户端封装"""

    def __init__(self, symbol, interval):
        self.symbol = symbol
        self.interval = interval
        self.session = requests.Session()

    def get_kline_data(self, symbol, interval, limit=100):
        """从币安API获取K线数据"""
        try:
            url = f"https://fapi.binance.com/fapi/v1/klines?symbol={symbol}&interval={interval}&limit={limit}"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()

            # 提取开盘价、最高价、最低价、收盘价、成交量
            opens = [float(d[1]) for d in data]
            highs = [float(d[2]) for d in data]
            lows = [float(d[3]) for d in data]
            closes = [float(d[4]) for d in data]
            timestamps = [d[0] for d in data]

            return {
                'open': np.array(opens, dtype=np.float64),
                'high': np.array(highs, dtype=np.float64),
                'low': np.array(lows, dtype=np.float64),
                'close': np.array(closes, dtype=np.float64),
                'timestamp': timestamps
            }
        except Exception as e:
            logger.error(f"获取K线数据失败: {e}")
            return None

