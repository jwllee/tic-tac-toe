import pygame, os


def main():
    pygame.init()
    window_icon_fp = os.path.join('..', 'icons',
                                  'base',
                                  'window-icon', 
                                  '128.png')
    logo = pygame.image.load(window_icon_fp)
    pygame.display.set_icon(logo)
    pygame.display.set_caption('minimal program')

    screen = pygame.display.set_mode((240, 180))

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


if __name__ == '__main__':
    main()
