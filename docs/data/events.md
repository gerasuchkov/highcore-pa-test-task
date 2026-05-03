# Каталог событий

Сырой поток событий — это длинная таблица, в которой каждая строка соответствует одному событию игрока. Формат близок к Firebase / GA4: у каждого события есть `event_name`, `event_timestamp`, `user_pseudo_id` и набор параметров `event_params` в виде `repeated struct{key, value:struct{string_value, int_value, double_value}}`.

Все события несут общие параметры, описывающие контекст пользователя на момент события: `platform`, `country`, `app_version`, `install_source`. Дополнительные параметры специфичны для конкретного типа события и описаны ниже.

## Список событий

| event_name | Когда эмитится | Специфичные параметры |
|---|---|---|
| `first_open` | Первый запуск приложения после установки | — (только общие) |
| `experiment_assignment` | Сразу после `first_open`, если игрок попал в активный эксперимент | `experiment_id`, `variant` |
| `session_start` | Начало пользовательской сессии | `session_id` |
| `tutorial_start` | Старт обучающего туториала | `session_id` |
| `tutorial_step` | Прохождение очередного шага туториала | `session_id`, `step` (1..7) |
| `tutorial_branch_chosen` | Выбор ветки развилки на 4-м шаге туториала | `session_id`, `branch` (`A`, `B` или `C`) |
| `tutorial_complete` | Туториал полностью пройден | `session_id` |
| `level_start` | Игрок начал прохождение уровня | `session_id`, `level_id` |
| `level_complete` | Уровень успешно пройден | `session_id`, `level_id`, `time_seconds` |
| `level_fail` | Игрок провалил уровень и вышел | `session_id`, `level_id`, `time_seconds` |
| `iap_view` | Игроку показано предложение покупки | `session_id`, `iap_id`, `price_usd` |
| `iap_initiate` | Игрок инициировал покупку (нажал «купить») | `session_id`, `iap_id`, `price_usd` |
| `purchase` | Покупка успешно завершена | `session_id`, `iap_id`, `iap_type`, `price_usd`, `currency`, `transaction_id` |
| `refund` | Возврат покупки (приходит позже самой покупки) | те же поля, что и у `purchase`, плюс `refund_reason` |
| `ad_impression` | Игроку показана реклама | `session_id`, `ad_unit` (`rewarded` / `interstitial` / `banner`) |

## Общие параметры

Эти параметры присутствуют во всех событиях:

| параметр | тип | описание |
|---|---|---|
| `platform` | string | `iOS` или `Android` |
| `country` | string | ISO-код страны игрока (US, UK, JP, DE, BR, IN и т.д.) |
| `app_version` | string | Версия мобильного клиента (например, `16.2.0` для iOS) |
| `install_source` | string | Источник установки (см. `ua_sources.md`) |

## Специфичные параметры

| параметр | тип | присутствует в событиях | описание |
|---|---|---|---|
| `session_id` | string | в большинстве событий, кроме `first_open` и `experiment_assignment` | Идентификатор пользовательской сессии (составной: `user_pseudo_id_d{day}_s{seq}`) |
| `experiment_id` | string | `experiment_assignment` | Идентификатор эксперимента (см. `experiments.md`) |
| `variant` | string | `experiment_assignment` | Группа эксперимента (`control` или `treatment`) |
| `step` | int | `tutorial_step` | Номер шага туториала (1..7) |
| `branch` | string | `tutorial_branch_chosen` | Выбранная ветка развилки (см. `tutorial_design.md`) |
| `level_id` | int | `level_start`, `level_complete`, `level_fail` | Идентификатор уровня |
| `time_seconds` | int | `level_complete`, `level_fail` | Время, проведённое игроком на уровне (в секундах) |
| `iap_id` | string | `iap_view`, `iap_initiate`, `purchase`, `refund` | Идентификатор позиции в IAP-каталоге (см. `iap_catalog.md`) |
| `iap_type` | string | `purchase`, `refund` | Тип позиции (`consumable`, `single_purchase`, `subscription`) |
| `price_usd` | double | `iap_view`, `iap_initiate`, `purchase`, `refund` | Цена позиции в USD |
| `currency` | string | `purchase`, `refund` | Валюта транзакции |
| `transaction_id` | string | `purchase`, `refund` | Идентификатор транзакции |
| `refund_reason` | string | `refund` | Причина возврата (`user_request`, `chargeback`, `policy`) |
| `ad_unit` | string | `ad_impression` | Тип рекламной единицы |

## Частоты событий

Это синтетический поток на ~200 000 пользователей за 60 дней наблюдения. Порядок величины:

- `first_open` — по одному на каждого пользователя
- `tutorial_*` — у большинства пользователей (некоторые дропают туториал на разных шагах)
- `session_start` — несколько на пользователя в день
- `level_start` / `level_complete` / `level_fail` — основная часть потока
- `purchase` / `refund` / `iap_*` — небольшая доля (платящих игроков мало)

## Как читать nested-параметры

В DuckDB параметры события можно достать так:

```sql
SELECT
    event_name,
    list_extract(filter(event_params, x -> x.key = 'level_id'), 1).value.int_value AS level_id
FROM raw.events
WHERE event_name = 'level_complete';
```

В BigQuery эквивалент через `UNNEST(event_params)` плюс `WHERE key = 'level_id'`.
