import os, duckdb, polars as pl

__status__ = "pre-alpha"
__version__ = "0.3.1"

class YoYo:
    """ 
    Serverless Cache DB Management

    #### Parameters : 
    - schema (optional) : user can set a string or use the default 'store'
    - cache_dir (optional) : user can set a string or use the default 'tmp' 
      within the current working directory
    """
    __status__ = __status__
    __version__ = __version__

    def __init__(self, **kwargs):
        cache_dir = "tmp"
        os.makedirs(cache_dir, exist_ok=True)
        
        self.cache_dir = f"""{cache_dir if "cache_dir" not in kwargs.keys() else kwargs["cache_dir"]}/backup/"""
        self.db = f"""{cache_dir if "cache_dir" not in kwargs.keys() else kwargs["cache_dir"]}/cache.duckdb"""
        self.schema = "store" if "schema" not in kwargs.keys() else kwargs["schema"]
        
    def connect(self):
        """Connect to the cache DB"""
        return duckdb.connect(self.db)

    def info(self):
        """Get the database structure"""
        conn = self.connect()
        res = conn.sql("DESCRIBE;").pl().to_dicts()
        conn.close()
        return res

    def check(self, table:str):
        """Check if a table exists in the cache"""            
        if "." in table and table in self.list_schema_tables():
            return True

        if f"{self.schema}.{table}" in self.list_schema_tables():
            return True

        elif f"{table}" in self.list_all_tables():
            return True 
        
        else:
            return False

    def list_all_tables(self):
        """Get a list of tables in the cache (no schema info)"""
        conn = self.connect()
        res = conn.sql("DESCRIBE;").pl().select("name").to_series().to_list()
        conn.close()
        return res

    def list_schema_tables(self):
        """Get a list of tables in the cache (schema.table)"""
        conn = self.connect()
        res = conn.sql("DESCRIBE;").pl().with_columns(
            pl.concat_str([pl.col("schema"), pl.col("name")], separator="."
            ).alias("tmp")).select("tmp").to_series().to_list()
        conn.close()
        return res

    def update(self, table:str, source:str):
        """Create or update a table using the name of a DuckDB readable source"""
        
        # if schema name provided
        if "." in table:
            user_schema, table = table.split(".", maxsplit=1)
            table = f"{self.schema}.{table}" if user_schema == "main" else f"{user_schema}.{table}"

        else:
            table = f"{self.schema}.{table}"

        conn = self.connect()
        conn.sql(f"""CREATE OR REPLACE TABLE {table} AS SELECT * FROM {source};""")
        conn.close()  
        return{200: f"update successful : {table}"}

    def backup(self, **kwargs):
        """
        Export the cache to a Parquet archive
        
        Users can optionally set their own 'backup' path string as a kwarg
        or use the default 'tmp/backup' within the current working directory.
        """
        self.cache_dir = self.cache_dir if "cache_dir" not in kwargs.keys() else kwargs["cache_dir"]
        os.makedirs(self.cache_dir, exist_ok=True)
    
        conn = self.connect()
        conn.execute(f"EXPORT DATABASE '{self.cache_dir}' (FORMAT PARQUET);").close()
    
        return {200: "export completed"}
    
    def erase_backup(self):
        """Remove the cache backup files"""
        cache_path = f"{os.getcwd()}/{self.cache_dir}"
        
        if os.path.exists(cache_path):
          _, _, files = list(os.walk(cache_path))[0]

          for file in files:
              os.remove(f"{os.getcwd()}/{self.cache_dir}/{file}")

          return {200 : "cache backup wiped"}

        else:
            return {200 : "cache backup already wiped"}
         
    def erase(self):
        """Remove the cache file"""
        cache_path = f"{os.getcwd()}/{self.db}"
        
        if os.path.exists(cache_path):
          os.remove(cache_path)
          return {200 : "cache wiped"}

        else:
            return {200 : "cache already wiped"}
        
    def clear(self, schema:str = None, table:str = None):
        """Clear the duckDB cache"""
        # User can clear a specific table or entire schema
        conn = self.connect()
        if schema and table:
            conn.execute(f"DROP TABLE IF EXISTS {schema}.{table};").close()
        
        elif schema and not table:
            conn.execute(f"DROP SCHEMA IF EXISTS {schema} CASCADE;").close()
        
        elif table and not schema:
            conn.execute(f"DROP TABLE IF EXISTS {self.schema}.{table}").close()
        
        else:
            conn.close()
            return {400 : f"bad request: {schema}.{table}"}

        return {200 : "cache cleared"}
