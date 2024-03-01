<h1 align="center">🪀 YoYo 🪀</h1>

<h3 align="center"><b>For Your YoYo Data Flow...</b></h3>

```py
from yoyo import YoYo

# Initialise a cache object model
cache = YoYo(
  schema = "custom_schema" # optional : default = "store"
  cache_dir = "cache-data" # optional : default = "tmp"
)

# Get a connection to the cache
conn = cache.connect()

# Query the cache
conn.execute("SELECT * FROM store.perfect_data LIMIT 1000;").pl() # returns Polars DataFrame

# Get the information schema
cache.info()

# Check if a table name exists in the cache (True / False)
cache.check(table="api_data_2024_02")

# List all tables in the cache 
cache.list_all_tables() # without schema information

cache.list_schema_tables() # with schema information

# Create / update a table in the cache with DuckDB readable in-memory data
cache.update(
  table = "post_delta_query",
  source = "api_data", 
) 

# Backup the cache to cache directory 
cache.backup(
  cache_dir = "cache/custom-dir" # optional : default = "tmp/backup"
  )

# Remove the cache backup files
cache.erase_backup()

# Remove the cache file
cache.erase()

# Clear items from the cache
cache.clear(schema = "custom-schema", table = "special-table") # specific schema table

cache.clear(schema = "custom-schema") # entire schema

cache.clear(table = "special-table") # specific table table in default schema ("store")


```

---
