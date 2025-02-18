from dotenv import load_dotenv
import os
import logging

load_dotenv()  # Load environment variables from .env

parent = os.getenv("DIR_ROOT_PROJECT")
DIR_TEMP_LOG = os.getenv("DIR_TEMP_LOG")

# Test if it works
print(os.getenv("DIR_TEMP_LOG"))

print(f"Does directory exist? {os.path.exists(parent)}")

logging.basicConfig(filename = f'{DIR_TEMP_LOG}/logs.log', 
                                level = logging.INFO, 
                                format = '%(asctime)s - %(levelname)s - %(message)s')
