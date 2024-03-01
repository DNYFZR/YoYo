# YoYo Cache Testing Module

import os, pytest, duckdb, polars as pl
from yoyo import YoYo

test_case = {
  "table": "test_table",
  "source": "test_df",
  "backup": f"/tmp/test_backup/",
  "db" : f"test_cache",
  "erase_db": "eraser",
  "erase_table": "tmp_table",
}

os.makedirs(f"{os.getcwd()}/tmp", exist_ok=True)

test_df = pl.DataFrame({
  "A": [1,2,3],
  "B": ["A", "B", "C"],
  "C": [2,4,6],
  "D": [0.1, 0.2, 0.3],
  })

@pytest.mark.parametrize("test_case", [test_case, ])
class TestCache:
  """Test the functionality of the Cache class"""
  def test_init(self, test_case):
    """Test initialisation of the Cache class"""
    obj  = YoYo(db=test_case["db"]).__dir__()

    if "cache_dir" not in obj:
      raise AssertionError(f"Cache initialisation error : 'cache_dir' not in object")
    
    if "db" not in obj:
      raise AssertionError(f"Cache initialisation error : 'db' not in object")
    
    if "schema" not in obj:
      raise AssertionError(f"Cache initialisation error : 'schema' not in object")
    

  def test_connect(self, test_case):
    """Test the connect method"""
    conn = YoYo(db=test_case["db"]).connect()

    if not isinstance(conn, duckdb.DuckDBPyConnection):
      del conn
      raise AssertionError("Cache connection test failed")
    
    conn.close()
    

  def test_info(self, test_case):
    """Test the info method"""
    cache = YoYo(db=test_case["db"]).info()

    if not isinstance(cache, list):
      raise AssertionError("Cache info data structure test failed")


  def test_list_all_tables(self, test_case):
    """Test the list tables (no schema info) method"""
    cache = YoYo(db=test_case["db"]).list_all_tables()

    if not isinstance(cache, list):
      raise AssertionError("Cache list tables data structure test failed")
  

  def test_list_schema_tables(self, test_case):
    """Test the list tables (with schema info) method"""
    cache = YoYo(db=test_case["db"]).list_schema_tables()

    if not isinstance(cache, list):
      raise AssertionError("Cache list schema tables data structure test failed")
  

  def test_update(self, test_case):
    """Test the table update method creates a table using in memory data"""
    try:
      cache = YoYo(db=test_case["db"])
      cache.connect()
      cache.update(table=test_case["table"], source=test_case["source"])

    except Exception as e:
      raise AssertionError(f"Test update method failed with error : {e}")


  def test_check(self, test_case):
    """Test the cache table checking method"""
    try:
      YoYo(db=test_case["db"]).check(test_case["table"])

    except Exception as e:
      raise AssertionError(f"Test table checking method failed with exeption :{e}")


  def test_backup(self, test_case):
    """Test the cache backup method creates a backup"""
    cache = YoYo(db=test_case["db"])
    cache.update(test_case["table"], test_case["source"])
    cache.backup(cache_dir=f"{os.getcwd()}/{test_case["backup"]}")
    _, _, backup_files = list(os.walk(f"{os.getcwd()}/{test_case["backup"]}"))[0]

    if len(backup_files) == 0:
      raise AssertionError("Test backup method failed : no backup was detected")
      
    
  def test_erase(self, test_case):
    """Test the cache erase method removes the cache file"""
    cache = YoYo(db=test_case["erase_db"])
    cache.erase()
    
    if os.path.exists(test_case["erase_db"]):
      raise AssertionError("Test erase method failed : cache file detected")
    

  def test_erase_backup(self, test_case):
    """Test the cache erase backup method removes backup files"""
    cache = YoYo(db=test_case["db"])
    cache.backup()
    _, _, backup_files = list(os.walk(cache.cache_dir))[0]
    cache.erase_backup()

    if any([os.path.exists(i) for i in backup_files]):
        raise AssertionError("Test erase backup method failed : backup files detected")
    

  def test_clear(self, test_case):
    """Test the cache clear method erases the cache 
       but leaves the file in place"""
    cache = YoYo(db=test_case["db"])
    cache.update(test_case["erase_table"], test_case["source"])
    cache.clear(table=test_case["erase_table"])

    if test_case["erase_table"] in cache.list_all_tables():
      raise AssertionError("Test clear method failed : table detected in cache")
    
