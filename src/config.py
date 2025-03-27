import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Keys
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
HUGGINGFACE_API_KEY = os.getenv('HUGGINGFACE_API_KEY')

# Database Configuration
CHROMA_DB_HOST = os.getenv('CHROMA_DB_HOST', 'localhost')
CHROMA_DB_PORT = int(os.getenv('CHROMA_DB_PORT', '8000'))

# Application Settings
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')

# Model Settings
MODEL_NAME = os.getenv('MODEL_NAME', 'gpt-3.5-turbo')
MAX_TOKENS = int(os.getenv('MAX_TOKENS', '2000')) 