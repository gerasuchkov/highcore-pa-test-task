.PHONY: help setup download duckdb clean

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "%-12s %s\n", $$1, $$2}'

setup: ## Install Python dependencies
	pip install -r requirements.txt

download: ## Download events.parquet only (~120 MB) — Option 1
	python scripts/prepare_data.py

duckdb: ## Download parquet AND build a local DuckDB (data/events.duckdb) — Option 2
	python scripts/prepare_data.py --duckdb

clean: ## Remove downloaded data
	rm -f data/events.parquet data/events.duckdb data/events.duckdb.wal
