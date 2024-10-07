import snowflake.connector
import os
from dotenv import load_dotenv

load_dotenv()


def load_data_to_snowflake(data):

    # # test
    # try:
    #     conn = snowflake.connector.connect(
    #         user=os.getenv('SNOWFLAKE_USER'),
    #         password=os.getenv('SNOWFLAKE_PASSWORD'),
    #         account=os.getenv('SNOWFLAKE_ACCOUNT'),
    #         warehouse=os.getenv('SNOWFLAKE_WAREHOUSE'),
    #         database=os.getenv('SNOWFLAKE_DATABASE'),
    #         schema=os.getenv('SNOWFLAKE_SCHEMA')
    #     )
    #     cursor = conn.cursor()
    #     print("Connection successful!")
    # except Exception as e:
    #     print(f"Connection failed: {e}")
    # finally:
    #     if 'conn' in locals():
    #         cursor.close()
    #         conn.close()

    # snowflake connector
    conn = snowflake.connector.connect(
        user=os.getenv('SNOWFLAKE_USER'),
        password=os.getenv('SNOWFLAKE_PASSWORD'),
        account=os.getenv('SNOWFLAKE_ACCOUNT'),
        warehouse=os.getenv('SNOWFLAKE_WAREHOUSE'),
        database=os.getenv('SNOWFLAKE_DATABASE'),
        schema=os.getenv('SNOWFLAKE_SCHEMA'),
        login_timeout=60,
        request_timeout=60
    )
    cursor = conn.cursor()

    # create_temp_table_query (stock_data without rows)
    create_temp_table_query = """
    CREATE OR REPLACE TEMPORARY TABLE temp_stock_data AS
    SELECT * FROM stock_data WHERE 0=1;
    """
    cursor.execute(create_temp_table_query)

    # Step 2: Insert DataFrame data into the temporary table
    for index, row in data.iterrows():
        insert_temp_query = f"""
        INSERT INTO temp_stock_data (ticker, queryCount, resultsCount, adjusted, volume,
                                    weightedAverage, openPrice, closePrice,
                                    highPrice, lowPrice, timeUnixMsec,
                                    transactionCount, dateTime, date, time)
        VALUES ('{row['ticker']}', {row['queryCount']}, {row['resultsCount']},
                {row['adjusted']}, {row['volume']}, {row['weightedAverage']},
                {row['openPrice']}, {row['closePrice']}, {row['highPrice']},
                {row['lowPrice']}, {row['timeUnixMsec']},
                {row['transactionCount']}, '{row['dateTime']}',
                '{row['date']}', '{row['time']}');
        """
        cursor.execute(insert_temp_query)

    # Step 3: Merge the temporary table into the stock_data table
    merge_query = """
    MERGE INTO stock_data AS target
    USING temp_stock_data AS source
    ON target.ticker = source.ticker AND target.timeUnixMsec = source.timeUnixMsec
    WHEN NOT MATCHED THEN
        INSERT (ticker, queryCount, resultsCount, adjusted, volume,
                weightedAverage, openPrice, closePrice,
                highPrice, lowPrice, timeUnixMsec,
                transactionCount, dateTime, date, time)
        VALUES (source.ticker, source.queryCount, source.resultsCount,
                source.adjusted, source.volume, source.weightedAverage,
                source.openPrice, source.closePrice,
                source.highPrice, source.lowPrice, source.timeUnixMsec,
                source.transactionCount, source.dateTime,
                source.date, source.time);
    """

    cursor.execute(merge_query)
    print("Data merged successfully!")

    # Step 4: Clean up by dropping the temporary table
    cursor.execute("DROP TABLE IF EXISTS temp_stock_data;")

    # close connection
    cursor.close()
    conn.close()
