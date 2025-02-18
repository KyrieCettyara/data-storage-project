import logging
import os
from dotenv import load_dotenv

def copy_log(source_file, destination_file):
    try:
        with open(source_file, 'r') as source:
            with open(destination_file, 'a') as destination:
                # Read the content of the source file and write it to the destination file
                destination.write(source.read())
    except Exception as e:
        print(f"An error occurred: {e}")



def add_log(task: str, timestamp: str):
    load_dotenv()

    DIR_TEMP_LOG = os.getenv("DIR_TEMP_LOG")
    logger = logging.getLogger(task)
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler = logging.FileHandler(f"{DIR_TEMP_LOG}/logs.log")
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    return logger