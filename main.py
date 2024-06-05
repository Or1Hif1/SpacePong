import math
import random

import pygame
from pygame.locals import *


pygame.init()
pygame.font.init()


SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Space Pong')
black_color = (0, 0, 0)
red_color = (255, 0, 0)
screen.fill(black_color)
running = False

clock = pygame.time.Clock()

font = pygame.font.SysFont('Poppins', 35)


PLAY_GAP = 46
BALL_GAP = 68

PLAYER_HEIGHT = 208
PLAYER_WITH_BLUR_HEIGHT = 328
player = pygame.Rect(133-PLAY_GAP, (SCREEN_HEIGHT-PLAYER_HEIGHT)/2-PLAY_GAP, PLAYER_WITH_BLUR_HEIGHT, 153)
player2 = pygame.Rect(1115-PLAY_GAP-27, (SCREEN_HEIGHT-PLAYER_HEIGHT)/2-PLAY_GAP, PLAYER_WITH_BLUR_HEIGHT, 153)


BALL_SIZE = 39


startButtonPos = pygame.Rect(319, 224, 509, 138)
startButtonPos2 = pygame.Rect(385, 286, 509, 138)

angel = random.randint(135, 225)
STATIC_VELOCITY = 500
velocity = pygame.Vector2(math.cos(math.radians(angel)) * STATIC_VELOCITY,
                          math.sin(math.radians(angel)) * STATIC_VELOCITY)

ballPos = pygame.Rect((SCREEN_WIDTH / 2) - (BALL_SIZE * 2), (SCREEN_HEIGHT / 2) - (BALL_SIZE * 2), BALL_SIZE, BALL_SIZE)

space_bg = pygame.image.load('Images/SpaceBG.png')
rectTexture = pygame.image.load('Images/RectBack.png')
ballTexture = pygame.image.load('Images/BallBack.png')
startButton = pygame.image.load('Images/StartButton.png')
RealSizeButton = pygame.image.load('Images/RealSizeButton.png')
RealSizeButtonLost = pygame.image.load('Images/BackBlur.png')
ButtonLost = pygame.image.load('Images/YouLostRealSize.png')

timer = 0
ticks = 1
runningLost = False


checkIsStart = True
while not running and checkIsStart:
    dt = clock.tick(60) / 1000
    screen.blit(space_bg, (0, 0))
    button = screen.blit(startButton, startButtonPos)
    second_button = screen.blit(RealSizeButton, startButtonPos2)

    for event in pygame.event.get():
        if event.type == QUIT:
            checkIsStart = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if second_button.collidepoint(pos):
                running = True
                checkIsStart = False

    pygame.display.flip()

while running:

    screen.blit(space_bg, (0, 0))
    screen.blit(font.render('Ticks: '+str(ticks-1), True, (255, 255, 255)), (10, 0))
    rect = screen.blit(rectTexture, player)  # right player
    rect2 = screen.blit(rectTexture, player2)
    ball = screen.blit(ballTexture, ballPos)
    dt = clock.tick(60) / 1000

    ballPos.move_ip(velocity.x * dt, velocity.y * dt)
    print("x: "+str(ball.x))
    print("y: "+str(ball.y))
    if not (0-BALL_GAP < ballPos.y < 720 - 175+BALL_GAP):
        print("angle: "+str(angel))
        angel = -angel
        velocity = pygame.Vector2(math.cos(math.radians(angel)) * STATIC_VELOCITY,
                                  math.sin(math.radians(angel)) * STATIC_VELOCITY)
    if (133-PLAY_GAP > ballPos.x-(39/2) and player.y-PLAY_GAP < ballPos.y < player.y + PLAYER_HEIGHT) or (ballPos.x > 1115 - PLAY_GAP-BALL_GAP and player2.y-PLAY_GAP < ballPos.y < player2.y + PLAYER_HEIGHT):
        ticks += 1
        angel = 180-angel
        velocity = pygame.Vector2(math.cos(math.radians(angel)) * STATIC_VELOCITY,
                                  math.sin(math.radians(angel)) * STATIC_VELOCITY)
    if 0 < ballPos.x+BALL_GAP/2+BALL_SIZE < 166 or player2.x < ballPos.x-(175/2)+BALL_SIZE+BALL_GAP:
        runningLost = True
        break

    key = pygame.key.get_pressed()

    # left player move
    if key[pygame.K_j] and player2.y > 0 - PLAY_GAP:
        player2.move_ip(0, -15)

    if key[pygame.K_k] and player2.y < SCREEN_HEIGHT-PLAYER_WITH_BLUR_HEIGHT+PLAY_GAP-2:
        player2.move_ip(0, 15)

    # right player move
    key = pygame.key.get_pressed()
    if key[pygame.K_f] and player.y > 0 - PLAY_GAP:
        player.move_ip(0, -15)

    if key[pygame.K_d] and player.y < SCREEN_HEIGHT - PLAYER_WITH_BLUR_HEIGHT + PLAY_GAP:
        player.move_ip(0, 15)

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    if ticks % 5 == 0:
        STATIC_VELOCITY += 1

    pygame.display.flip()

while runningLost:
    dt = clock.tick(60) / 1000
    screen.blit(space_bg, (0, 0))
    second_buttonT = screen.blit(RealSizeButtonLost, startButtonPos)
    buttonT = screen.blit(ButtonLost, startButtonPos2)

    for event in pygame.event.get():
        if event.type == QUIT:
            runningLost = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if second_buttonT.collidepoint(pos):
                runningLost = False
    pygame.display.flip()

pygame.quit()
