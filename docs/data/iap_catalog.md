# Каталог IAP

Магазин игры состоит из 21 позиции трёх типов. Тип определяет, может ли позиция быть куплена один раз за пользователя или многократно.

## Типы позиций

| Тип | Что значит |
|---|---|
| `consumable` | Расходник (валюта, энергия, подсказки, паки контента). Один и тот же пользователь может покупать одну и ту же позицию многократно — это ожидаемое поведение. |
| `single_purchase` | Не-расходник: разовая покупка, привязанная к аккаунту (например, премиум-апгрейд или сезонный пасс). По дизайну каждая такая позиция может быть куплена пользователем **только один раз**. |
| `subscription` | Подписка с автопродлением. По продлению — отдельное событие `purchase` за каждый расчётный период. |

Эти типы записываются в параметр `iap_type` каждого события `purchase` / `refund`. Сам идентификатор позиции — в параметре `iap_id`.

## Каталог

| iap_id | Название | Цена (USD) | Тип |
|---|---|---|---|
| `starter_pack` | Starter Pack | 4.99 | `single_purchase` |
| `remove_ads` | Remove Ads Forever | 2.99 | `single_purchase` |
| `season_pass_v1` | Season Pass V1 | 9.99 | `single_purchase` |
| `coins_small` | 100 Coins | 0.99 | `consumable` |
| `coins_med` | 500 Coins | 4.99 | `consumable` |
| `coins_large` | 1500 Coins | 9.99 | `consumable` |
| `coins_huge` | 5000 Coins | 24.99 | `consumable` |
| `coins_mega` | 12000 Coins | 49.99 | `consumable` |
| `gems_small` | 50 Gems | 1.99 | `consumable` |
| `gems_med` | 300 Gems | 9.99 | `consumable` |
| `gems_large` | 1000 Gems | 29.99 | `consumable` |
| `energy_refill` | Energy Refill | 0.99 | `consumable` |
| `hint_pack_3` | 3 Hints | 0.99 | `consumable` |
| `hint_pack_10` | 10 Hints | 2.99 | `consumable` |
| `skip_level` | Skip Level | 1.99 | `consumable` |
| `daily_deal_1` | Daily Deal — Coins | 0.99 | `consumable` |
| `daily_deal_2` | Daily Deal — Gems | 1.99 | `consumable` |
| `piggy_bank` | Piggy Bank | 4.99 | `consumable` |
| `xmas_bundle` | Holiday Bundle | 14.99 | `consumable` |
| `vip_monthly` | VIP Monthly | 7.99 | `subscription` |
| `vip_yearly` | VIP Yearly | 59.99 | `subscription` |

## Как поведение этих позиций фиксируется в данных

Полная воронка одной покупки включает три события (см. `events.md`):

1. `iap_view` — игроку показано предложение
2. `iap_initiate` — игрок инициировал покупку (нажал «купить»)
3. `purchase` — покупка завершена (платёж прошёл)

В случае возврата позже добавляется парное событие `refund` с теми же `iap_id` / `transaction_id` и параметром `refund_reason`. Возвраты приходят с лагом 1–4 дня от исходной покупки.

В параметре `iap_type` каждого события покупки/возврата зафиксирован тип позиции, чтобы тип не нужно было каждый раз джойнить из этого каталога.
