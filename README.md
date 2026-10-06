
#  Алхимический Рынок (Alchemy Craft & Trade)

Учебный проект 2D-игры в жанре логического крафтинга, разработанный на языке Python с использованием библиотеки Pygame.

##  Описание проекта
В данной игре игрок выступает в роли алхимика. С помощью мыши (механика Drag-and-Drop) можно перетаскивать базовые элементы друг на друга, открывая новые рецепты и создавая более редкие вещества (например, *Огонь + Вода = Пар*). В следующих лабораторных работах полученные редкие элементы можно будет продавать на динамическом рынке.

##  Механики и функционал
* **Drag-and-Drop:** Плавное перетаскивание графических элементов мышью.
* **Обсчет коллизий:** Автоматическая проверка столкновений объектов с помощью `pygame.Rect.colliderect`.
* **Система крафта:** Генерация новых элементов при совпадении рецепта и удаление исходных ингредиентов.
* **Модульная архитектура:** Разделение логики на константы, графические объекты и главный игровой цикл.

##  Структура проекта
```text
python-game/
│
├── assets/                # Папка с PNG иконками
├── recipes.json           # Структура рецептов и стартовых элементов (JSON)
├── game_flight.log        # Автоматически создаваемый лог событий (LOG/TXT)
├── session_stats.csv      # Таблица рекордов и сессий (CSV)
├── constants.py           # Константы и парсинг рецептов
├── data_manager.py        # Модуль работы с JSON, CSV и logging
├── element.py             # Класс игрового элемента
├── main.py                # Точка входа и главный игровой цикл
└── README.md              # Документация проекта
```
## Скриншоты игры</h1>

<h3>Базовое состояние игры</h3>
<img width="599" height="477" alt="Screenshot_14" src="https://github.com/user-attachments/assets/1cd67048-a0d7-4f6f-9db9-bc16d4c655de" />


<h3>Создание энергии из огня и воздуха</h3>
<img width="599" height="476" alt="Screenshot_2" src="https://github.com/user-attachments/assets/3025870a-fef2-4899-8e5a-1be83d0b56f5" />

<h3>Создание грязи из воды и земли</h3>
<img width="598" height="473" alt="Screenshot_5" src="https://github.com/user-attachments/assets/a5e3fd24-79c1-4aec-a9ce-038d3fac45ed" />

<h3>Создание пара из огня и воды</h3>
<img width="596" height="470" alt="Screenshot_1" src="https://github.com/user-attachments/assets/6c76e628-56bb-4422-9dc9-69e1e5419906" />

<h3>Создание лавы из огня и земли</h3>
<img width="600" height="469" alt="Screenshot_3" src="https://github.com/user-attachments/assets/3f893147-e9cf-4ec6-a0f5-289d327a3e98" />

<h3>Создание дождя из воды и воздуха</h3>
<img width="598" height="474" alt="Screenshot_4" src="https://github.com/user-attachments/assets/c52610ca-7fe1-48bf-8914-0a1bd154d913" />

