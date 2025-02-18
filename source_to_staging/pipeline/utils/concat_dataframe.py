import pandas as pd
from dotenv import load_dotenv
import os

# Define root dir project
ROOT_DIR = os.getenv("DIR_ROOT_PROJECT")

def concat_dataframes(df1, df2):
    
    concatenated_df = pd.concat([df1, df2], ignore_index=True)
    concatenated_df.to_csv(f'{ROOT_DIR}/pipeline_summary.csv', index = False)