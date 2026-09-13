import pygame
from constants import ELEMENT_BORDER, ELEMENT_DATA, TEXT_COLOR


class Element:

    def __init__(self, type_id, x, y, font):
        self.type_id = type_id
        self.font = font
        self.name = ELEMENT_DATA.get(type_id, {}).get("name", type_id)

        # Размеры элемента
        self.width = 80
        self.height = 80
        self.rect = pygame.Rect(x, y, self.width, self.height)

        # Перетаскивание
        self.is_dragging = False
        self.offset_x = 0
        self.offset_y = 0

        # Загрузка и подгонка картинки под размер 80x80
        try:
            raw_image = pygame.image.load(
                f"assets/{type_id}.png"
            ).convert_alpha()
            self.image = pygame.transform.scale(
                raw_image, (self.width, self.height)
            )
        except Exception:
            self.image = None  # Если картинки нет, программа не упадет

    def draw(self, surface):
        # 1. Рисуем картинку (если она загрузилась)
        if self.image:
            surface.blit(self.image, self.rect)
        else:
            # Запасной прямоугольник, если файл не найден
            pygame.draw.rect(
                surface, (100, 100, 100), self.rect, border_radius=10
            )

        # 2. Подпись под картинкой
        text_surf = self.font.render(self.name, True, TEXT_COLOR)
        text_rect = text_surf.get_rect(
            center=(self.rect.centerx, self.rect.bottom + 10)
        )

        # Темный фон под текстом
        bg_rect = text_rect.inflate(8, 4)
        pygame.draw.rect(surface, (20, 20, 20), bg_rect, border_radius=4)
        pygame.draw.rect(
            surface, ELEMENT_BORDER, bg_rect, width=1, border_radius=4
        )

        surface.blit(text_surf, text_rect)
