# Django Stripe Payment App

Простой пример приложения на Django с интеграцией Stripe Payment Intent для оплаты товаров с поддержкой скидок, налогов
и нескольких валют.

---

## Функционал

- Модель Item с полями: имя, описание, цена, валюта (USD или EUR)
- Модели Discount, Tax для применения к заказу
- Модель Order для объединения нескольких товаров, применения скидок и налогов
- Оплата через Stripe Payment Intent с учётом валюты

- API эндпоинты:
    - ```GET /item/{id}/``` — простая HTML-страница с info о товаре и кнопкой покупки
    - ```GET /buy/{id}/``` — создание Stripe Payment Intent и получение client secret для оплаты через JS
    - Django Admin с возможностью управления товарами, заказами, скидками и налогами
    - Кастомная Django команда ```createadmin``` для автоматического создания администратора при старте

- Docker и docker-compose для контейнеризации и удобного запуска
- Приложение запущено онлайн: https://stripetest-production-38a0.up.railway.app/

---

## Быстрый старт локально

1. Клонируйте репозиторий:

```
git clone https://github.com/kreenna/stripe_test
cd stripe_test
```

2. Создайте файл .env с переменными окружения на основе .env-sample.

3. Запустите Docker-контейнеры:

```
docker-compose up --build
```

4. При первом запуске выполнится миграция, сбор статики и команда createadmin, которая создаст администратора:

```
username: admin
password: 123qwe456rty
```

5. Приложение будет доступно по адресу http://localhost/

- Админка: http://localhost/admin/
- Страницы товаров: http://localhost/item/{id}/
- Запрос оплаты с использованием Payment Intent (client_secret): http://localhost/buy/{id}/

---

## Deploy

- Использован Dockerfile с двухступенчатой сборкой для уменьшения размера образа
- Пример docker-compose.yml содержит сервисы:
    - ```web``` — Django с Gunicorn
    - ```db``` — PostgreSQL с сохранением данных в volume
    - ```nginx``` — для обработки статических файлов и проксирования

- Используются переменные окружения из файла ```.env```
- Для старта на сервере достаточно запустить ```docker-compose up --build```

---

## Особенности и бонусы

- Поддержка двух валют (USD и EUR) с двумя разными Stripe ключами
- Оплата реализована через Stripe Payment Intent (не Session)
- Автоматическое создание админа через команду ```createadmin```
- Модели ```Discount``` и ```Tax``` применяются к заказу и передаются в платеж Stripe
- Полная админ-панель Django для управления данными
- Приложение доступно онлайн с демонстрационной админкой

---

### Ссылки

- Онлайн приложение: https://stripetest-production-38a0.up.railway.app/
- Админка онлайн: https://stripetest-production-38a0.up.railway.app/admin/
- Документация Stripe: https://stripe.com/docs

---
