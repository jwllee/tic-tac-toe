import numpy as np
import pygame, os, pygameMenu, datetime
from pygameMenu.locals import *
from functools import partial


BLUE = (0, 0, 255)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (40, 0, 40)


W_SIZE, H_SIZE = (600, 600)
COLOR_BACKGROUND = [128, 0, 128]
ABOUT = ['pygameMenu {}'.format(pygameMenu.__version__),
         'Author: {}'.format(pygameMenu.__author__),
         pygameMenu.locals.PYGAMEMENU_TEXT_NEWLINE,
         'Email: {}'.format(pygameMenu.__email__)]
HELP = ['Press ESC to enable/disable menu',
        'Press ENTER to access a submenu or use an option',
        'Press UP/DOWN to move through menu',
        'Press LEFT/RIGHT to move through selectors']



def mainmenu_background(surface):
    surface.fill(PURPLE)


def reset_timer(timer):
    timer[0] = 0


def change_color_bg(value, c=None, **kwargs):
    color, _ = value
    if c == (-1, -1, -1): # random color
        c = (np.random.randint(0, 256),
             np.random.randint(0, 256),
             np.random.randint(0, 256))
    if kwargs['write_on_console']:
        print('New background color: {} ({}, {}, {})'.format(color, *c))
    COLOR_BACKGROUND[0] = c[0]
    COLOR_BACKGROUND[1] = c[1]
    COLOR_BACKGROUND[2] = c[2]


class TestCallClassMethod:
    @staticmethod
    def update_game_settings():
        print('Update game with new settings')


def make_timer_menu(surface, timer):
    timer_menu = pygameMenu.Menu(surface,
                                 dopause=False,
                                 font=pygameMenu.fonts.FONT_NEVIS,
                                 menu_alpha=85,
                                 menu_color=BLACK,
                                 menu_color_title=BLACK,
                                 menu_height=int(H_SIZE * 0.65),
                                 menu_width=600,
                                 onclose=pygameMenu.events.PYGAME_MENU_RESET,
                                 option_shadow=True,
                                 rect_width=4,
                                 title='Timer Menu',
                                 title_offsety=5,
                                 window_height=H_SIZE,
                                 window_width=W_SIZE)

    timer_menu.add_option('Reset timer', partial(reset_timer, timer))

    bgcolor_options = [
        ('Random', (-1, -1, -1)),
        ('Default', (128, 0, 128)),
        ('Black', BLACK),
        ('Blue', BLUE)
    ]
    timer_menu.add_selector('Change bgcolor',
                            bgcolor_options,
                            default=1,
                            onchange=change_color_bg,
                            onreturn=change_color_bg,
                            write_on_console=True)
    timer_menu.add_option('Update game object', 
                          TestCallClassMethod().update_game_settings)
    timer_menu.add_option('Return to menu', pygameMenu.events.PYGAME_MENU_BACK)
    timer_menu.add_option('Close menu', pygameMenu.events.PYGAME_MENU_CLOSE)
    return timer_menu


def make_help_menu(surface):
    help_menu = pygameMenu.TextMenu(surface,
                                    dopause=False,
                                    font=pygameMenu.fonts.FONT_FRANCHISE,
                                    menu_color=(30, 50, 107),
                                    menu_color_title=(120, 45, 30),
                                    onclose=pygameMenu.events.PYGAME_MENU_DISABLE_CLOSE,
                                    option_shadow=True,
                                    option_shadow_position=pygameMenu.locals.PYGAME_POSITION_SOUTHEAST,
                                    text_align=pygameMenu.locals.PYGAME_ALIGN_CENTER,
                                    title='Help',
                                    window_height=H_SIZE,
                                    window_width=W_SIZE)
    help_menu.add_option('Return to Menu', pygameMenu.events.PYGAME_MENU_BACK)
    for m in HELP:
        help_menu.add_line(m)
    return help_menu


def make_about_menu(surface):
    about_menu = pygameMenu.TextMenu(surface,
                                     dopause=False,
                                     draw_text_region_x=5,
                                     font=pygameMenu.fonts.FONT_NEVIS,
                                     font_size_title=30,
                                     font_title=pygameMenu.fonts.FONT_8BIT,
                                     menu_color_title=BLUE,
                                     onclose=pygameMenu.events.PYGAME_MENU_DISABLE_CLOSE,
                                     option_shadow=True,
                                     text_fontsize=20,
                                     title='About',
                                     window_height=H_SIZE,
                                     window_width=W_SIZE)
    about_menu.add_option('Return to menu', pygameMenu.events.PYGAME_MENU_BACK)
    for m in ABOUT:
        about_menu.add_line(m)
    about_menu.add_line(pygameMenu.locals.PYGAMEMENU_TEXT_NEWLINE)
    return about_menu


def make_main_menu(surface, submenu_list=[]):
    mainmenu_background_partial = partial(mainmenu_background, surface)
    menu = pygameMenu.Menu(surface,
                           dopause=True,
                           bgfun=mainmenu_background_partial,
                           enabled=False,
                           font=pygameMenu.fonts.FONT_NEVIS,
                           menu_alpha=90,
                           menu_centered=True,
                           onclose=pygameMenu.events.PYGAME_MENU_CLOSE,
                           title='Main menu',
                           title_offsety=5,
                           window_height=H_SIZE,
                           window_width=W_SIZE)

    for submenu in submenu_list:
        menu.add_option(submenu.get_title(), submenu)
    menu.add_option('Exit', pygameMenu.events.PYGAME_MENU_EXIT)
    return menu


def draw_grid(screen, n_rows=3, n_cols=3, color=BLACK, thickness=2):
    width, height = pygame.display.get_surface().get_size()
    padding = 5

    width -= 2 * padding
    height -= 2 * padding

    # vertical lines
    vlines = np.linspace(padding, width - padding, num=n_rows + 1)
    for i in range(1, n_rows):
        x = vlines[i]
        pygame.draw.line(screen, color, 
                         (x, padding), 
                         (x, height - padding), 
                         thickness)

    hlines = np.linspace(padding, height - padding, num=n_cols + 1)
    for i in range(1, n_cols):
        y = hlines[i]
        pygame.draw.line(screen, color,
                         (padding, y),
                         (width - padding, y),
                         thickness)


def main():
    pygame.init()

    FPS = 60
    clock = pygame.time.Clock()
    timer = [0.0]
    dt = 1.0 / FPS
    timer_font = pygame.font.Font(pygameMenu.fonts.FONT_NEVIS, 100)

    window_icon_fp = os.path.join('..', 'icons',
                                  'base',
                                  'window-icon', 
                                  '128.png')
    logo = pygame.image.load(window_icon_fp)
    pygame.display.set_icon(logo)
    pygame.display.set_caption('minimal program')

    screen = pygame.display.set_mode((W_SIZE, H_SIZE))
    pygame.display.set_caption('Draw circle')

    draw_grid(screen, n_rows=4, n_cols=5)

    # make menu
    timer_menu = make_timer_menu(screen, timer)
    about_menu = make_about_menu(screen)
    help_menu = make_help_menu(screen)
    submenu_list = [
        timer_menu,
        help_menu,
        about_menu,
    ]
    menu = make_main_menu(screen, submenu_list)

    running = True
    while running:
        # tick clock
        clock.tick(60)
        timer[0] += dt

        screen.fill(COLOR_BACKGROUND)

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menu.enable()

        # Draw timer
        time_string = str(datetime.timedelta(seconds=int(timer[0])))
        time_blit = timer_font.render(time_string, 1, WHITE)
        time_blit_size = time_blit.get_size()
        time_blit_x = W_SIZE / 2 - time_blit_size[0] / 2
        time_blit_y = H_SIZE / 2 - time_blit_size[1] / 2
        screen.blit(time_blit, (time_blit_x, time_blit_y))
        menu.mainloop(events)

        # update the full display Surface to the screen
        pygame.display.flip()


if __name__ == '__main__':
    main()
