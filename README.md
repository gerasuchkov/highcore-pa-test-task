# Highcore — тестовое задание для Product Analyst

Стартовый репозиторий с описанием задания, документацией данных и скриптом для скачивания датасета. Само задание — в [TEST_ASSIGNMENT.md](TEST_ASSIGNMENT.md).

## Требования

- Python 3.11+
- ~500 MB свободного места на диске
- `make` (опционально)

## Установка

1. Клонируй репозиторий и перейди в него:

```bash
git clone <url>
cd highcore-pa-test-task
```

2. Создай виртуальное окружение и установи зависимости:

```bash
python3.11 -m venv .venv     # или python3.12 / python3.13
source .venv/bin/activate
make setup                   # pip install -r requirements.txt
```

3. Получи датасет — выбери один из двух вариантов:

### Вариант 1 — только parquet

```bash
make download
```

Скачивает `data/events.parquet` (~120 MB) с Google Диска. Дальше работаешь с ним любым удобным инструментом: `pandas`, `polars`, `duckdb` поверх parquet, BigQuery sandbox, что угодно.

### Вариант 2 — parquet + готовая DuckDB

```bash
make duckdb
```

Дополнительно создаёт `data/events.duckdb` с таблицей `raw.events`. Удобно, если хочешь сразу писать SQL-запросы без прелюдии. Запросы можно выполнять через `duckdb` CLI или Python:

```python
import duckdb
con = duckdb.connect('data/events.duckdb', read_only=True)
print(con.execute('SELECT event_name, COUNT(*) FROM raw.events GROUP BY 1').fetchdf())
```

## Какой инструмент использовать для анализа

На твой выбор. Главное — воспроизводимость: чтобы мы могли повторить твои расчёты.

## Структура репозитория

```
.
├── README.md                  # этот файл
├── TEST_ASSIGNMENT.md         # само задание — начни отсюда
├── Makefile
├── requirements.txt
├── scripts/
│   └── prepare_data.py        # скачивает датасет и (опц.) поднимает DuckDB
├── docs/
│   └── data/
│       ├── events.md          # каталог событий и параметров
│       ├── iap_catalog.md     # каталог IAP-позиций и их типов
│       ├── tutorial_design.md # структура туториала и развилка
│       ├── ua_sources.md      # источники привлечения (UA-каналы)
│       └── experiments.md     # описание текущего A/B-теста
├── analysis/                  # сюда складываешь свои запросы и ноутбуки
├── skills/                    # сюда — кастомный скилл, если будешь его делать
└── data/                      # сюда положатся events.parquet и events.duckdb
```

## С чего начать

1. **`TEST_ASSIGNMENT.md`** — что именно нужно сделать.
2. **`docs/data/events.md`** — формат событий, какие event_name есть, какие параметры.
3. **Остальные `docs/data/*.md`** — продуктовый контекст: каталог IAP, дизайн туториала, UA-каналы, описание A/B-теста.
