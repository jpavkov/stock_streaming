# stock_streaming 

## Overview
The goal of this project is to ingest stock data using a Yahoo! api, process the data and manipulate it with python, storing it in Snowflake. AWS will be used to deploy Docker containers to a Kubernetes cluster. Upon completion, the data will be available for phase 2, which will be to perform modeling on stock prices over time with time-series analysis.

## Architecture
/stock_streaming/
│
├── .github/                # GitHub-related files (actions, workflows, etc.)
├── .gitignore              # Ignore files for Git version control
├── Dockerfile              # Dockerfile to containerize the Python application
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
├── airflow/                # Airflow DAG definitions
│   └── stock_data_dag.py   # Airflow DAG for orchestrating the pipeline
│
├── src/                    # Main source code folder
│   ├── __init__.py         # Marks the folder as a package
│   ├── data/               # Data-related code
│   │   ├── fetch_data.py   # Functions for fetching data from the Yahoo Finance API
│   │   └── transform_data.py # Functions for data cleaning/transformation
│   ├── db/                 # Database interactions
│   │   ├── snowflake_connector.py # Functions for interacting with Snowflake
│   ├── config/             # Configuration and secrets (handled securely)
│   │   └── config.py       # Configurations (API keys, Snowflake credentials)
│   └── main.py             # Entry point for running the pipeline locally
│
├── tests/                  # Unit tests for the Python code
│   ├── test_fetch_data.py  # Tests for data fetching functions
│   ├── test_transform_data.py # Tests for data transformation
│   └── test_snowflake.py   # Tests for Snowflake interactions
│
└── kubernetes/             # Kubernetes-related files
    ├── deployment.yaml     # Kubernetes Deployment manifest
    ├── service.yaml        # Kubernetes Service manifest
    └── secrets.yaml        # Kubernetes secrets for sensitive information
