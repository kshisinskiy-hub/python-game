WIDTH, HEIGHT = 800, 600
FPS = 60

BG_COLOR = (30, 30, 40)
TEXT_COLOR = (255, 255, 255)
ELEMENT_BORDER = (120, 120, 160)

RECIPES = {
    tuple(sorted(("fire", "water"))): "steam",
    tuple(sorted(("fire", "earth"))): "lava",
    tuple(sorted(("water", "earth"))): "mud",
    tuple(sorted(("air", "fire"))): "energy",
    tuple(sorted(("air", "water"))): "rain",
}

ELEMENT_DATA = {
    "fire": {"name": "Огонь", "color": (230, 80, 50)},
    "water": {"name": "Вода", "color": (50, 120, 230)},
    "earth": {"name": "Земля", "color": (120, 80, 40)},
    "air": {"name": "Воздух", "color": (150, 200, 230)},
    "steam": {"name": "Пар", "color": (200, 200, 220)},
    "lava": {"name": "Лава", "color": (255, 100, 0)},
    "mud": {"name": "Грязь", "color": (100, 70, 50)},
    "energy": {"name": "Энергия", "color": (255, 220, 50)},
    "rain": {"name": "Дождь", "color": (80, 160, 240)},
}
