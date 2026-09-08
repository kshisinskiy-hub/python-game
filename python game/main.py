import sys
import pygame
from constants import BG_COLOR, FPS, HEIGHT, RECIPES, WIDTH
from element import Element


def try_craft(elem1, elem2, font):
    key = tuple(sorted((elem1.type_id, elem2.type_id)))
    result_type = RECIPES.get(key)

    if result_type:
        new_x = (elem1.rect.x + elem2.rect.x) // 2
        new_y = (elem1.rect.y + elem2.rect.y) // 2
        return Element(result_type, new_x, new_y, font)
    return None


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Алхимический Рынок")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 16, bold=True)

    elements = [
        Element("fire", 100, 100, font),
        Element("water", 220, 100, font),
        Element("earth", 340, 100, font),
        Element("air", 460, 100, font),
    ]

    active_element = None
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = event.pos
                    for elem in reversed(elements):
                        if elem.rect.collidepoint(mouse_pos):
                            elem.is_dragging = True
                            elem.offset_x = elem.rect.x - mouse_pos[0]
                            elem.offset_y = elem.rect.y - mouse_pos[1]
                            active_element = elem
                            elements.remove(elem)
                            elements.append(elem)
                            break

            elif event.type == pygame.MOUSEMOTION:
                if active_element and active_element.is_dragging:
                    mouse_x, mouse_y = event.pos
                    active_element.rect.x = mouse_x + active_element.offset_x
                    active_element.rect.y = mouse_y + active_element.offset_y

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and active_element:
                    active_element.is_dragging = False
                    for other in elements:
                        if other is not active_element:
                            if active_element.rect.colliderect(other.rect):
                                new_elem = try_craft(
                                    active_element, other, font
                                )
                                if new_elem:
                                    elements.remove(active_element)
                                    elements.remove(other)
                                    elements.append(new_elem)
                                break
                    active_element = None

        screen.fill(BG_COLOR)
        for elem in elements:
            elem.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()