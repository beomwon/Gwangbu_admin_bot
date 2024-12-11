import dotenv, os

dotenv.load_dotenv()

BOT_APPLICATION_ID  = os.getenv('BOT_APPLICATION_ID')
BOT_PUBLIC_KEY = os.getenv('BOT_PUBLIC_KEY')
BOT_TOKEN = os.getenv('BOT_TOKEN')