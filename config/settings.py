# config/settings.py
import os

# 基础配置
SYMBOL = "FARTCOINUSDT"      # 交易对
INTERVAL = "15m"        # K线周期
DATA_LIMIT = 100        # 获取的K线数量
PRODUCT_TYPE= "USDT-FUTURES" # 产品类型
SIGNAL_COOLDOWN = 900  # 信号冷却时间(秒)

# 技术指标参数
EMA_PERIOD_SHORT = 10   # 短期EMA周期
EMA_PERIOD_LONG = 20    # 长期EMA周期
RSI_PERIOD = 14         # RSI周期
VOLUME_MULTIPLIER = 1.5 # 成交量放大倍数阈值

# github action 通知配置
WECHAT_WEBHOOK_URL = os.environ.get("WECHAT_WEBHOOK_URL")


# 日志配置
LOG_FILE = "trading_signal_monitor.log"
LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR, CRITICAL