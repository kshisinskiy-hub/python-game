import pygame
from constants import ELEMENT_BORDER, ELEMENT_DATA, TEXT_COLOR


class Element:

    def __init__(self, type_id, x, y, font):
        self.type_id = type_id
        self.font = font
        self.name = ELEMENT_DATA.get(type_id, {}).get("name", type_id)
        self.color = ELEMENT_DATA.get(type_id, {}).get("color", (150, 150, 150))

        self.width = 90
        self.height = 50
        self.rect = pygame.Rect(x, y, self.width, self.height)

        self.is_dragging = False
        self.offset_x = 0
        self.offset_y = 0

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect, border_radius=8)
        pygame.draw.rect(
            surface, ELEMENT_BORDER, self.rect, width=2, border_radius=8
        )

        text_surf = self.font.render(self.name, True, TEXT_COLOR)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
