# src/core/indicators.py
import talib
import numpy as np
from src.utils.logger import logger

def calculate_technical_indicators(closes, short_period, long_period, rsi_period):
    """基于收盘价序列计算技术指标"""
    if closes is None or len(closes) < max(short_period, long_period, rsi_period):
        logger.warning(f"数据不足 ({len(closes) if closes else 0}条), 无法计算指标")
        return None
    
    try:
        # 将列表转换为NumPy数组
        np_closes = np.array(closes)
        
        # EMA计算
        ema_short = talib.EMA(np_closes, timeperiod=short_period)
        ema_long = talib.EMA(np_closes, timeperiod=long_period)
        
        # RSI计算
        rsi = talib.RSI(np_closes, timeperiod=rsi_period)
        
        # 过滤NaN值
        valid_indices = ~np.isnan(ema_short) & ~np.isnan(ema_long) & ~np.isnan(rsi)
        valid_closes = np_closes[valid_indices]
        valid_ema_short = ema_short[valid_indices]
        valid_ema_long = ema_long[valid_indices]
        valid_rsi = rsi[valid_indices]
        
        return {
            'closes': valid_closes,
            'ema_short': valid_ema_short,
            'ema_long': valid_ema_long,
            'rsi': valid_rsi
        }
    except Exception as e:
        logger.error(f"指标计算失败: {str(e)}")
        return None