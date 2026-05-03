"""Download the events parquet and (optionally) load it into a local DuckDB.

Usage:
    python scripts/prepare_data.py             # download parquet only
    python scripts/prepare_data.py --duckdb    # also load into data/events.duckdb
"""

import argparse
import os
import sys
import time

import gdown


GDRIVE_FILE_ID = "1v_X1FpOvk3GrZKQZRo2vLZYyqWi5E45P"
GDRIVE_URL = f"https://drive.google.com/uc?id={GDRIVE_FILE_ID}"

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
PARQUET_PATH = os.path.join(DATA_DIR, "events.parquet")
DUCKDB_PATH = os.path.join(DATA_DIR, "events.duckdb")


def download_parquet():
    if os.path.exists(PARQUET_PATH):
        size_mb = os.path.getsize(PARQUET_PATH) / 1e6
        print(f"Parquet already present: {PARQUET_PATH} ({size_mb:.0f} MB)")
        return
    os.makedirs(DATA_DIR, exist_ok=True)
    print("Downloading events.parquet from Google Drive (≈120 MB)...")
    gdown.download(GDRIVE_URL, PARQUET_PATH, quiet=False)
    size_mb = os.path.getsize(PARQUET_PATH) / 1e6
    print(f"Done: {size_mb:.0f} MB at {PARQUET_PATH}")


def load_to_duckdb():
    import duckdb
    if os.path.exists(DUCKDB_PATH):
        os.remove(DUCKDB_PATH)
    print(f"Loading parquet into DuckDB: {DUCKDB_PATH}")
    t0 = time.time()
    con = duckdb.connect(DUCKDB_PATH)
    con.execute("CREATE SCHEMA IF NOT EXISTS raw")
    con.execute(f"CREATE OR REPLACE TABLE raw.events AS SELECT * FROM read_parquet('{PARQUET_PATH}')")
    cnt = con.execute("SELECT COUNT(*) FROM raw.events").fetchone()[0]
    con.close()
    print(f"Loaded {cnt:,} events ({time.time()-t0:.1f}s). Query as `raw.events`.")


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--duckdb", action="store_true",
                    help="Also load the parquet into a local DuckDB at data/events.duckdb")
    args = ap.parse_args()

    download_parquet()
    if args.duckdb:
        load_to_duckdb()


if __name__ == "__main__":
    sys.exit(main())
