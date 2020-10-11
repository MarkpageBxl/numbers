#!/usr/bin/env python3

import colorsys
import pygame
import random
import sys

from espeakng import ESpeakNG

def next_number():
   return random.randint(0, 9999)

def next_color():
    return [int(x*255) for x in colorsys.hls_to_rgb(random.random(), 0.6, 1)]

def speak(n):
    speech.say(str(n), sync=True)

pygame.init()
size = width, height = 720, 360
black = 0, 0, 0
white = 255, 255, 255
speech = ESpeakNG()
speech.voice = 'fr-be'
speech.speed = 120
speech.pitch = 75

screen = pygame.display.set_mode(size)
pygame.display.toggle_fullscreen()
pygame.display.set_caption("Numbers game")
font = pygame.font.SysFont('liberationsans', 256, True, False)
n = next_number()
color = next_color()

while True:
    played = False
    for event in pygame.event.get():
        if played:
            continue
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            color = next_color()
            n = next_number()
            played = True
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            speak(n)
            played = True
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_f:
            pygame.display.toggle_fullscreen()
            played = True

    text = font.render(str(n), True, color, black)
    textRect = text.get_rect()
    textRect.center = (width // 2, height // 2)
    screen.fill(black)
    screen.blit(text, textRect)
    pygame.display.flip()
