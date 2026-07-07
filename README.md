# Highcore: тестовое задание для Product Analyst

Стартовый репозиторий с описанием задания, документацией данных и скриптом для скачивания датасета. Само задание лежит в [TEST_ASSIGNMENT.md](TEST_ASSIGNMENT.md).

## Требования

- Python 3.10+
- ~500 MB свободного места на диске
- `make` (не обязательно)

## Установка

1. Клонируй репозиторий и перейди в него:

```bash
git clone <url>
cd highcore-pa-test-task
```

2. Создай виртуальное окружение и установи зависимости:

```bash
python3 -m venv .venv
source .venv/bin/activate
make setup                   # pip install -r requirements.txt
```

Все дальнейшие команды `make` выполняй в этом активированном окружении, потому что Makefile использует `python` и `pip` из него.

3. Для получения датасета выбери один из двух вариантов:

### Вариант 1: только parquet

```bash
make download
```
Либо скачай напрямую https://drive.google.com/file/d/1v_X1FpOvk3GrZKQZRo2vLZYyqWi5E45P/view?usp=sharing и положи файл как `data/events.parquet`.

Скачивает `data/events.parquet` (~120 MB, MD5 `74383bd82304c04e8a3f7deb4c5fbcf2`) с Google Диска. Дальше работаешь с ним любым удобным инструментом: `pandas`, `polars`, `duckdb` поверх parquet, BigQuery sandbox, что угодно.

### Вариант 2: parquet и готовая база DuckDB

```bash
make duckdb
```

Дополнительно создаёт `data/events.duckdb` с таблицей `raw.events`. Запросы можно выполнять через `duckdb` CLI или Python:

```python
import duckdb
con = duckdb.connect('data/events.duckdb', read_only=True)
print(con.execute('SELECT event_name, COUNT(*) FROM raw.events GROUP BY 1').fetchdf())
```

## Какой инструмент использовать для анализа

На твой выбор. Главное, чтобы мы могли повторить твои расчёты и получить те же цифры.

## Структура репозитория

```
.
├── README.md                  # этот файл
├── TEST_ASSIGNMENT.md         # само задание, начни отсюда
├── Makefile
├── requirements.txt
├── scripts/
│   └── prepare_data.py        # скачивает датасет и (по желанию) собирает DuckDB
├── docs/
│   └── data/
│       ├── events.md          # каталог событий и параметров
│       ├── iap_catalog.md     # каталог IAP-позиций и их типов
│       ├── tutorial_design.md # структура туториала и развилка
│       ├── ua_sources.md      # описание источников привлечения
│       └── experiments.md     # описание текущего A/B-теста
├── analysis/                  # сюда складываешь свои запросы и расчёты
├── skills/                    # сюда кладёшь свой скилл, если будешь его делать
└── data/                      # сюда положатся events.parquet и events.duckdb
```

## С чего начать

1. **`TEST_ASSIGNMENT.md`**: что именно нужно сделать.
2. **`docs/data/events.md`**: формат событий, какие event_name есть, какие параметры.
3. **Остальные `docs/data/*.md`**: продуктовый контекст (каталог IAP, устройство туториала, каналы привлечения, описание A/B-теста).
