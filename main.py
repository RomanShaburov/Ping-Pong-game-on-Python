import pygame
import random
from Colors import *

pygame.init()
pygame.mixer.init()

font = pygame.font.Font(None, 50)
smallFont = pygame.font.Font(None, 25)
ARIAL_50 = pygame.font.SysFont('arial', 74)
pixel_font = pygame.font.Font("Fonts/PressStart2P-Regular.ttf", 50)
pixel_font_small = pygame.font.Font("Fonts/PressStart2P-Regular.ttf", 15)

class Menu:
    def __init__(self):
        self._option_surfaces = []
        self._callbacks = []
        self._current_option_index = 0

    def append_option(self, option, callback):
        self._option_surfaces.append(pixel_font.render(option, True, white))
        self._callbacks.append(callback)

    def switch(self, direction):
        self._current_option_index = max(0, min(self._current_option_index + direction, len(self._option_surfaces) - 1))

    def select(self):
        self._callbacks[self._current_option_index]()

    def draw(self, surf, x, y, option_y_padding):
        for i, option in enumerate(self._option_surfaces):
            option_rect = option.get_rect()
            option_rect.topleft = (x, y + i * option_y_padding)
            if i == self._current_option_index:
                pygame.draw.rect(surf, green, option_rect)
            surf.blit(option, option_rect)

WIDTH = 1000
HEIGHT = 600

paddleHeight = 150
paddleWidth = 15
paddleSpeed = 10

ballRadius = 10
ballSpeed = 10
ballD = ballRadius*2

backgroundPhoto = pygame.image.load("Images/TableTennis.png")
backgroundPhoto = pygame.transform.scale(backgroundPhoto, (WIDTH, HEIGHT))
gameMusic = "Game Sounds/music/Lumber Tycoon 2 Main Biome Theme.mp3"
mainMenuMusic = "Game Sounds/music/uglyburger0_-_3008s_friday_theme_except_its_crunchy_74565571.mp3"

background1 = pygame.image.load("Images/Background/menuBG.jpg")
background2 = pygame.image.load("Images/Background/MenuBG1.jpg")
background3 = pygame.image.load("Images/Background/MenuBG2.jpg")
background4 = pygame.image.load("Images/Background/MenuBG3.jpg")
menuBG = pygame.transform.scale(background1, (WIDTH, HEIGHT))

currentMusic = None
def playMusic(musicFile):
    global currentMusic
    if musicFile != currentMusic:
        pygame.mixer.music.load(musicFile)
        if musicFile == mainMenuMusic:
            pygame.mixer.music.set_volume(0.1)
        else:
            pygame.mixer.music.set_volume(0.05)
        pygame.mixer.music.play(-1)
        currentMusic = musicFile

playMusic(mainMenuMusic)

WelcomeSound = pygame.mixer.Sound("Game Sounds/sounds/MenuSounds/welcomeSound.mp3")
WelcomeSound.set_volume(0.1)
pygame.mixer.Sound.play(WelcomeSound)

pointLeft = 0
pointRight = 0

ballStartX = WIDTH//2-ballRadius
ballStartY = HEIGHT//2-ballRadius

paddleRight = pygame.Rect(WIDTH-paddleWidth-5, HEIGHT/2-paddleHeight/2, paddleWidth, paddleHeight)
paddleLeft = pygame.Rect(5, HEIGHT/2-paddleHeight/2, paddleWidth, paddleHeight)

fps = 60
screen = pygame.display.set_mode((WIDTH, HEIGHT))

ball = pygame.Rect(ballStartX, ballStartY, ballD, ballD)
dxStart = 1
dyStart = 1
dyChangesPlus = [0.1, 0.09, 0.08, 0.08, 0.07, 0.06, 0.05, 0.04, 0.03, 0.02, 0.01]
dyChangesMinus = [-0.1, -0.09, -0.08, -0.08, -0.07, -0.06, -0.05, -0.04, -0.03, -0.02, -0.01]
dx = 1
dy = -1

clock = pygame.time.Clock()

pygame.display.set_caption("My Ping-Pong")

miniPause = False
pauseFlag = False
pause = True
game = True
menu_flag = True
menu_flag_after = False

def startGame():
    global pause
    global menu_flag
    menu_flag = False
    pause = not pause
    playMusic(mainMenuMusic)

def continueGame():
    global menu_flag_after
    menu_flag_after = False
    playMusic(gameMusic)

def exitGame():
    print("="*40, "\n", " "*5, "|| До скорой встречи! ||")
    print("="*40)
    exitSound = pygame.mixer.Sound("Game Sounds/sounds/MenuSounds/exitSound.mp3")
    pygame.mixer.Sound.play(exitSound)
    pygame.time.delay(500)
    pygame.quit()
    exit()

menu = Menu()
menu.append_option("Начать игру", startGame)
menu.append_option("Выйти", exitGame)

menuAfter = Menu()
menuAfter.append_option("Продолжить игру", continueGame)
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
                elif event.key == pygame.K_SPACE:
                    menuAfter.select()
                    pygame.mixer.Sound.play(menuSelectSound)
            elif menu_flag:
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    menu.switch(1)
                    pygame.mixer.Sound.play(menuSwitchSound)
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    menu.switch(-1)
                    pygame.mixer.Sound.play(menuSwitchSound)
                elif event.key == pygame.K_SPACE:
                    menu.select()
                    pygame.mixer.Sound.play(menuSelectSound)
            else:
                if event.key == pygame.K_ESCAPE:
                    menuBG = pygame.transform.scale(random.choice((background1, background2, background3, background4)), (WIDTH, HEIGHT))
                    menu_flag_after = True
                    pause = not pause
                    if menu_flag_after:
                        playMusic(mainMenuMusic)
                if event.key == pygame.K_p:
                    pause = not pause

    if menu_flag_after or menu_flag:
        menuSwitchSound = pygame.mixer.Sound(random.choice(("Game Sounds/sounds/MenuSounds/optionSwitch.mp3",
                                                            "Game Sounds/sounds/MenuSounds/optionSwitch2.mp3")))
        menuSelectSound = pygame.mixer.Sound("Game Sounds/sounds/MenuSounds/optionChoose.mp3")
        playMusic(mainMenuMusic)
        if menuBG:
            screen.blit(menuBG, (0, 0))
        else:
            screen.fill(black)
    elif not menu_flag and not menu_flag_after and currentMusic != gameMusic:
        playMusic(gameMusic)

    if menu_flag_after:
        menuAfter.draw(screen, 100, 100, 75)

        tipText = pixel_font_small.render('Ты уже знаешь, как играть ;p', True, green)
        screen.blit(tipText, (100, HEIGHT-550))
    elif menu_flag:
        menu.draw(screen, 100, 100, 75)

        tipText1 = pixel_font_small.render('Стрелки "ВВЕРХ" и "ВНИЗ"|для навигации в меню', True, white)
        tipText2 = pixel_font_small.render('Клавиши   "W"   и  "S"  |для навигации в меню', True, white)
        tipText3 = pixel_font_small.render('Пробел - выбор', True, white)
        screen.blit(tipText1, (100, 240))
        screen.blit(tipText2, (100, 270))
        screen.blit(tipText3, (100, 300))
    else:
        goalSound = pygame.mixer.Sound(random.choice(("Game Sounds/sounds/GameSounds/goalSound1.mp3",
                                                      "Game Sounds/sounds/GameSounds/goalSound2.mp3",
                                                      "Game Sounds/sounds/GameSounds/goalSound3.mp3")))
        goalSound.set_volume(0.2)
        BallPaddle = pygame.mixer.Sound(random.choice(("Game Sounds/sounds/GameSounds/BallPaddle1.mp3",
                                                       "Game Sounds/sounds/GameSounds/BallPaddle2.mp3",
                                                       "Game Sounds/sounds/GameSounds/BallPaddle3.mp3",
                                                       "Game Sounds/sounds/GameSounds/BallPaddle4.mp3")))
        BallPaddle.set_volume(0.3)
        BallTable = pygame.mixer.Sound("Game Sounds/sounds/GameSounds/BallTable.mp3")
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

            # currentGameTime = pygame.time.get_ticks() - gameStartTime
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
            if -2 < dy < -0.8:
                dyRand = random.choice(dyChangesMinus)
                if -2 < dy - dyRand < -0.8:
                    dy -= dyRand
            if 2 > dy > 0.8:
                dyRand = random.choice(dyChangesPlus)
                if 2 > dy + dyRand > 0.8:
                    dy += dyRand
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

        pygame.draw.rect(screen, lightRed, paddleLeft)
        pygame.draw.rect(screen, lightBlue, paddleRight)
        pygame.draw.circle(screen, white, ball.center, ballRadius)

        gameTipText = smallFont.render("ESC - меню, P - пауза", True, white)
        screen.blit(gameTipText, (200, HEIGHT - 30))

        rightText = font.render("Игрок 2:", True, yellow)
        screen.blit(rightText, (WIDTH-200, 5))
        leftText = font.render("Игрок 1:", True, yellow)
        screen.blit(leftText, (50, 5))

        rightPoints = font.render(f"{pointRight}", True, lightBlue)
        screen.blit(rightPoints, (WIDTH-50, 5))
        leftPoints = font.render(f"{pointLeft}", True, lightRed)
        screen.blit(leftPoints, (200, 5))

        dxSpeed = smallFont.render(f"s_x : {dx:.2f}", True, white)
        screen.blit(dxSpeed, (25, HEIGHT - 40))
        dySpeed = smallFont.render(f"s_y : {dy:.2f}", True, white)
        screen.blit(dySpeed, (25, HEIGHT - 20))

        matchTimeCounter = smallFont.render(f"Время матча: {matchMinutes}.{matchSeconds}.{matchMiliseconds}", True, white)
        screen.blit(matchTimeCounter, (WIDTH-380, HEIGHT-40))
        gameTimeCounter = smallFont.render(f"Время игры : {gameMinutes}.{gameSeconds}.{gameMiliseconds}", True, white)
        screen.blit(gameTimeCounter, (WIDTH - 380, HEIGHT - 20))

        if pause:
            pauseFont = ARIAL_50.render("ПАУЗА", True, lightRed)
            pauseRect = pauseFont.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(pauseFont, pauseRect)

    pygame.display.flip()
    clock.tick(fps)
pygame.quit()

# Доработать чтобы когда мяч забивал он летел от того, кому забили (сделано)
# Реализовать паузу через esc (Сделано)
# Сделать меню (По большей части сделано)
# |
# L   Игроки выбирают макс счет, время всей игры и имена