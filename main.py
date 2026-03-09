import pygame
import random
import math
from Constants import *
from Colors import *
from Menu import Menu
from Bomb import Bomb
from Booster import Booster
from Bullet import Bullet
import os
import sys

pygame.init()
pygame.mixer.init()

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

font = pygame.font.Font(None, 50)
smallFont = pygame.font.Font(None, 25)
ARIAL_50 = pygame.font.SysFont('arial', 74)
pixel_font = pygame.font.Font(resource_path("assets/fonts/PressStart2P-Regular.ttf"), 45)
pixel_font_options = pygame.font.Font(resource_path("assets/fonts/PressStart2P-Regular.ttf"), 30)
pixel_font_small = pygame.font.Font(resource_path("assets/fonts/PressStart2P-Regular.ttf"), 15)


def load_and_prepare_icon(image_path, target_size=(32, 32)):
    try:
        image = pygame.image.load(resource_path(image_path))
        icon = pygame.transform.scale(image, target_size)
        icon = icon.convert_alpha()
        return icon
    except pygame.error as e:
        print(f"Не удалось загрузить иконку: {e}")
        icon = pygame.Surface(target_size)
        icon.fill((100, 100, 100))
        pygame.draw.rect(icon, (255, 255, 255), (4, 4, 24, 24), 2)
        return icon

backgroundPhoto = pygame.image.load(resource_path("assets/images/background/TableTennis.png"))
backgroundPhoto = pygame.transform.scale(backgroundPhoto, (WIDTH, HEIGHT))
gameMusic = resource_path("assets/music/Lumber Tycoon 2 Main Biome Theme.mp3")
mainMenuMusic = resource_path("assets/music/uglyburger0_-_3008s_friday_theme_except_its_crunchy_74565571.mp3")

background1 = pygame.image.load(resource_path("assets/images/background/menuBG.jpg"))
background2 = pygame.image.load(resource_path("assets/images/background/MenuBG1.jpg"))
background3 = pygame.image.load(resource_path("assets/images/background/MenuBG2.jpg"))
background4 = pygame.image.load(resource_path("assets/images/background/MenuBG3.jpg"))
optionsMenuBG = pygame.image.load(resource_path("assets/images/background/optionsMenuBG.jpg"))
optionsMenuBG = pygame.transform.scale(optionsMenuBG, (WIDTH, HEIGHT))
modsMenuBG =pygame.image.load(resource_path("assets/images/background/modMenuBG.png"))
modsMenuBG = pygame.transform.scale(modsMenuBG, (WIDTH, HEIGHT))
helpMenuBG = pygame.image.load(resource_path("assets/images/background/helpmenuBG.jpg"))
helpMenuBG = pygame.transform.scale(helpMenuBG, (WIDTH, HEIGHT))
helpModMenuBG = pygame.image.load(resource_path("assets/images/background/helpmodmenuBG.jpg"))
helpModMenuBG = pygame.transform.scale(helpModMenuBG, (WIDTH, HEIGHT))
menuBG = pygame.transform.scale(background1, (WIDTH, HEIGHT))

boosterSprite1 = pygame.image.load(resource_path("assets/images/Sprites/ball_smaller.png"))
boosterSprite1 = pygame.transform.scale(boosterSprite1, (60, 60))
boosterSprite2 = pygame.image.load(resource_path("assets/images/Sprites/doubleBall.png"))
boosterSprite2 = pygame.transform.scale(boosterSprite2, (60, 60))
boosterSprite3 = pygame.image.load(resource_path("assets/images/Sprites/enemy_slow.png"))
boosterSprite3 = pygame.transform.scale(boosterSprite3, (60, 60))
boosterSprite4 = pygame.image.load(resource_path("assets/images/Sprites/increace_paddle_length.png"))
boosterSprite4 = pygame.transform.scale(boosterSprite4, (60, 60))
boosterSprite5 = pygame.image.load(resource_path("assets/images/Sprites/paddle_slowDown.png"))
boosterSprite5 = pygame.transform.scale(boosterSprite5, (60, 60))
boosterSprite6 = pygame.image.load(resource_path("assets/images/Sprites/paddle_speedUp.png"))
boosterSprite6 = pygame.transform.scale(boosterSprite6, (60, 60))
bombSprite = pygame.image.load(resource_path("assets/images/Sprites/bomb (1).png"))
bombSprite = pygame.transform.scale(bombSprite, (60, 60))

currentMusic = None
def playMusic(musicFile):
    global currentMusic, gameMusicVol, menuMusicVol
    if musicFile != currentMusic:
        pygame.mixer.music.load(musicFile)
        if musicFile == mainMenuMusic:
            pygame.mixer.music.set_volume(menuMusicVol)
        else:
            pygame.mixer.music.set_volume(gameMusicVol)
        pygame.mixer.music.play(-1)
        currentMusic = musicFile

def update_music_volume():
    global currentMusic, menuMusicVol, gameMusicVol
    if currentMusic == mainMenuMusic:
        pygame.mixer.music.set_volume(menuMusicVol)
    else:
        pygame.mixer.music.set_volume(gameMusicVol)

playMusic(mainMenuMusic)

WelcomeSound = pygame.mixer.Sound(resource_path("assets/sounds/MenuSounds/welcomeSound.mp3"))
WelcomeSound.set_volume(0.1)
pygame.mixer.Sound.play(WelcomeSound)

ballStartX = WIDTH//2-ballRadius
ballStartY = HEIGHT//2-ballRadius

paddleRight = pygame.Rect(WIDTH-paddleWidth-5, HEIGHT/2-paddleHeight/2, paddleWidth, paddleHeight)
paddleLeft = pygame.Rect(5, HEIGHT/2-paddleHeight/2, paddleWidth, paddleHeight)

screen = pygame.display.set_mode((WIDTH, HEIGHT), vsync = 1 )

ball = pygame.Rect(ballStartX, ballStartY, ballD, ballD)
ball1 = pygame.Rect(ballStartX, ballStartY, ballD, ballD)

clock = pygame.time.Clock()
pygame.display.set_caption("My Ping-Pong")
icon = load_and_prepare_icon("assets/icons/icon.ico")
pygame.display.set_icon(icon)

miniPause = False
menu_pause = False #Я забыл зачем оно \_0-0_/
mods_flag = False
pauseFlag = False
pause = False
game = True
menu_flag = True
menu_flag_after = False
options_flag = False
help_flag = False
help_mod_menu_flag = False
help_mod_menu_flag1 = False

#--------------------Моды---------------------
mods = {
    "bomb_mode" : False,
    "booster_mode" : False,
    "live_field_mode" : False,
    "bullet_mode": False,
    "PVE_mode" : False
}
#--------------------Моды---------------------

bombs = []  # Список активных бомб
counterForBomb = 3
boost_added = 0.0  # Сколько скорости добавили
boost_remove_time = 0  # Когда убрать

booster_remove_time = 0
counterForBooster = 0
boosters = []

second_ball_active = False
second_ball_end_time = 0
second_ball_rect = None
second_ball_dy = 0

bullets = []
bullet_spawn = 0

# Инициализируем оригинальные значения
original_paddle_height = paddleHeight
original_paddle_left_speed = paddleLeftSpeed
original_paddle_right_speed = paddleRightSpeed
original_ball_radius = ballRadius

# Словарь для хранения активных эффектов
active_boosters = {
    "ball_smaller": False,
    "double_ball": False,
    "enemy_slow": False,
    "increace_paddle_length": False,
    "paddle_slowDown": False,
    "paddle_speedUp": False
}

# Словарь для хранения времени окончания эффектов
booster_end_times = {}


def apply_booster_effect(booster_name):
    global paddleLeftSpeed, paddleRightSpeed, paddleHeight, ballRadius, paddleLeft, paddleRight, dx
    global second_ball_active, second_ball_end_time, second_ball_rect, second_ball_dy

    booster_end_times[booster_name] = pygame.time.get_ticks() + 5000
    active_boosters[booster_name] = True

    if booster_name == "ball_smaller":
        ballRadius = max(7, ballRadius - 3)
        ball.width = ball.height = ballRadius * 2

    elif booster_name == "enemy_slow":
        if dx > 0:
            paddleRightSpeed = max(1, paddleLeftSpeed - 3)
        else:
            paddleLeftSpeed = max(1, paddleRightSpeed - 3)

    elif booster_name == "double_ball":
        second_ball_active = True
        second_ball_end_time = pygame.time.get_ticks() + 5000
        second_ball_rect = pygame.Rect(ball.x, ball.y, ball.width, ball.height)
        second_ball_dy = -dy if dy != 0 else random.choice([-1, 1])


    elif booster_name == "increace_paddle_length":
        if dx > 0:
            paddleLeft.height = min(200, paddleLeft.height + 50)
            global increased_paddle_side
            increased_paddle_side = "left"
        else:
            paddleRight.height = min(200, paddleRight.height + 50)
            increased_paddle_side = "right"

    elif booster_name == "paddle_slowDown":
        if dx > 0:  # Мяч движется вправо (замедляем левого игрока)
            paddleLeftSpeed = max(1, paddleLeftSpeed - 3)
        else:  # Мяч движется влево (замедляем правого игрока)
            paddleRightSpeed = max(1, paddleRightSpeed - 3)

    elif booster_name == "paddle_speedUp":
        if dx > 0:  # Мяч движется вправо (ускоряем левого игрока)
            paddleLeftSpeed = min(20, paddleLeftSpeed + 3)  # Максимум 20
        else:  # Мяч движется влево (ускоряем правого игрока)
            paddleRightSpeed = min(20, paddleRightSpeed + 3)  # Максимум 20


def remove_booster_effect(booster_name):
    global paddleLeftSpeed, paddleRightSpeed, paddleHeight, ballRadius, paddleLeft, paddleRight
    global second_ball_active, second_ball_rect

    active_boosters[booster_name] = False
    if booster_name in booster_end_times:
        del booster_end_times[booster_name]

    # Восстанавливаем оригинальные значения
    if booster_name == "ball_smaller":
        ballRadius = original_ball_radius
        ball.width = ball.height = ballRadius * 2

    elif booster_name == "double_ball":
        second_ball_active = False
        second_ball_rect = None

    elif booster_name in ["enemy_slow", "paddle_slowDown", "paddle_speedUp"]:
        paddleLeftSpeed = original_paddle_left_speed
        paddleRightSpeed = original_paddle_right_speed


    elif booster_name == "increace_paddle_length":
        if increased_paddle_side == "left":
            paddleLeft.height = original_paddle_height
        elif increased_paddle_side == "right":
            paddleRight.height = original_paddle_height


def update_boosters():
    """Проверяет и обновляет активные бустеры"""
    global second_ball_active, second_ball_rect, second_ball_dy
    current_time = pygame.time.get_ticks()

    # Обновление движения второго мяча
    if second_ball_active and second_ball_rect and not miniPause and not pause:
        # Движение второго мяча
        second_ball_rect.x += ballSpeed * dx
        second_ball_rect.y += ballSpeed * second_ball_dy

        # Отскок от границ
        if second_ball_rect.top <= 0:
            second_ball_rect.top = 1
            second_ball_dy = -second_ball_dy
        elif second_ball_rect.bottom >= HEIGHT:
            second_ball_rect.bottom = HEIGHT - 1
            second_ball_dy = -second_ball_dy

        # Отскок от ракеток
        if second_ball_rect.colliderect(paddleLeft):
            second_ball_rect.left = paddleLeft.right
            second_ball_dy = -second_ball_dy
        elif second_ball_rect.colliderect(paddleRight):
            second_ball_rect.right = paddleRight.left
            second_ball_dy = -second_ball_dy

    # Проверка времени окончания эффектов
    for booster_name in list(active_boosters.keys()):
        if active_boosters[booster_name]:
            if booster_name == "double_ball" and current_time > second_ball_end_time:
                remove_booster_effect(booster_name)
            elif booster_name != "double_ball" and booster_name in booster_end_times and current_time > \
                    booster_end_times[booster_name]:
                remove_booster_effect(booster_name)

def screen_update(var):
    global WIDTH, HEIGHT, screen, backgroundPhoto, paddleRight, paddleLeft, ball, gameStartTime
    backgroundPhoto1 = backgroundPhoto
    gw = 1200
    gh = 720
    if var == 1 and WIDTH <= gw:
        WIDTH += 15
        screen = pygame.display.set_mode((WIDTH, HEIGHT), vsync=1)
        if backgroundPhoto1:
            backgroundPhoto1 = pygame.transform.scale(backgroundPhoto1, (WIDTH, HEIGHT))
            screen.blit(backgroundPhoto1, (0, 0))
        else:
            screen.fill(black)
        pygame.display.flip()
    elif var == 0 and HEIGHT <= gh:
        HEIGHT += 10
        screen = pygame.display.set_mode((WIDTH, HEIGHT), vsync=1)
        if backgroundPhoto1:
            backgroundPhoto1 = pygame.transform.scale(backgroundPhoto1, (WIDTH, HEIGHT))
            screen.blit(backgroundPhoto1, (0, 0))
        else:
            screen.fill(black)
        pygame.display.flip()
    paddleRight.left = WIDTH - paddleWidth - 5

def startGame():
    global menu_flag, menu_pause, paddleRight
    menu_flag = False
    pygame.mixer.Sound.play(menuSelectSound)
    pygame.time.delay(1000)
    playMusic(gameMusic)
    menu_pause = True

def continueGame():
    global menu_flag_after, menu_pause
    menu_flag_after = False
    pygame.mixer.Sound.play(menuSelectSound)
    pygame.time.delay(1000)
    playMusic(gameMusic)
    menu_pause = True
    paddleRight.left = WIDTH - paddleWidth - 5

def mod_menu():
    global menu_flag, menu_flag_after, mods_flag
    pygame.mixer.Sound.play(menuSwitchSound)
    menu_flag = menu_flag_after  = False
    mods_flag = True

def mod_update(mod_name):
    if mod_name in mods:
        mods[mod_name] = not mods[mod_name]
    toggleSound = pygame.mixer.Sound(resource_path("assets/sounds/MenuSounds/modToggleSound.mp3"))
    toggleSound.set_volume(0.5)
    pygame.mixer.Sound.play(toggleSound)

def help():
    global menu_flag_after, menu_flag, help_flag
    pygame.mixer.Sound.play(menuSwitchSound)
    menu_flag = menu_flag_after =  False
    help_flag = True

def help_mod():
    global help_flag, mods_flag, help_mod_menu_flag, help_mod_menu_flag1
    pygame.mixer.Sound.play(menuSwitchSound)
    help_flag = mods_flag = help_mod_menu_flag1 = False
    help_mod_menu_flag = True

def help_mod1():
    global help_flag, mods_flag, help_mod_menu_flag, help_mod_menu_flag1
    pygame.mixer.Sound.play(menuSwitchSound)
    help_flag = mods_flag = help_mod_menu_flag = False
    help_mod_menu_flag1 = True

def options():
    global menu_flag, menu_flag_after, options_flag
    pygame.mixer.Sound.play(menuSwitchSound)
    menu_flag = menu_flag_after = False
    options_flag = True

def musicVolUp():
    global menuMusicVol, gameMusicVol, Volume
    menuMusicVol = min(1.0, menuMusicVol + Volume)
    gameMusicVol = min(1.0, gameMusicVol + Volume)
    pygame.mixer.Sound.play(menuSwitchSound)
    update_music_volume()

def musicVolDown():
    global menuMusicVol, gameMusicVol, Volume
    menuMusicVol = max(0.0, menuMusicVol - Volume)
    gameMusicVol = max(0.0, gameMusicVol - Volume)
    pygame.mixer.Sound.play(menuSwitchSound)
    update_music_volume()

def resetScore():
    global pointRight, pointLeft
    pointRight = pointLeft = 0
    pygame.mixer.Sound.play(menuSwitchSound)

def resetBackground():
    global backgroundPhoto
    backgroundPhoto = pygame.image.load(resource_path("assets/images/background/TableTennis.png"))
    backgroundPhoto = pygame.transform.scale(backgroundPhoto, (WIDTH, HEIGHT))
    pygame.mixer.Sound.play(menuSwitchSound)

def returnToMenu():
    global menu_flag, menu_flag_after, options_flag, help_flag, mods_flag, help_mod_menu_flag, help_mod_menu_flag1
    menu_flag = options_flag = help_flag = mods_flag = help_mod_menu_flag = help_mod_menu_flag1 = False
    menu_flag_after = True
    pygame.mixer.Sound.play(menuSwitchSound)

def draw_volume_info(screen):
    menu_vol_text = pixel_font_small.render(f'Громкость меню: {int(menuMusicVol * 100)}%', True, yellow)
    game_vol_text = pixel_font_small.render(f'Громкость игры: {int(gameMusicVol * 100)}%', True, yellow)
    screen.blit(menu_vol_text, (100, 300))
    screen.blit(game_vol_text, (100, 320))

def exitGame():
    print("="*40, "\n", " "*5, "|| До скорой встречи! ||")
    print("="*40)
    exitSound = pygame.mixer.Sound(resource_path("assets/sounds/MenuSounds/exitSound.mp3"))
    pygame.mixer.Sound.play(exitSound)
    pygame.time.delay(500)
    pygame.quit()
    sys.exit()

menu = Menu(pixel_font, white)
menu.append_option("Начать игру", startGame)
menu.append_option("Настройки", options)
menu.append_option("Управление", help)
menu.append_option("Моды", mod_menu)
menu.append_option("Выйти", exitGame)

menuAfter = Menu(pixel_font, white)
menuAfter.append_option("Продолжить игру", continueGame)
menuAfter.append_option("Настройки", options)
menuAfter.append_option("Управление", help)
menuAfter.append_option("Моды", mod_menu)
menuAfter.append_option("Выйти", exitGame)

options_menu = Menu(pixel_font_options, lightRed)
options_menu.append_option("Вернуться в меню", returnToMenu)
options_menu.append_option("Увеличить громкость музыки", musicVolUp)
options_menu.append_option("Уменьшить громкость музыки", musicVolDown)
options_menu.append_option("Обновить фон поля", resetBackground)
options_menu.append_option("Сбросить счет", resetScore)

mods_menu = Menu(pixel_font, white)
mods_menu.append_option("Бомбы", lambda : mod_update("bomb_mode"))
mods_menu.append_option("Бустеры ", lambda : mod_update("booster_mode"))
mods_menu.append_option("Живое поле (Багает)", lambda : mod_update("live_field_mode"))
mods_menu.append_option("Пули", lambda : mod_update("bullet_mode"))
mods_menu.append_option("Игра против бота", lambda : mod_update("PVE_mode"))
mods_menu.append_option("Помощь", help_mod)
mods_menu.append_option("Вeрнуться в меню", returnToMenu)

help_menu = Menu(pixel_font, lightBlue)
help_menu.append_option("Вернуться в меню", returnToMenu)
help_menu.append_option("Помощь (моды)", help_mod)

help_mod_menu = Menu(pixel_font, white)
help_mod_menu.append_option("Следующая страница", help_mod1)
help_mod_menu.append_option("Вернуться в меню", returnToMenu)

help_mod_menu1 = Menu(pixel_font, white)
help_mod_menu1.append_option("Предыдущая страница", help_mod)
help_mod_menu1.append_option("Вернуться в меню", returnToMenu)

gameStartTime = pygame.time.get_ticks()
last_shrink_time = 0
last_shrink_time1 = 0
SHRINK_INTERVAL = 500
while game:
    current_time = pygame.time.get_ticks()
    current_time1 = pygame.time.get_ticks()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False

        if event.type == pygame.KEYDOWN:
            if menu_flag_after:
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    menuAfter.switch(1)
                    pygame.mixer.Sound.play(menuSwitchSound)
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    menuAfter.switch(-1)
                    pygame.mixer.Sound.play(menuSwitchSound)
                elif event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    menuAfter.select()
            elif menu_flag:
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    menu.switch(1)
                    pygame.mixer.Sound.play(menuSwitchSound)
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    menu.switch(-1)
                    pygame.mixer.Sound.play(menuSwitchSound)
                elif event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    menu.select()
            elif options_flag:
                if event.key == pygame.K_ESCAPE:
                    returnToMenu()
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    options_menu.switch(1)
                    pygame.mixer.Sound.play(menuSwitchSound)
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    options_menu.switch(-1)
                    pygame.mixer.Sound.play(menuSwitchSound)
                elif event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    options_menu.select()
            elif mods_flag:
                if event.key == pygame.K_ESCAPE:
                    returnToMenu()
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    mods_menu.switch(1)
                    pygame.mixer.Sound.play(menuSwitchSound)
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    mods_menu.switch(-1)
                    pygame.mixer.Sound.play(menuSwitchSound)
                elif event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    mods_menu.select()
            elif help_flag:
                if event.key == pygame.K_ESCAPE:
                    returnToMenu()
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    help_menu.switch(1)
                    pygame.mixer.Sound.play(menuSwitchSound)
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    help_menu.switch(-1)
                    pygame.mixer.Sound.play(menuSwitchSound)
                elif event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    help_menu.select()
            elif help_mod_menu_flag:
                if event.key == pygame.K_ESCAPE:
                    returnToMenu()
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    help_mod_menu.switch(1)
                    pygame.mixer.Sound.play(menuSwitchSound)
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    help_mod_menu.switch(-1)
                    pygame.mixer.Sound.play(menuSwitchSound)
                elif event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    help_mod_menu.select()
            elif help_mod_menu_flag1:
                if event.key == pygame.K_ESCAPE:
                    returnToMenu()
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    help_mod_menu1.switch(1)
                    pygame.mixer.Sound.play(menuSwitchSound)
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    help_mod_menu1.switch(-1)
                    pygame.mixer.Sound.play(menuSwitchSound)
                elif event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    help_mod_menu1.select()
            else:
                if event.key == pygame.K_ESCAPE:
                    menuBG = pygame.transform.scale(random.choice((background1, background2, background3, background4)), (GWIDTH, GHEIGHT))
                    menu_flag_after = True
                    pause = True
                    if menu_flag_after:
                        playMusic(mainMenuMusic)
                if event.key == pygame.K_p:
                    pause = not pause
    if menu_flag_after or menu_flag or options_flag or help_flag or mods_flag or help_mod_menu_flag:
        if GWIDTH != WIDTH or GHEIGHT != HEIGHT:
            WIDTH, HEIGHT = GWIDTH, GHEIGHT
            screen = pygame.display.set_mode((1000, 600), vsync=1)
        clock.tick(20)
        menuSwitchSound = pygame.mixer.Sound(random.choice((resource_path("assets/sounds/MenuSounds/optionSwitch.mp3"),
                                                            resource_path("assets/sounds/MenuSounds/optionSwitch2.mp3"))))
        menuSelectSound = pygame.mixer.Sound(resource_path("assets/sounds/MenuSounds/optionChoose.mp3"))
        playMusic(mainMenuMusic)
        if menuBG:
            screen.blit(menuBG, (0, 0))
        else:
            screen.fill(black)
    elif not menu_flag and not menu_flag_after and not options_flag and not help_flag and not mods_flag and not help_mod_menu_flag and not help_mod_menu_flag1 and currentMusic != gameMusic:
        playMusic(gameMusic)

    if menu_flag_after:
        menuAfter.draw(screen, 50, 30, 60)
        tipText = pixel_font_small.render('Ты уже знаешь, как играть ;p', True, green)
        screen.blit(tipText, (100, HEIGHT-590))

    elif menu_flag:
        menu.draw(screen, 50, 30, 60)
        tipText1 = pixel_font_small.render('"W" и  "S" для навигации в меню', True, white)
        tipText2 = pixel_font_small.render('Enter - выбор', True, white)
        screen.blit(tipText1, (450, 220))
        screen.blit(tipText2, (450, 250))

    elif options_flag:
        screen.blit(optionsMenuBG, (0, 0))
        options_menu.draw(screen, 50, 30, 40)
        draw_volume_info(screen)

    elif mods_flag:
        screen.blit(modsMenuBG, (0, 0))
        mods_menu.draw(screen, 100, 100, 60)
        y_offset = 110
        for i in mods:
            pygame.draw.rect(screen, black, (34, y_offset - 5, 41, 40), 0)
            if mods[i] == False:
                pygame.draw.rect(screen, red, (40, y_offset, 30, 30), 0)
            if mods[i] == True:
                pygame.draw.rect(screen, green, (40, y_offset, 30, 30), 0)
            y_offset += 58
        mod1 = pixel_font.render("Список модов:", True, white)
        screen.blit(mod1, (20, 20))

    elif help_flag:
        screen.blit(helpMenuBG, (0, 0))
        help_menu.draw(screen, 50, 30, 60)
        controls_text = [
            "Управление в игре:",
            "Игрок 1 (слева):",
            "  W - двигать ракетку вверх",
            "  S - двигать ракетку вниз",
            "",
            "Игрок 2 (справа):",
            "  Стрелка ВВЕРХ - двигать ракетку вверх",
            "  Стрелка ВНИЗ - двигать ракетку вниз",
            "",
            "Общее управление:",
            "  ESC - открыть меню",
            "  P - пауза",
            "  Пробел/Enter - выбор в меню"
        ]
        y_offset = 150
        for line in controls_text:
            text_surface = pixel_font_small.render(line, True, pink)
            screen.blit(text_surface, (100, y_offset))
            y_offset += 25
    elif help_mod_menu_flag:
        screen.blit(helpModMenuBG, (0, 0))
        screen.blit(bombSprite, (300, 1))
        screen.blit(boosterSprite1, (400, 50))
        screen.blit(boosterSprite2, (50, 120))
        screen.blit(boosterSprite3, (50, 190))
        screen.blit(boosterSprite4, (50, 260))
        screen.blit(boosterSprite5, (50, 330))
        screen.blit(boosterSprite6, (50, 400))
        text1 = pixel_font.render("Бомбы:", True, white)
        screen.blit(text1, (50, 15))
        text11 = pixel_font_small.render("При попадании по бомбе", True, white)
        text111 = pixel_font_small.render("мяч летит в другую сторону с ускорением", True, white)
        screen.blit(text11, (380, 25))
        screen.blit(text111, (380, 40))

        text2 = pixel_font.render("Бустеры:", True, white)
        screen.blit(text2, (50, 60))
        text21 = pixel_font_options.render("Уменьшает мяч", True, white)
        text22 = pixel_font_options.render("Раздваивает мяч", True, white)
        text23 = pixel_font_options.render("Замедляет ракетку противника", True, white)
        text24 = pixel_font_options.render("Удлиняет ракетку", True, white)
        text25 = pixel_font_options.render("Замедляет ракетку", True, white)
        text26 = pixel_font_options.render("Ускоряет ракетку", True, white)
        screen.blit(text21, (480, 70))
        screen.blit(text22, (130, 140))
        screen.blit(text23, (130, 210))
        screen.blit(text24, (130, 280))
        screen.blit(text25, (130, 350))
        screen.blit(text26, (130, 420))
        help_mod_menu.draw(screen, 50, HEIGHT - 120, 60)

    elif help_mod_menu_flag1:
        screen.blit(helpModMenuBG, (0, 0))
        text3 = pixel_font.render("Живое поле:", True, white)
        screen.blit(text3, (50, 15))
        text31 = pixel_font_small.render("При отскоке мяча", True, white)
        text32 = pixel_font_small.render("меняется размер экрана", True, white)
        screen.blit(text31, (545, 25))
        screen.blit(text32, (545, 40))

        text4 = pixel_font.render("Пули:", True, white)
        screen.blit(text4, (50, 80))
        pygame.draw.circle(screen, black,(320, 100),10)
        pygame.draw.rect(screen, yellow, (280, 90, 40, 20))
        pygame.draw.rect(screen, orange, (280, 98, 15, 5))
        text41 = pixel_font_small.render("Пули летят в ракетки,", True, white)
        text42 = pixel_font_small.render("в кого попадет - тому гол", True, white)
        screen.blit(text41, (350, 80))
        screen.blit(text42, (350, 105))

        text5 = pixel_font_options.render("Игра против бота:", True, white)
        screen.blit(text5, (50, 145))
        text51 = pixel_font_small.render("Обычный PVE - режим", True, white)
        screen.blit(text51, (565, 152))
        help_mod_menu1.draw(screen, 50, HEIGHT - 120, 60)

    else:
        goalSound = pygame.mixer.Sound(random.choice((resource_path("assets/sounds/GameSounds/goalSound1.mp3"),
                                                      resource_path("assets/sounds/GameSounds/goalSound2.mp3"),
                                                      resource_path("assets/sounds/GameSounds/goalSound3.mp3"))))
        goalSound.set_volume(0.2)
        BallPaddle = pygame.mixer.Sound(random.choice((resource_path("assets/sounds/GameSounds/BallPaddle1.mp3"),
                                                       resource_path("assets/sounds/GameSounds/BallPaddle2.mp3"),
                                                       resource_path("assets/sounds/GameSounds/BallPaddle3.mp3"),
                                                       resource_path("assets/sounds/GameSounds/BallPaddle4.mp3"))))
        BallPaddle.set_volume(0.3)
        BallTable = pygame.mixer.Sound(resource_path("assets/sounds/GameSounds/BallTable.mp3"))
        BallTable.set_volume(0.3)

        gameTimeCounter = pygame.time.get_ticks()
        gameMinutes = gameTimeCounter // 1000 // 60
        gameSeconds = gameTimeCounter // 1000 % 60
        gameMiliseconds = (gameTimeCounter // 100) % 10

        currentGameTime = pygame.time.get_ticks() - gameStartTime
        matchMinutes = currentGameTime // 1000 // 60
        matchSeconds = currentGameTime // 1000 % 60
        matchMiliseconds = (currentGameTime // 100) % 10

        if backgroundPhoto:
            screen.blit(backgroundPhoto, (0, 0))
        else:
            screen.fill(black)

        if not pause:
            # currentGameTime = pygame.time.get_ticks()
            # matchMinutes = currentGameTime // 1000 // 60
            # matchSeconds = currentGameTime // 1000 % 60
            # matchMiliseconds = (currentGameTime // 100) % 10

            key = pygame.key.get_pressed()

            if mods["PVE_mode"] == False:
                if key[pygame.K_UP] and paddleRight.top > 0:
                    paddleRight.top -= paddleRightSpeed
                if key[pygame.K_DOWN] and paddleRight.bottom < HEIGHT:
                    paddleRight.top += paddleRightSpeed

            else:
                if paddleRight.top < 0:
                    paddleRight.top = 5
                if paddleRight.bottom > HEIGHT:
                    paddleRight.bottom = HEIGHT - 5


                if mods["bullet_mode"]:
                    dangerBullet = None
                    bulletyDirection = 0
                    waitTimer = 0
                    if len(bullets) > 0 and dangerBullet is None:
                        for bullet in bullets:
                            if bullet.rect.right > GWIDTH * 0.85:
                                dangerBullet = bullet
                                bulletyDirection = -1 if bullet.dy < 0 else 1
                                break
                    if dangerBullet is not None:
                        if ((dangerBullet.rect.bottom < paddleRight.top - 40) or (dangerBullet.rect.top > paddleRight.bottom + 40)) and dangerBullet.rect.right < GWIDTH * 0.7:# or bullet.rect.left > GWIDTH - 5:
                            if ball.centery > paddleRight.centery + 25:
                                paddleRight.top += paddleRightSpeed
                            if ball.centery < paddleRight.centery - 25:
                                paddleRight.top -= paddleRightSpeed
                        else:
                            if dangerBullet.rect.center[1] < 135 and paddleRight.centery < HEIGHT / 3:
                                paddleRight.top += paddleRightSpeed
                                # print("Уклоняюсь вниз (из за положения пули)")
                                # pygame.time.wait(200)
                            elif dangerBullet.rect.center[1] > HEIGHT - 135 and paddleRight.centery > HEIGHT * 0.67:
                                paddleRight.top -= paddleRightSpeed
                                # print("Уклоняюсь вверх (из за положения пули)")
                                # pygame.time.wait(200)
                            else:
                                paddleRight.top += paddleRightSpeed * bulletyDirection * (-1)
                                # print("Уклоняюсь противоположно пуле")
                                # pygame.time.wait(200)


                    else:
                        if ball.centery > paddleRight.centery + 25:
                            paddleRight.top += paddleRightSpeed
                        if ball.centery < paddleRight.centery - 25:
                            paddleRight.top -= paddleRightSpeed
                else:
                    if ball.centery > paddleRight.centery + 25:
                        paddleRight.top += paddleRightSpeed
                    if ball.centery < paddleRight.centery - 25:
                        paddleRight.top -= paddleRightSpeed

            if key[pygame.K_w] and paddleLeft.top > 0:
                paddleLeft.top -= paddleLeftSpeed
            if key[pygame.K_s] and paddleLeft.bottom < HEIGHT:
                paddleLeft.top += paddleLeftSpeed

            ball.x += ballSpeed * dx
            ball.y += ballSpeed * dy

            if WIDTH > GWIDTH:
                if current_time - last_shrink_time >= SHRINK_INTERVAL / 3:
                    WIDTH = max(GWIDTH, WIDTH - 1)
                    screen = pygame.display.set_mode((WIDTH, HEIGHT), vsync=1)
                    if backgroundPhoto:
                        screen.blit(backgroundPhoto, (0, 0))
                    else:
                        screen.fill(black)
                    pygame.display.flip()
                    paddleRight.left = WIDTH - paddleWidth - 5
                    backgroundPhoto = pygame.transform.scale(backgroundPhoto, (WIDTH, HEIGHT))
                    last_shrink_time = current_time

            if HEIGHT > GHEIGHT:
                if current_time1 - last_shrink_time1 >= SHRINK_INTERVAL/3:
                    HEIGHT = max(GHEIGHT, HEIGHT - 1)
                    screen = pygame.display.set_mode((WIDTH, HEIGHT), vsync=1)
                    if backgroundPhoto:
                        screen.blit(backgroundPhoto, (0, 0))
                    else:
                        screen.fill(black)
                    pygame.display.flip()
                    paddleRight.left = WIDTH - paddleWidth - 5
                    backgroundPhoto = pygame.transform.scale(backgroundPhoto, (WIDTH, HEIGHT))
                    last_shrink_time1 = current_time

        if ball.centery < ballRadius:
            if mods["live_field_mode"] == True:
                screen_update(0)
            if mods["bullet_mode"]:
                bullet_spawn += 1
                if bullet_spawn % 4 == 0:
                    bullets.append(Bullet(4, WIDTH//2, HEIGHT//2, dx))
                    ShootSound = pygame.mixer.Sound(resource_path("assets/sounds/GameSounds/modSounds/Shoot_sound.mp3"))
                    ShootSound.set_volume(0.1)
                    pygame.mixer.Sound.play(ShootSound)
            ball.y += 1
            dy = -dy
            pygame.mixer.Sound.play(BallTable)
        if ball.centery > HEIGHT:
            if mods["live_field_mode"] == True:
                screen_update(0)
            if mods["bullet_mode"]:
                bullet_spawn += 1
                if bullet_spawn % 4 == 0:
                    bullets.append(Bullet(4, WIDTH//2, HEIGHT//2, dx))
                    ShootSound = pygame.mixer.Sound(resource_path("assets/sounds/GameSounds/modSounds/Shoot_sound.mp3"))
                    ShootSound.set_volume(0.1)
                    pygame.mixer.Sound.play(ShootSound)
            ball.y -= 1
            dy = -dy
            pygame.mixer.Sound.play(BallTable)
        current_time = pygame.time.get_ticks()
        if current_time > boost_remove_time and boost_remove_time > 0 and not miniPause:
            if dx > 0:
                dx -= boost_added
            else:
                dx += boost_added

            boost_added = 0.0
            boost_remove_time = 0
        if mods["bullet_mode"]:
            bullets_to_remove = []

            for i, bullet in enumerate(bullets) :
                bullet.draw(screen)

                if not pause:
                     # Двигаем пулю и проверяем, нужно ли ее удалить
                     if bullet.move():
                         bullets_to_remove.append(i)
                         continue

                     # Проверяем столкновения с ракетками
                     if bullet.rect.colliderect(paddleLeft):
                         BulletHitSound = pygame.mixer.Sound(
                             resource_path("assets/sounds/GameSounds/modSounds/bulletHitSound.mp3"))
                         BulletHitSound.set_volume(0.1)
                         pygame.mixer.Sound.play(BulletHitSound)
                         looserFlag = 1
                         dx = 0
                         dy = 0
                         pointRight += 1
                         pygame.mixer.Sound.play(goalSound)
                         ball.x = WIDTH // 2
                         ball.y = HEIGHT // 2
                         goalTime = pygame.time.get_ticks()
                         miniPause = True
                         bullets_to_remove.append(i)
                         continue

                     if bullet.rect.colliderect(paddleRight):
                         BulletHitSound = pygame.mixer.Sound(
                             resource_path("assets/sounds/GameSounds/modSounds/bulletHitSound.mp3"))
                         BulletHitSound.set_volume(0.1)
                         pygame.mixer.Sound.play(BulletHitSound)
                         looserFlag = -1
                         dx = 0
                         dy = 0
                         pointLeft += 1
                         pygame.mixer.Sound.play(goalSound)
                         ball.x = WIDTH // 2
                         ball.y = HEIGHT // 2
                         goalTime = pygame.time.get_ticks()
                         miniPause = True
                         bullets_to_remove.append(i)
                         continue

            # Удаляем помеченные пули
            for i in sorted(bullets_to_remove, reverse=True):
                if i < len(bullets):
                    del bullets[i]

        for booster in boosters[:]:
            booster.draw(screen)
            if booster.check_collision(ball):
                apply_booster_effect(booster.name)
                boosterSound = pygame.mixer.Sound(
                    resource_path(f"assets/sounds/GameSounds/modSounds/{booster.name}.mp3"))
                boosterSound.set_volume(0.1)
                pygame.mixer.Sound.play(boosterSound)
                boosters.remove(booster)
                break

        if not miniPause and not pause:
            update_boosters()

        if active_boosters.get("double_ball", False) and second_ball_rect:
            pygame.draw.circle(screen, (white), second_ball_rect.center, ballRadius)

        # Отрисовка основного мяча
        ball.width = ball.height = ballRadius * 2
        pygame.draw.circle(screen, lightgray, ball.center, ballRadius)
        for bomb in bombs[:]:
            bomb.draw(screen)
            if bomb.check_collision(ball):
                current_time = pygame.time.get_ticks()
                dx = -dx
                if dx > 0 and not miniPause:
                    dx += 0.25
                if dx < 0 and not miniPause:
                    dx -= 0.25
                boost_added = 0.2
                boost_remove_time = current_time + 1000
                bombs.remove(bomb)
                explosionSound = pygame.mixer.Sound(resource_path("assets/sounds/GameSounds/modSounds/explosion.mp3"))
                explosionSound.set_volume(0.1)
                pygame.mixer.Sound.play(explosionSound)
                break
        if mods["bomb_mode"] and not miniPause:
            if 0 < dx < 1:
                dx = 1
            if -1 < dx < 0:
                dx = -1
            if dx > 2.2:
                dx=2.2
            if dx < -2.2:
                dx = -2.2
        if ball.colliderect(paddleLeft) or ball.colliderect(paddleRight):
            if mods["booster_mode"]:
                if counterForBooster % 4 == 0:
                    rand = random.randint(1, 6)
                    if rand == 1:
                        boosters.append( Booster("ball_smaller",screen, resource_path("assets/images/Sprites/ball_smaller.png")))
                    if rand == 2:
                        boosters.append(Booster("double_ball",screen, resource_path("assets/images/Sprites/doubleBall.png")))
                    if rand == 3:
                        boosters.append(Booster("enemy_slow",screen, resource_path("assets/images/Sprites/enemy_slow.png")))
                    if rand == 4:
                        boosters.append(Booster("increace_paddle_length",screen, resource_path("assets/images/Sprites/increace_paddle_length.png")))
                    if rand == 5:
                        boosters.append(Booster("paddle_slowDown",screen, resource_path("assets/images/Sprites/paddle_slowDown.png")))
                    if rand == 6:
                        boosters.append(Booster("paddle_speedUp",screen, resource_path("assets/images/Sprites/paddle_speedUp.png")))
                counterForBooster += 1
            if mods["bomb_mode"]:
                if 0 < dx < 1:
                    dx = 1
                if -1 < dx < 0:
                    dx = -1
                if counterForBomb % 4 == 0:
                    bombs.append(Bomb(screen, resource_path("assets/images/Sprites/bomb (1).png")))
                counterForBomb += 1
            if mods["live_field_mode"] == True:
                screen_update(1)
            if -1.6 < dy < -0.8:
                dyRand = random.choice(dyChangesMinus)
                if -1.6 < dy - dyRand < -0.8:
                    dy -= dyRand
            if 1.6 > dy > 0.8:
                dyRand = random.choice(dyChangesPlus)
                if 1.6 > dy + dyRand > 0.8:
                    dy += dyRand
            if ball.colliderect(paddleLeft):
                ball.left = paddleLeft.right
            else:
                ball.right = paddleRight.left
            if -2 < dx < 2:
                dx = -dx + -dx * 0.005
            else:
                dx = -dx
            pygame.mixer.Sound.play(BallPaddle)

        if ball.centerx < ballRadius:
            looserFlag = 1
            dx = 0
            dy = 0
            pointRight += 1
            pygame.mixer.Sound.play(goalSound)
            ball.x = WIDTH // 2
            ball.y = HEIGHT // 2
            goalTime = pygame.time.get_ticks()
            miniPause = True

        if ball.centerx > WIDTH:
            looserFlag = -1
            dx = 0
            dy = 0
            pointLeft += 1
            pygame.mixer.Sound.play(goalSound)
            ball.x = WIDTH // 2
            ball.y = HEIGHT // 2
            goalTime = pygame.time.get_ticks()
            miniPause = True

        if miniPause:
            if miniPause:
                for booster_name in list(active_boosters.keys()):
                    if active_boosters[booster_name]:
                        remove_booster_effect(booster_name)
                boosters.clear()

            if mods["bullet_mode"]:
                for i in sorted(bullets_to_remove, reverse=True):
                    if i < len(bullets):
                        del bullets[i]

            for bullet in bullets:
                bullets.remove(bullet)
            for bomb in bombs:
                bombs.remove(bomb)

            gameStartTime = pygame.time.get_ticks()
            time = pygame.time.get_ticks()
            if time - goalTime > 1000:
                miniPause = False
                dy = random.choice((1, -1))
                dx = looserFlag

        if pause:
            pauseFont = ARIAL_50.render("ПАУЗА", True, lightRed)
            pauseRect = pauseFont.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(pauseFont, pauseRect)

        pygame.draw.rect(screen, lightRed, paddleLeft)
        pygame.draw.rect(screen, lightBlue, paddleRight)
        ball.width = ball.height = ballRadius * 2
        pygame.draw.circle(screen, lightgray, ball.center, ballRadius)

        gameTipText = smallFont.render("ESC - меню, P - пауза", True, white)
        screen.blit(gameTipText, (200, HEIGHT - 30))

        rightText = font.render("Игрок 2:", True, yellow)
        screen.blit(rightText, (WIDTH - 200, 5))
        leftText = font.render("Игрок 1:", True, yellow)
        screen.blit(leftText, (50, 5))

        rightPoints = font.render(f"{pointRight}", True, lightBlue)
        screen.blit(rightPoints, (WIDTH - 50, 5))
        leftPoints = font.render(f"{pointLeft}", True, lightRed)
        screen.blit(leftPoints, (200, 5))

        dxSpeed = smallFont.render(f"s_x : {dx:.2f}", True, white)
        screen.blit(dxSpeed, (25, HEIGHT - 40))
        dySpeed = smallFont.render(f"s_y : {dy:.2f}", True, white)
        screen.blit(dySpeed, (25, HEIGHT - 20))
        # screenw = smallFont.render(f"W : {WIDTH}", True, white)
        # screen.blit(screenw, (WIDTH // 2, 40))
        # screenh = smallFont.render(f"H : {HEIGHT}", True, white)
        # screen.blit(screenh, (WIDTH // 2, 60))

        matchTimeCounter = smallFont.render(f"Время раунда: {matchMinutes}.{matchSeconds}.{matchMiliseconds}", True,
                                            white)
        screen.blit(matchTimeCounter, (WIDTH - 380, HEIGHT - 40))
        gameTimeCounter = smallFont.render(f"Время игры :    {gameMinutes}.{gameSeconds}.{gameMiliseconds}", True,
                                           white)
        screen.blit(gameTimeCounter, (WIDTH - 380, HEIGHT - 20))

    pygame.display.flip()
    clock.tick(fps)
pygame.quit()

# Доработать чтобы когда мяч забивал он летел от того, кому забили (Сделано)
# Реализовать паузу через esc (Сделано)
# Добавить при продолжении игры паузу (Сделано)
# Пофиксить баг с дрожанием мяча внутри ракетки (Сделано)
# Пофиксить баг с паузой
# L пофиксить баг с паузой и временем раунда
#                                   L игры
# Добавить мини паузу при продолжении/начале игры
# Сделать меню (По большей части сделано)
# |
# L   Игроки выбирают макс счет, время всей игры и имена
# L   Сделать настройки
#       L громкость музыки (Сделано)
#       L скорость мяча
#       L скорость игрока
#       L громкость звуков
#
# Сделать оптимизацию (Сделано)
# |
# L добавить ограничения по FPS (Сделано)
# Переписать игру через классы (мяч, игроки как минимум) (Сделано)
# Сделать меню - описание модов (Сделано)
# Сделать моды (Сделано!!!)
# |
# L При отскоке мяча увеличивать ширину/длину экрана (Сделано)
# L Спавн бомб (Сделано)
# L Изменение характеристик ракеток и мяча, пикапы, бустеры, бонусы и тп (Сделано)
#                               L сделать моргание увеличенной части
# Сделать так, чтобы защитник Defender не ругался
# Сделать боту уклонение от пуль(Сделано базовое)
# |
# L Бот уклонятеся от пули (сделано)
# L Бот вычисляет траекторрии полета пули + мяча и выбирает лучший вариант