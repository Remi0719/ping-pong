from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Constants
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY", "")
MODEL_NAME = "gpt-3.5-turbo"  # or your preferred model
MAX_TOKENS = 1000

# PPManager class
class PPManager:
    def __init__(self):
        self.history = []
    
    def add_ping(self, message):
        self.history.append({"role": "user", "content": message})
    
    def add_pong(self, message):
        self.history.append({"role": "assistant", "content": message})

# AlpacaChatPPManager class
class AlpacaChatPPManager(PPManager):
    def __init__(self):
        super().__init__()