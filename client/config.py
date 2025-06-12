import os
from dotenv import load_dotenv

load_dotenv()

def get_config():
    return {
        "server_hostname": os.getenv("DATABRICKS_HOST"),
        "http_path": os.getenv("DATABRICKS_HTTP_PATH"),
        "access_token": os.getenv("DATABRICKS_TOKEN"),
    }