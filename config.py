import os
from dotenv import load_dotenv

# 加载.env文件中的环境变量
load_dotenv()

# API密钥
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")

# 其他配置
DEFAULT_MODEL_SIZE = os.getenv("DEFAULT_MODEL_SIZE", "base")
DEFAULT_SAVE_DIR = os.getenv("DEFAULT_SAVE_DIR", "./data/saved_meetings")

# 检查必需的环境变量
if not TOGETHER_API_KEY and os.path.exists(".env.example") and not os.path.exists(".env"):
    print("警告: API密钥未设置。请复制.env.example为.env并设置您的API密钥。")