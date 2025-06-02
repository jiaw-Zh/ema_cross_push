# src/notification/wechat.py
import requests
from datetime import datetime
from src.utils.logger import logger
from config.settings import SYMBOL, WECHAT_WEBHOOK_URL

class WechatNotifier:
    """企业微信通知器"""
    
    def __init__(self, webhook_url=WECHAT_WEBHOOK_URL):
        self.webhook_url = webhook_url
        self.session = requests.Session()
    
    def send_signal(self, signal_type, indicators, strength):
        """发送交易信号通知"""
        if indicators is None:
            logger.warning("无法发送消息：缺少必要数据")
            return False
            
        try:
            current_price = float(indicators['closes'][-1])
            ema_s = float(indicators['ema_short'][-1])
            ema_l = float(indicators['ema_long'][-1])
            rsi = float(indicators['rsi'][-1])
            
            if signal_type == "BUY":
                title = "🚀 买入信号"
            else:
                title = "🔻 卖出信号"
                
            content = f"**{title}**\n" \
                      f"> **交易对**: `{SYMBOL}`\n" \
                      f"> **当前价**: ${current_price:.2f}\n" \
                      f"> **EMA快/慢**: {ema_s:.2f}/{ema_l:.2f}\n" \
                      f"> **RSI**: {rsi:.2f}\n" \
                      f"> **信号强度**: {strength}/100\n" \
                      f"> **时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                      
            payload = {
                "touser": "@all",  # 发送给所有人
                "msgtype": "markdown",
                "markdown": {"content": content}
            }
            
            response = self.session.post(
                self.webhook_url, 
                json=payload, 
                timeout=5
            )
            
            if response.status_code == 200:
                logger.info(f"{signal_type}信号已发送")
                return True
            else:
                logger.warning(f"发送失败: HTTP {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"通知发送失败: {str(e)}")
            return False