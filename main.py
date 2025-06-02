# main.py
import time
import schedule
from datetime import datetime
from config import settings as cfg
from src.api.client import BinanceClient
from src.core.indicators import calculate_technical_indicators
from src.core.signals import SignalDetector
from src.notification.wechat import WechatNotifier
from src.utils.logger import logger


class TradingSignalSystem:
    """交易信号系统主控制器"""

    def __init__(self):
        # 初始化组件
        self.client = BinanceClient(symbol=cfg.SYMBOL, interval=cfg.INTERVAL)
        self.signal_detector = SignalDetector(
            short_period=cfg.EMA_PERIOD_SHORT,
            long_period=cfg.EMA_PERIOD_LONG,
            rsi_period=cfg.RSI_PERIOD)
        self.notifier = WechatNotifier()

        # 状态变量
        self.last_buy_signal_time = 0
        self.last_sell_signal_time = 0

    def run_strategy(self):
        """执行完整的交易策略"""
        logger.info(">> 开始执行策略")

        try:
            # 1. 获取收盘价数据
            logger.info("获取收盘价序列...")
            closes = self.client.get_kline_data(cfg.SYMBOL,
                                                cfg.INTERVAL,
                                                limit=cfg.DATA_LIMIT).get(
                                                    'close', None)

            if closes is None or len(closes) < max(
                    cfg.EMA_PERIOD_SHORT, cfg.EMA_PERIOD_LONG, cfg.RSI_PERIOD):
                logger.warning("数据获取失败或不足，终止策略")
                return

            logger.info(f"获取到 {len(closes)} 条收盘价数据")

            # 2. 计算技术指标
            logger.info("计算技术指标...")
            indicators = calculate_technical_indicators(
                closes=closes,
                short_period=cfg.EMA_PERIOD_SHORT,
                long_period=cfg.EMA_PERIOD_LONG,
                rsi_period=cfg.RSI_PERIOD)

            if indicators is None:
                logger.warning("指标计算失败，终止策略")
                return


            # 3. 检测交易信号
            logger.info("检测交易信号...")
            signals = self.signal_detector.detect_signals(indicators)

            if signals is None:
                logger.info("未检测到有效信号")
                return

            logger.info(f"信号结果: 买入={signals['buy']}, 卖出={signals['sell']}")

            # 4. 处理信号
            current_time = time.time()

            if signals['buy'] and (current_time - self.last_buy_signal_time
                                   > cfg.SIGNAL_COOLDOWN):
                logger.info(f"发现买入信号! 强度: {signals['signal_strength']}/100")
                self.notifier.send_signal("BUY", indicators,
                                          signals['signal_strength'])
                self.last_buy_signal_time = current_time

            if signals['sell'] and (current_time - self.last_sell_signal_time
                                    > cfg.SIGNAL_COOLDOWN):
                logger.info(f"发现卖出信号! 强度: {signals['signal_strength']}/100")
                self.notifier.send_signal("SELL", indicators,
                                          signals['signal_strength'])
                self.last_sell_signal_time = current_time

        except Exception as e:
            logger.error(f"策略执行异常: {str(e)}")
        finally:
            logger.info("<< 策略执行完成\n")

    def start(self):
        """启动交易系统"""
        logger.info("========== 交易信号系统启动 ==========")
        logger.info(f"交易对: {cfg.SYMBOL}")
        logger.info(f"时间周期: {cfg.INTERVAL}")
        logger.info(f"冷却时间: {cfg.SIGNAL_COOLDOWN//60}分钟")

        # 立即运行一次
        self.run_strategy()

        # 设置定时任务
        schedule.every(15).minutes.do(self.run_strategy)

        # 主循环
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)
        except KeyboardInterrupt:
            logger.info("系统安全停止")


if __name__ == "__main__":
    system = TradingSignalSystem()
    system.start()
