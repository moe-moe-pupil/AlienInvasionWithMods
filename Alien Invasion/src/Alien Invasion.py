import pygame
from pygame.locals import *
from pygame.sprite import Group
from settings import Settings
from my_enum.color_enum import ColorEnum
from option import Option
import sys
from gui_controller import GuiController
from ship import Ship
from game_stats import GameStats
import game_function as gf
from mod.mod_loader import ModLoader
from mod.mod_api import ModApi

color_enum = ColorEnum()
options = {}
selected_idx = 1
menus = {}


def modify_range(mod_int):
    global selected_idx
    global options
    if selected_idx + mod_int < 0:
        selected_idx = selected_idx + len(options) + mod_int
    elif selected_idx + mod_int >= len(options):
        selected_idx = mod_int - 1
    else:
        selected_idx += mod_int


def start():
    print("start")


def leave():
    sys.exit()


def update():
    global menus
    global options
    global screen
    global selected_idx
    global ai_settings
    global ship
    global mod_gui
    global bullets
    global aliens
    global stats
    global mods
    while menus["selected"] != "NULL":
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
                elif event.key == pygame.K_r:
                    mod_gui.browser_refresh()
            if event.type == pygame.MOUSEMOTION:
                pos = pygame.mouse.get_pos()
                #print(pos)
                for i in range(0, len(options)):
                    if options[i].can_selected:
                        o_x = ai_settings.screen_width / 2 - options[i].content.get_rect()[2] / 2
                        o_y = options[i].height
                        o_x1 = o_x + options[i].content.get_rect()[2]
                        o_y1 = o_y + 100
                        if o_x <= pos[0] <= o_x1 and o_y <= pos[1] <= o_y1:
                            #print(i)
                            selected_idx = i
                            for j in range(0, len(options)):
                                options[j].unselected()
                            options[i].selected()
                            break
            if event.type == MOUSEBUTTONDOWN:
                pressed_array = pygame.mouse.get_pressed()
                for index in range(len(pressed_array)):
                    if pressed_array[index]:
                        if index == 0:
                            for i in range(0, len(options)):
                                o_x = ai_settings.screen_width / 2 - options[i].content.get_rect()[2] / 2
                                o_y = options[i].height
                                o_x1 = o_x + options[i].content.get_rect()[2]
                                o_y1 = o_y + 100
                                if o_x <= pos[0] <= o_x1 and o_y <= pos[1] <= o_y1:
                                    options[i].trigger()
                                    break
        # 初始化UI
        screen.fill(ai_settings.bg_color)

        for i in range(0, len(options)):
            screen.blit(options[i].content, (ai_settings.screen_width / 2 - (options[i].content.get_rect()[2] / 2),
                                             options[i].height))
        pygame.display.update()
    while menus["selected"] == "NULL":
        gf.check_events(ai_settings, screen, ship, bullets, mod_gui)
        if stats.game_active:
            ship.update()
            gf.update_aliens(ai_settings, stats, screen, ship, aliens, bullets)
            gf.update_bullets(ai_settings, screen, ship, aliens, bullets)
        else:
            main_menu()
            update()
        gf.update_screen(ai_settings, screen, ship, aliens, bullets)


def main_menu():
    global menus
    global selected_idx
    global options
    global ai_settings
    options.clear()
    menus["selected"] = "main"
    font = "SourceHanSansCN-Normal.ttf"
    selected_idx = 1
    options[0] = Option(0, "title", "外星人入侵", font , 90, color_enum.gray, can_selected=False)
    options[1] = Option(1, "start", "开始", font, 75, color_enum.black, run_game, height=380)
    options[2] = Option(2, "mod", "模组", font, 75, color_enum.black, mod_menu, height=480)
    options[3] = Option(3, "about", "关于", font, 75, color_enum.black, about_menu, height=580)
    options[4] = Option(4, "quit", "退出", font, 75, color_enum.black, leave,height=680)
    options[1].selected()
    pygame.display.set_caption("外星人入侵")


def about_menu():
    global menus
    global selected_idx
    global options
    global ai_settings
    options.clear()
    menus["selected"] = "about"
    font = "SourceHanSansCN-Normal.ttf"
    selected_idx = 5
    options[0] = Option(0, "title", "外星人入侵", font, 90, color_enum.gray, can_selected=False)
    options[1] = Option(1, "author", "@作者：董浩", font, 65, color_enum.black, can_selected=False, height=380)
    options[2] = Option(2, "text", "·本项目完全开源，免费，仅供技术学习和交流之用                 ",
                        font,
                        40,
                        color_enum.black,
                        can_selected=False, height=450)
    options[3] = Option(3, "about", "·遵循MIT开源协议，您制作的MOD所有权利均归您个人所有", font, 40, color_enum.black,
                        can_selected=False,
                        height=520)
    options[4] = Option(4, "about-1", "·https://gitee.com/moe_moe_pupil/alien-invasion-supporting-mod（回车复制）",
                        font,
                        30,
                        color_enum.black, height=590)
    options[5] = Option(5, "back", "返回", font, 75, color_enum.black, main_menu, height=690)
    options[5].selected()
    pygame.display.set_caption("关于我")


def mod_menu():
    global menus
    global selected_idx
    global options
    global ai_settings
    global mods
    options.clear()
    menus["selected"] = "mod"
    font = "SourceHanSansCN-Normal.ttf"
    selected_idx = 2
    options[0] = Option(0, "title", "外星人入侵", font, 90, color_enum.gray, can_selected=False)
    options[1] = Option(1, "author", "已加载模组数量{}/{}".format(len(mods.mod_list), len(mods.mod_list)), font, 65, color_enum.black, can_selected=False, height=280)
    idx = 2
    for mod in mods.mod_name:
        options[idx] = Option(idx, "mods" + str(idx), mod, font, 75, color_enum.black, can_selected= False, height=280 + idx * 100)
        idx += 1
    options[idx] = Option(idx, "back", "返回", font, 75, color_enum.black, main_menu, height=280 + idx * 100)
    options[idx].selected()
    pygame.display.set_caption("模组")


def run_game():
    global ai_settings
    global screen
    pygame.display.set_caption("外星人入侵")
    global ship
    global mod_gui
    global menus
    global options
    global aliens
    global stats
    stats = GameStats(ai_settings)
    gf.create_fleet(ai_settings, screen, ship, aliens)
    menus["selected"] = "NULL"
    options.clear()



pygame.init()
ai_settings = Settings()
screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
ship = Ship(screen)
mods = ModLoader()
mod_api = ModApi(ai_settings)
mod_gui = GuiController(mod_api)
hwnd = pygame.display.get_wm_info()['window']
for mod in mods.mod_list:
    print(mod)
    mod_gui.browser_embed(mod, hwnd, 0, 0, show=False)

bullets = Group()
aliens = Group()
stats = GameStats(ai_settings)
main_menu()
update()
