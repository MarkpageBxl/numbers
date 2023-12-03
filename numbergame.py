#!/usr/bin/env python3

import argparse
import colorsys
import random
import sys

import pygame
from espeakng import ESpeakNG


def number_gen(m: int, n: int, shuffle: bool) -> int:
    nums = list(range(m, n + 1))
    if shuffle:
        random.shuffle(nums)
    for i in nums:
        yield i


def next_color():
    return [int(x * 255) for x in colorsys.hls_to_rgb(random.random(), 0.6, 1)]


def speak(n):
    speech.say(str(n), sync=True)


parser = argparse.ArgumentParser()
parser.add_argument("--min", "-m", type=int, default=0)
parser.add_argument("--max", "-n", type=int, default=9999)
parser.add_argument("--shuffle", "-s", action='store_true')
args = parser.parse_args()

pygame.init()
size = width, height = 720, 360
black = 0, 0, 0
white = 255, 255, 255
speech = ESpeakNG()
speech.voice = "fr-be"
speech.speed = 120
speech.pitch = 75

screen = pygame.display.set_mode(size)
pygame.display.toggle_fullscreen()
pygame.display.set_caption("Numbers game")
font = pygame.font.SysFont("liberationsans", 256, True, False)
gen = number_gen(args.min, args.max, args.shuffle)
n = next(gen)
color = next_color()

done = False
while not done:
    played = False
    for event in pygame.event.get():
        if played:
            continue
        if event.type == pygame.QUIT or (
            event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
        ):
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            speak(n)
            color = next_color()
            try:
                n = next(gen)
            except StopIteration:
                done = True
                break
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
