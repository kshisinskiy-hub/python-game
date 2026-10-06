from data_manager import load_game_config

WIDTH, HEIGHT = 800, 600
FPS = 60

BG_COLOR = (30, 30, 40)
TEXT_COLOR = (255, 255, 255)
ELEMENT_BORDER = (120, 120, 160)

# Загружаем данные из JSON при старте приложения
config_data = load_game_config()

# Преобразуем строковые ключи в отсортированные кортежи
RECIPES = {}
for key, result in config_data.get("recipes", {}).items():
    ingredients = tuple(sorted(key.split("+")))
    RECIPES[ingredients] = result

INITIAL_ELEMENTS_CONFIG = config_data.get("initial_elements", [])

ELEMENT_DATA = {
    "fire": {"name": "Огонь"},
    "water": {"name": "Вода"},
    "earth": {"name": "Земля"},
    "air": {"name": "Воздух"},
    "steam": {"name": "Пар"},
    "lava": {"name": "Лава"},
    "mud": {"name": "Грязь"},
    "energy": {"name": "Энергия"},
    "rain": {"name": "Дождь"},
}