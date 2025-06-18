import math
import pandas as pd
from databricks import sql
from .config import get_config


class DatabricksSQLClient:
    def __init__(self):
        config = get_config()
        self.conn = sql.connect(
            server_hostname=config["server_hostname"],
            http_path=config["http_path"],
            access_token=config["access_token"],
        )

    def execute(self, sql_statement):
        cursor = self.conn.cursor()
        cursor.execute(sql_statement)
        cursor.close()

    def create_table(self, catalog, schema, table_name, columns_spec):
        sql_statement = f"""
        CREATE TABLE {catalog}.{schema}.{table_name} (
            {columns_spec}
        )
        """
        self.execute(sql_statement)

    def read_table(self, table_full_name):
        query = f"SELECT * FROM {table_full_name}"
        return pd.read_sql(query, self.conn)

    def write_table(self, table_full_name, df: pd.DataFrame, mode="overwrite"):
        import tempfile, os
        temp_path = tempfile.NamedTemporaryFile(delete=False, suffix=".parquet").name
        df.to_parquet(temp_path)
        cursor = self.conn.cursor()

        if mode == "overwrite":
            cursor.execute(f"DELETE FROM {table_full_name}")

        for _, row in df.iterrows():
            values = ','.join([f"'{str(x)}'" for x in row])
            cursor.execute(f"INSERT INTO {table_full_name} VALUES ({values})")
        os.remove(temp_path)
        cursor.close()

    def edit_table(self, table_full_name, set_clause, where_clause):
        query = f"UPDATE {table_full_name} SET {set_clause} WHERE {where_clause}"
        cursor = self.conn.cursor()
        cursor.execute(query)
        cursor.close()

    def insert_row(self, table_full_name, row_data: dict):
        def sql_repr(value):
            if value is None or (isinstance(value, float) and math.isnan(value)):
                return "NULL"
            elif isinstance(value, str):
                escaped = value.replace("'", "''")
                return f"'{escaped}'"
            else:
                return str(value)

        columns = ', '.join(row_data.keys())
        values = ', '.join([sql_repr(value) for value in row_data.values()])
        query = f"INSERT INTO {table_full_name} ({columns}) VALUES ({values})"
        cursor = self.conn.cursor()
        cursor.execute(query)
        cursor.close()