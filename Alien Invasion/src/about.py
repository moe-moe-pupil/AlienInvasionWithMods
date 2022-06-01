import pygame
from settings import Settings
from my_enum import ColorEnum
from gui.option import Option
import sys

color_enum = ColorEnum()
options = {}
selected_idx = 5


def modify_range(mod_int):
    global selected_idx
    global options
    if selected_idx + mod_int < 0:
        selected_idx = selected_idx + len(options) + mod_int
    elif selected_idx + mod_int >= len(options):
        selected_idx = mod_int - 1
    else:
        selected_idx += mod_int


def back():
    sys.exit()


def about_menu():
    about = True
    global selected_idx
    global options
    font = "SourceHanSansCN-Normal.ttf"
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    options[0] = Option(0, "title", "外星人入侵", font, 90, color_enum.gray, can_selected=False)
    options[1] = Option(1, "author", "@作者：董浩", font, 65, color_enum.black, can_selected=False)
    options[2] = Option(2, "text", "·本项目完全开源，免费，仅供技术学习和交流之用                 ", font, 40, color_enum.black, can_selected=False)
    options[3] = Option(3, "about", "·遵循MIT开源协议，您制作的MOD所有权利均归您个人所有", font, 40, color_enum.black, can_selected=False)
    options[4] = Option(4, "about-1", "·https://gitee.com/moe_moe_pupil/alien-invasion-supporting-mod（回车复制）", font, 30, color_enum.black)
    options[5] = Option(5, "back", "返回", font, 75, color_enum.black, back)
    options[5].selected()
    while about:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    options[selected_idx].unselected()
                    modify_range(-1)
                    while not options[selected_idx].can_selected:
                        modify_range(-1)
                    options[selected_idx].selected()
                elif event.key == pygame.K_DOWN:
                    options[selected_idx].unselected()
                    modify_range(1)
                    while not options[selected_idx].can_selected:
                        modify_range(1)
                    options[selected_idx].selected()
                elif event.key == pygame.K_RETURN:
                    options[selected_idx].trigger()
            if event.type == pygame.MOUSEMOTION:
                pos = pygame.mouse.get_pos()
                print(pos)


        # 初始化UI
        screen.fill(ai_settings.bg_color)

        # if selected == "start":
        #     text_start = text_format("开始", font, 75, color_enum.white)
        # else:
        #     text_start = text_format("开始", font, 75, color_enum.black)
        # if selected == "quit":
        #     text_quit = text_format("结束", font, 75, color_enum.white)
        # else:
        #     text_quit = text_format("结束", font, 75, color_enum.black)
        screen.blit(options[0].content, (ai_settings.screen_width / 2 - (options[0].content.get_rect()[2] / 2), 80))
        for i in range(1, len(options)):
            screen.blit(options[i].content, (ai_settings.screen_width / 2 - (options[i].content.get_rect()[2] / 2), 180
                                             + i * 100))

        pygame.display.update()
        pygame.display.set_caption("外星人入侵")


pygame.init()
about_menu()
