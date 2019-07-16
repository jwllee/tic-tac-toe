import pygame, os


BLUE = (0, 0, 255)
WHITE = (255, 255, 255)


def draw_circle(screen, color=BLUE, center=(150, 50), radius=15, thickness=1):
    pygame.draw.circle(screen, color, 
                       center, radius, 
                       thickness)


def main():
    pygame.init()
    window_icon_fp = os.path.join('..', 'icons',
                                  'base',
                                  'window-icon', 
                                  '128.png')
    logo = pygame.image.load(window_icon_fp)
    pygame.display.set_icon(logo)
    pygame.display.set_caption('minimal program')

    screen = pygame.display.set_mode((300, 200))
    pygame.display.set_caption('Draw circle')

    screen.fill(WHITE)
    draw_circle(screen)

    # update the full display Surface to the screen
    pygame.display.flip()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


if __name__ == '__main__':
    main()