import snowflake.connector
import os
from dotenv import load_dotenv


class Build:
    def initial_build(self):
        conn = snowflake.connector.connect(
            user=os.getenv('SNOWFLAKE_USER'),
            password=os.getenv('SNOWFLAKE_PASSWORD'),
            account=os.getenv('SNOWFLAKE_ACCOUNT'),
            warehouse=os.getenv('SNOWFLAKE_WAREHOUSE'),
            database=os.getenv('SNOWFLAKE_DATABASE'),
            schema=os.getenv('SNOWFLAKE_SCHEMA')
        )
        cursor = conn.cursor()

        # create initial table and load data
        create_table_query = """
        CREATE OR REPLACE TABLE stock_data (
            ticker STRING,
            queryCount INT,
            resultsCount INT,
            adjusted BOOLEAN,
            volume FLOAT,
            weightedAverage FLOAT,
            openPrice FLOAT,
            closePrice FLOAT,
            highPrice FLOAT,
            lowPrice FLOAT,
            timeUnixMsec INT,
            transactionCount INT,
            dateTime TIMESTAMP,
            date STRING,
            time STRING
        );
        """

        #
        try:
            cursor.execute(create_table_query)
            print("Table created successfully!")
        except Exception as e:
            print(f"Error creating table: {e}")

        # close connection
        cursor.close()
        conn.close()


build = Build()
build.initial_build()
