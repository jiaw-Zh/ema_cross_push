# src/core/signals.py
from src.utils.logger import logger

class SignalDetector:
    """交易信号检测器"""
    
    def __init__(self, short_period, long_period, rsi_period):
        self.short_period = short_period
        self.long_period = long_period
        self.rsi_period = rsi_period
    
    def detect_cross(self, short, long):
        """检测EMA交叉信号（金叉/死叉）"""
        if len(short) < 2 or len(long) < 2:
            logger.warning("交叉检测数据不足")
            return None, None
        
        # 转换为标量值
        current_short = float(short[-1])
        current_long = float(long[-1])
        prev_short = float(short[-2])
        prev_long = float(long[-2])
        
        golden_cross = (prev_short <= prev_long) and (current_short > current_long)
        death_cross = (prev_short >= prev_long) and (current_short < current_long)
        
        return golden_cross, death_cross
    
    def detect_signals(self, indicators):
        """基于技术指标检测交易信号"""
        if indicators is None:
            return None
            
        try:
            # 确保所有数组长度一致
            min_length = min(
                len(indicators['closes']),
                len(indicators['ema_short']),
                len(indicators['ema_long']),
                len(indicators['rsi'])
            )
            if min_length < 2:
                logger.warning("有效数据点不足 (至少需要2个)")
                return None
                
            # 获取当前值
            current_close = float(indicators['closes'][-1])
            ema_s = float(indicators['ema_short'][-1])
            ema_l = float(indicators['ema_long'][-1])
            rsi_current = float(indicators['rsi'][-1])
            
            # 检测交叉信号
            golden_cross, death_cross = self.detect_cross(
                indicators['ema_short'], 
                indicators['ema_long']
            )
            
            # 生成交易信号
            buy_signal = False
            sell_signal = False
            signal_strength = 0
            
            if golden_cross and rsi_current > 50:
                buy_signal = True
                signal_strength = 60
                if rsi_current > 60:
                    signal_strength += 15
                if current_close > float(indicators['closes'][-2]):
                    signal_strength += 15
                    
            if death_cross and rsi_current < 50:
                sell_signal = True
                signal_strength = 60
                if rsi_current < 40:
                    signal_strength += 15
                if current_close < float(indicators['closes'][-2]):
                    signal_strength += 15
            
            return {
                'buy': buy_signal,
                'sell': sell_signal,
                'signal_strength': min(signal_strength, 100)
            }
            
        except Exception as e:
            logger.error(f"信号检测失败: {str(e)}")
            return None