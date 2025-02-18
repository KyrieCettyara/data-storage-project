import time
import luigi
import datetime
import traceback
import pandas as pd
from sqlalchemy import text

import os
from dotenv import load_dotenv

from pipeline.extract import Extract
from pipeline.utils.db_conn import db_connection
from pipeline.utils.copy_log import add_log

load_dotenv()

# Define DIR
DIR_ROOT_PROJECT = os.getenv("DIR_ROOT_PROJECT")
DIR_TEMP_LOG = os.getenv("DIR_TEMP_LOG")
DIR_TEMP_DATA = os.getenv("DIR_TEMP_DATA")
DIR_LOAD_QUERY = os.getenv("DIR_LOAD_QUERY")
DIR_LOG = os.getenv("DIR_LOG")

class GlobalParams(luigi.Config):
    CurrentTimestampParams = luigi.DateSecondParameter(default=datetime.datetime.now())

class Load(luigi.Task):

    tables_to_load = ['address',
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
    
    current_timestamp = GlobalParams().CurrentTimestampParams

    def requires(self):
        return Extract()
    
    def run(self):

        # Define db connection engine
        _, stg_engine = db_connection()
    

        logger = add_log("load", self.current_timestamp)
        logger.info("==================================PREPARATION - TRUNCATE DATA=======================================")

        # Truncating the tables before loading the data to avoid duplicates
        try:
            with db_connection.connect() as conn:
                for table in self.tables_to_load:
                    select_query = text(f"SELECT 1 FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = '{table}'")
                    result = conn.execute(select_query)

                    if result.scalar_one_or_none():
                        truncate_query = text(f"TRUNCATE public.{table} CASCADE")
                        
                        conn.execute(truncate_query)
                        conn.commit()

                        logger.info(f"TRUNCATE {table} - SUCCESS")
                    else:
                        logger.info(f"Table '{table}' does not exist, skipping truncate operation")
            logger.info("TRUNCATE ALL TABLES - DONE")

        except Exception as e:
            logger.error(f"TRUNCATE DATA - FAILED: {e}\n{traceback.format_exc()}")
        
        logger.info("==================================ENDING PREPARATION=======================================")
        logger.info("==================================STARTING LOAD DATA=======================================")

        # Loading the data after the tables already empty
        try:
            start_time = time.time()

            dfs: list[pd.DataFrame] = []

            for table in self.tables_to_load:
                df = pd.read_csv(f"{DIR_TEMP_DATA}/{table}.csv")
                dfs.append(df)

                logger.info(f"READ '{table}' - SUCCESS")
            
            logger.info("READ EXTRACTED TABLES - SUCCESS")

            for index, df in enumerate(dfs):
                df.to_sql(
                    name=self.tables_to_load[index],
                    con=stg_engine,
                    schema="public",
                    if_exists="append",
                    index=False
                )

                logger.info(f"LOAD '{self.tables_to_load[index]}' - SUCCESS")
            
            logger.info("LOAD ALL DATA - SUCCESS")

            end_time = time.time()
            exe_time = end_time - start_time

            summary_data = {
                "timestamp": [datetime.datetime.now()],
                "task": ["Load"],
                "status": ["Success"],
                "execution_time": [exe_time]
            }
            summary = pd.DataFrame(summary_data)
            summary.to_csv(self.output().path, index=False, mode="a")
        except Exception as e:
            logger.error(f"LOAD ALL DATA - FAILED: {e}\n{traceback.format_exc()}")

            summary_data = {
                "timestamp": [datetime.datetime.now()],
                "task": ["Load"],
                "status": ["Failed"],
                "execution_time": [0]
            }
            summary = pd.DataFrame(summary_data)
            summary.to_csv(self.output().path, index=False, mode="a")
        
        logger.info("==================================ENDING LOAD DATA=======================================")
    
    def output(self):
        return [luigi.LocalTarget(f'{DIR_TEMP_LOG}/logs.log'),
                luigi.LocalTarget(f'{DIR_TEMP_DATA}/load-summary.csv')]