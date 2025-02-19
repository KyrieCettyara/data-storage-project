
import luigi
import logging
import pandas as pd
import time
import traceback
import datetime
from pipeline.extract import Extract
from pipeline.utils.db_conn import db_connection
from sqlalchemy import text,inspect
import os

# Define DIR
DIR_ROOT_PROJECT = os.getenv("DIR_ROOT_PROJECT")
DIR_TEMP_LOG = os.getenv("DIR_TEMP_LOG")
DIR_TEMP_DATA = os.getenv("DIR_TEMP_DATA")
DIR_LOAD_QUERY = os.getenv("DIR_LOAD_QUERY")
DIR_LOG = os.getenv("DIR_LOG")

class Load(luigi.Task):

    # Define tables to be extracted from db sources
    tables_to_extract = ['address',
                        'address_status',
                        'author',
                        'book_author',
                        'book_language',
                        'book',
                        'country',
                        'cust_order',
                        'customer_address',
                        'customer',
                        'order_history',
                        'order_line',
                        'order_status',
                        'publisher',
                        'shipping_method']
    
    def requires(self):
        return Extract()
    
    def run(self):         
        # Configure logging
        logging.basicConfig(filename = f'{DIR_TEMP_LOG}/logs.log', 
                            level = logging.INFO, 
                            format = '%(asctime)s - %(levelname)s - %(message)s')
        
        

        logging.info("==================================STARTING TRUNCATE=======================================")
        # Define db connection engine
        _, trg_engine = db_connection()

        ##truncate data
        try:
            with trg_engine.connect() as conn:
               for index, table_name in enumerate(self.tables_to_extract):
                    ##for table in tables:
                    select_query = text(f"SELECT 1 FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = '{table_name}'")
                    result = conn.execute(select_query)


                    if result.scalar_one_or_none():
                       truncate_query = text(f"TRUNCATE public.{table_name} CASCADE")
                       
                       conn.execute(truncate_query)
                       conn.commit()
                       logging.info(f"TRUNCATE {table_name} - SUCCESS")
                    else:
                       logging.info(f"Table '{table_name}' does not exist, skipping truncate operation")
           
            logging.info("TRUNCATE ALL TABLES - DONE")
       
        except Exception as e:
           logging.error(f"TRUNCATE DATA - FAILED: {e}\n{traceback.format_exc()}")
           raise Exception("Failed to truncate data")
        logging.info("==================================END TRUNCATE=======================================")
        logging.info("==================================STARTING LOAD DATA=================================")

        try:
            start_time = time.time()
            dfs = []
            
            with trg_engine.connect() as conn:
                inspector = inspect(conn)
                for index, table in enumerate(self.tables_to_extract):
                    columns = [column['name'] for column in inspector.get_columns(table)]
                    df = pd.read_csv(f"{DIR_TEMP_DATA}/{table}.csv")

                    # Ensure df only contains columns that exist in the table schema
                    df = df[[col for col in df.columns if col in columns]]
                    dfs.append(df)

                    logging.info(f"READ '{table}' - SUCCESS")

            logging.info("READ EXTRACTED TABLES - SUCCESS")

            for index, df in enumerate(dfs):
                df.to_sql(name=self.tables_to_extract[index], con=trg_engine, schema="public", if_exists="append", index=False)
                logging.info(f"LOAD '{self.tables_to_extract[index]}' - SUCCESS")
            logging.info("LOAD ALL DATA - SUCCESS")

            end_time = time.time()
            exe_time = end_time - start_time
    
            summary_data = {
                "timestamp": [datetime.datetime.now()],
                "task": ["Load"],
                "status": ["Success"],
                "execution_time": [exe_time]
            }
            summary = pd.DataFrame(summary_data)
            summary.to_csv(f"{DIR_TEMP_DATA}/extract-summary.csv", index=False, mode="a")

        except Exception as e:
            logging.error(f"LOAD ALL DATA - FAILED: {e}\n{traceback.format_exc()}")

            summary_data = {
              "timestamp": [datetime.datetime.now()],
              "task": ["Load"],
              "status": ["Failed"],
              "execution_time": [0]
              }
            summary = pd.DataFrame(summary_data)
            summary.to_csv(f"{DIR_TEMP_DATA}/extract-summary.csv", index=False, mode="a")

        logging.info("==================================ENDING LOAD DATA=======================================")
               
    #----------------------------------------------------------------------------------------------------------------------------------------
    def output(self):
        outputs = []

        outputs.append(luigi.LocalTarget(f'{DIR_TEMP_LOG}/logs.log'))
        outputs.append(luigi.LocalTarget(f'{DIR_TEMP_DATA}/load-summary.csv'))

        return outputs
    
