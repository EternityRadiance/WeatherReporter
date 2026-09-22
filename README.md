# Weather Forecast Application

## Описание проекта

Программа для получения прогноза погоды на 4 дня для указанного города с использованием OpenWeatherMap API. Приложение получает данные о погоде, сохраняет их в базу данных SQLite и экспортирует результаты в Markdown-формат.

**Технологии и API:**
- Python 3.x
- OpenWeatherMap API (бесплатный тариф)
- SQLAlchemy (работа с базой данных)
- Requests (HTTP-запросы)
- SQLite (встроенная база данных)
- python-dotenv (управление переменными окружения)

## Установка

1. **Клонирование репозитория:**
   ```bash
   git clone <repository-url>
   cd Lab1
   ```

2. **Создание виртуального окружения:**
   ```bash
   python -m venv venv
   ```

3. **Активация виртуального окружения:**
   - Linux/macOS:
     ```bash
     source venv/bin/activate
     ```
   - Windows:
     ```bash
     venv\Scripts\activate
     ```

4. **Установка зависимостей:**
   ```bash
   pip install -r requirements.txt
   ```

## Настройка

1. **Создание файла `.env`:**
   ```bash
   cp .env.example .env
   ```

2. **Регистрация на OpenWeatherMap:**
   - Перейдите на [openweathermap.org](https://openweathermap.org)
   - Зарегистрируйтесь и получите бесплатный API-ключ
   - Вставьте ключ в файл `.env` в переменную `WEATHER_API_KEY`

3. **Заполнение параметров в файле `.env`:**
   ```env
   # OpenWeatherMap
   WEATHER_API_KEY=ваш_api_ключ_здесь
   WEATHER_API_BASE_URL=https://api.openweathermap.org/data/2.5/forecast
   
   # GeoAPI
   GEO_API_URL=https://ipinfo.io
   GEO_API_FALLBACK_CITY=ваш_город_по_умолчанию
   
   # База данных
   DB_URL=sqlite:///weather_forecast.db
   
   # Выходной файл
   OUTPUT_FILE=weather_report.md
   ```

## Запуск

```bash
python main.py
```

Программа выполнит следующие шаги:
1. Инициализирует базу данных
2. Определит местоположение (по IP или использует город по умолчанию)
3. Получит прогноз погоды на 4 дня
4. Сохранит данные в базу данных (пропуская дубликаты)
5. Экспортирует результаты из базы данных в Markdown-файл

## Структура проекта

- **`main.py`** - основной скрипт, координирующий работу всех модулей
- **`weather_client.py`** - взаимодействие с OpenWeatherMap API, получение и обработка данных о погоде
- **`geo_locator.py`** - определение местоположения по IP-адресу (используется ipinfo.io)
- **`db_models.py`** - модели базы данных SQLAlchemy, функции для работы с БД
- **`exporter.py`** - экспорт данных из базы данных в Markdown-формат
- **`requirements.txt`** - список зависимостей Python
- **`.env.example`** - шаблон файла конфигурации
- **`.env`** - файл конфигурации

## Пример вывода

### Консольный вывод:
```
City: Helsinki
Coords: 60.1699, 24.9384

Days: 4
Period: 2026-09-22 - 2026-09-25

Saved: 4.
Skipped: 0.

File: weather_report.md
```

### Markdown-файл (weather_report.md):
```markdown
Weather Forecast

Location: Helsinki
Period: 2026-09-22 - 2026-09-25

| Date | Min.Temp | Max.Temp | Desc | Humidity | Wind |
|------|----------|----------|------|----------|------|
|2026-09-22 |7.88 15.3 ясно 75 4 |
|2026-09-23 |10.22 13.01 небольшой дождь 83 5.46 |
|2026-09-24 |9.7 13.97 дождь 94 8.09 |
|2026-09-25 |12.77 13.65 пасмурно 79 8.08 |
```