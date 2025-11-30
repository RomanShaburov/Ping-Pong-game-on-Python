import pygame
import random
from Colors import *
from Menu import Menu
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
pixel_font = pygame.font.Font(resource_path("assets/fonts/PressStart2P-Regular.ttf"), 50)
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

WIDTH = 1000
HEIGHT = 600

paddleHeight = 150
paddleWidth = 15
paddleSpeed = 10

ballRadius = 10
ballSpeed = 10
ballD = ballRadius*2

backgroundPhoto = pygame.image.load(resource_path("assets/images/background/TableTennis.png"))
backgroundPhoto = pygame.transform.scale(backgroundPhoto, (WIDTH, HEIGHT))
gameMusic = resource_path("assets/music/Lumber Tycoon 2 Main Biome Theme.mp3")
gameMusicVol = 0.1
mainMenuMusic = resource_path("assets/music/uglyburger0_-_3008s_friday_theme_except_its_crunchy_74565571.mp3")
menuMusicVol = 0.05

background1 = pygame.image.load(resource_path("assets/images/background/menuBG.jpg"))
background2 = pygame.image.load(resource_path("assets/images/background/MenuBG1.jpg"))
background3 = pygame.image.load(resource_path("assets/images/background/MenuBG2.jpg"))
background4 = pygame.image.load(resource_path("assets/images/background/MenuBG3.jpg"))
optionsMenuBG = pygame.image.load(resource_path("assets/images/background/optionsMenuBG.jpg"))
optionsMenuBG = pygame.transform.scale(optionsMenuBG, (WIDTH, HEIGHT))
helpMenuBG = pygame.image.load(resource_path("assets/images/background/helpmenuBG.jpg"))
helpMenuBG = pygame.transform.scale(helpMenuBG, (WIDTH, HEIGHT))
menuBG = pygame.transform.scale(background1, (WIDTH, HEIGHT))

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

pointLeft = 0
pointRight = 0

ballStartX = WIDTH//2-ballRadius
ballStartY = HEIGHT//2-ballRadius

paddleRight = pygame.Rect(WIDTH-paddleWidth-5, HEIGHT/2-paddleHeight/2, paddleWidth, paddleHeight)
paddleLeft = pygame.Rect(5, HEIGHT/2-paddleHeight/2, paddleWidth, paddleHeight)

fps = 60
screen = pygame.display.set_mode((WIDTH, HEIGHT), vsync = 1 )

ball = pygame.Rect(ballStartX, ballStartY, ballD, ballD)
dxStart = 1
dyStart = 1
dyChangesPlus = [0.1, 0.09, 0.08, 0.08, 0.07, 0.06, 0.05, 0.04, 0.03, 0.02, 0.01]
dyChangesMinus = [-0.1, -0.09, -0.08, -0.08, -0.07, -0.06, -0.05, -0.04, -0.03, -0.02, -0.01]
dx = 1
dy = -1

clock = pygame.time.Clock()
pygame.display.set_caption("My Ping-Pong")
icon = load_and_prepare_icon("assets/icons/icon.ico")
pygame.display.set_icon(icon)

Volume = 0.05
miniPause = False
pauseFlag = False
pause = False
game = True
menu_flag = True
menu_flag_after = False
options_flag = False
help_flag = False

def startGame():
    global menu_flag, pause
    menu_flag = False
    pygame.mixer.Sound.play(menuSelectSound)
    pygame.time.delay(1000)
    playMusic(gameMusic)

def continueGame():
    global menu_flag_after, pause
    menu_flag_after = False
    pygame.mixer.Sound.play(menuSelectSound)
    pygame.time.delay(1000)
    playMusic(gameMusic)
    pause = True

def help():
    global menu_flag_after, menu_flag, help_flag, options_flag
    pygame.mixer.Sound.play(menuSwitchSound)
    menu_flag = menu_flag_after = options_flag = False
    help_flag = True

def options():
    global menu_flag, menu_flag_after, options_flag
    pygame.mixer.Sound.play(menuSwitchSound)
    menu_flag = menu_flag_after = False
    options_flag = True

def musicVolUp():
    global menuMusicVol, gameMusicVol, Volume
    menuMusicVol = min(1.0, menuMusicVol + Volume)
    gameMusicVol = min(1.0, gameMusicVol + Volume)
    update_music_volume()

def musicVolDown():
    global menuMusicVol, gameMusicVol, Volume
    menuMusicVol = max(0.0, menuMusicVol - Volume)
    gameMusicVol = max(0.0, gameMusicVol - Volume)
    update_music_volume()

def returnToMenu():
    global menu_flag, menu_flag_after, options_flag, help_flag
    menu_flag = options_flag = help_flag = False
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
menu.append_option("Помощь", help)
menu.append_option("Выйти", exitGame)

options_menu = Menu(pixel_font_options, lightRed)
options_menu.append_option("Вернуться в меню", returnToMenu)
options_menu.append_option("Увеличить громкость музыки", musicVolUp)
options_menu.append_option("Уменьшить громкость музыки", musicVolDown)

help_menu = Menu(pixel_font, lightBlue)
help_menu.append_option("Вернуться в меню", returnToMenu)

menuAfter = Menu(pixel_font, white)
menuAfter.append_option("Продолжить игру", continueGame)
menuAfter.append_option("Настройки", options)
menuAfter.append_option("Помощь", help)
menuAfter.append_option("Выйти", exitGame)

gameStartTime = pygame.time.get_ticks()
while game:
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
            else:
                if event.key == pygame.K_ESCAPE:
                    menuBG = pygame.transform.scale(random.choice((background1, background2, background3, background4)), (WIDTH, HEIGHT))
                    menu_flag_after = True
                    pause = not pause
                    if menu_flag_after:
                        playMusic(mainMenuMusic)
                if event.key == pygame.K_p:
                    pause = not pause

    if menu_flag_after or menu_flag or options_flag or help_flag:
        clock.tick(20)
        menuSwitchSound = pygame.mixer.Sound(random.choice((resource_path("assets/sounds/MenuSounds/optionSwitch.mp3"),
                                                            resource_path("assets/sounds/MenuSounds/optionSwitch2.mp3"))))
        menuSelectSound = pygame.mixer.Sound(resource_path("assets/sounds/MenuSounds/optionChoose.mp3"))
        playMusic(mainMenuMusic)
        if menuBG:
            screen.blit(menuBG, (0, 0))
        else:
            screen.fill(black)
    elif not menu_flag and not menu_flag_after and not options_flag and not help_flag and currentMusic != gameMusic:
        playMusic(gameMusic)

    if menu_flag_after:
        menuAfter.draw(screen, 50, 50, 75)
        tipText = pixel_font_small.render('Ты уже знаешь, как играть ;p', True, green)
        screen.blit(tipText, (100, HEIGHT-580))

    elif menu_flag:
        menu.draw(screen, 50, 50, 75)
        tipText1 = pixel_font_small.render('"W" и  "S" для навигации в меню', True, white)
        tipText2 = pixel_font_small.render('Enter - выбор', True, white)
        screen.blit(tipText1, (450, 220))
        screen.blit(tipText2, (450, 250))

    elif options_flag:
        screen.blit(optionsMenuBG, (0, 0))
        options_menu.draw(screen, 50, 30, 40)
        draw_volume_info(screen)

    elif help_flag:
        screen.blit(helpMenuBG, (0, 0))
        help_menu.draw(screen, 50, 30, 40)
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
        y_offset = 100
        for line in controls_text:
            text_surface = pixel_font_small.render(line, True, pink)
            screen.blit(text_surface, (100, y_offset))
            y_offset += 25

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
            if key[pygame.K_UP] and paddleRight.top > 0:
                paddleRight.top -= paddleSpeed
            if key[pygame.K_DOWN] and paddleRight.bottom < HEIGHT:
                paddleRight.top += paddleSpeed

            if key[pygame.K_w] and paddleLeft.top > 0:
                paddleLeft.top -= paddleSpeed
            if key[pygame.K_s] and paddleLeft.bottom < HEIGHT:
                paddleLeft.top += paddleSpeed

            ball.x += ballSpeed * dx
            ball.y += ballSpeed * dy

        if ball.centery < ballRadius:
            ball.y += 1
            dy = -dy
            pygame.mixer.Sound.play(BallTable)
        if ball.centery > HEIGHT:
            ball.y -= 1
            dy = -dy
            pygame.mixer.Sound.play(BallTable)

        if ball.colliderect(paddleLeft) or ball.colliderect(paddleRight):
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
            ball.x = ballStartX
            ball.y = ballStartY
            goalTime = pygame.time.get_ticks()
            miniPause = True

        if ball.centerx > WIDTH:
            looserFlag = -1
            dx = 0
            dy = 0
            pointLeft += 1
            pygame.mixer.Sound.play(goalSound)
            ball.x = ballStartX
            ball.y = ballStartY
            goalTime = pygame.time.get_ticks()
            miniPause = True

        if miniPause:
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
        pygame.draw.circle(screen, white, ball.center, ballRadius)

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
# Пофиксить баг с паузой (Сделано)
# L пофиксить баг с паузой и временем раунда
#                                   L игры
# Добавить мини паузу при продолжении/начале игры
# Сделать меню (По большей части сделано)
# |
# L   Игроки выбирают макс счет, время всей игры и имена
# L   Сделать настройки (громкость музыки, скорость мяча и игрока и тп)
# Сделать оптимизацию (50%/100%)
# |
# L добавить ограничения по FPS (Сделано)
# L переписать игру через классы (мяч, игроки как минимум)
# Сделать моды
# L При отскоке мяча увеличивать ширину/длину экрана
# L Спавн бомб
# L Изменение характеристик ракеток и мяча, пикапы, бустеры, бонусы и тп