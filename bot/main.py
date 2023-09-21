import os
import sys

from dotenv import load_dotenv

load_dotenv()
python_path = os.getenv("PYTHON_PATH_FOR_BOT")

sys.path.extend(python_path.split(":"))


from bot.core.engine import StarNaviBot


if __name__ == "__main__":
    bot = StarNaviBot("config.json")
    bot.show_api_work()
