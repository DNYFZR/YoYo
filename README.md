<h1 align="center">LiteCache 🪀</h1>

<h3 align="center"><b>For Your Yo-Yo Data Flow</b></h3>

LiteCache provides serverless data caching services, with backup functionality, inside a light weight & powerful API.

There are minimal dependencies, LiteCache only requires :

- Polars (no mandatory dependencies)
- DuckDB (no mandatory dependencies)
- PyArrow (also installs NumPy)

It was developed to serve as a low overhead backend API cache manager. Users have access the cache's underlying DuckDB functionaliy via the ```Cache().connect()``` method, which returns a connection with access to all inherrited DuckDB functionality, and Polars brings the power of Rust for data processing along side the main caching mechanisms.

## API Reference

```py
from lite_cache import Cache

# Initialise a cache object model
cache = Cache(
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

# Create / update a table in the cache
cache.update(
  table = "post_delta_query",
  source = "api_data", # api_data is an in-memory table which DuckDB can interact with (see DuckDB docs for current list) 
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

cache.clear(table = "special-table") # specific table table in default schema ("tmp")


```

---
