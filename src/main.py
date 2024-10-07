from data.fetch_data import fetch_stock_data
from data.transform_data import transform_data
from db.snowflake_connector import load_data_to_snowflake
# from db.snowflake_table_build import initial_build
# import pandas as pd
import datetime
import sys
print("Python Version:", sys.version)
print("Executable path:", sys.executable)


def get_previous_day_range():
    # Get today's date
    today = datetime.date.today()

    # Calculate the previous day
    previous_day = today - datetime.timedelta(days=5)

    # Format dates as strings
    start_date = previous_day.strftime("%Y-%m-%d")
    end_date = today.strftime("%Y-%m-%d")  # Single day range

    return start_date, end_date


if __name__ == "__main__":
    # fetch_stock_data(symbol: str, mult: int, span: str, start_dt: str, end_dt: str)
    # Fetch the date range for the previous day
    start_dt, end_dt = get_previous_day_range()

    # fetch stock data for the previous day's information
    raw_data = fetch_stock_data("SPY", 1, "hour", start_dt, end_dt)

    # transform data
    transformed_data = transform_data(raw_data)

    # load updated data into snowflake
    load_data_to_snowflake(transformed_data)
