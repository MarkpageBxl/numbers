#!/usr/bin/env python3

import argparse
import colorsys
import random
import sys
from collections.abc import Iterator
from threading import Semaphore

import pygame
import speechd

speech_semaphore = Semaphore(0)


def number_gen(m: int, n: int, step: int, shuffle: bool) -> Iterator[int]:
    nums = list(range(m, n + 1, step))
    if shuffle:
        random.shuffle(nums)
    for i in nums:
        yield i


def next_color():
    return [int(x * 255) for x in colorsys.hls_to_rgb(random.random(), 0.6, 1)]


def speak_callback(event_type: str, index_mark=None):
    speech_semaphore.release()


def speak(n):
    speech.speak(
        str(n), callback=speak_callback, event_types=(speechd.CallbackType.END,)
    )
    speech_semaphore.acquire()


parser = argparse.ArgumentParser()
parser.add_argument("--min", "-m", type=int, default=0)
parser.add_argument("--max", "-n", type=int, default=9999)
parser.add_argument("--step", "-s", type=int, default=1)
parser.add_argument("--shuffle", "-S", action="store_true")
parser.add_argument("--language", "-l", default="fr-be")
args = parser.parse_args()

pygame.init()
black = 0, 0, 0
white = 255, 255, 255
speech = speechd.SSIPClient("speak")
speech.set_language(args.language)
speech.set_rate(0)
speech.set_pitch(75)

size = width, height = 800, 450
screen = pygame.display.set_mode(size, pygame.FULLSCREEN | pygame.SCALED)
pygame.display.set_caption("Numbers game")
font = pygame.font.SysFont("liberationsans", 200, True, False)
gen = number_gen(args.min, args.max, args.step, args.shuffle)
n = next(gen)
color = next_color()

done = False
clock = pygame.time.Clock()
while not done:
    played = False
    for event in pygame.event.get():
        if played:
            continue
        if event.type == pygame.QUIT or (
            event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
        ):
            pygame.quit()
            speech.close()
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
            if pygame.display.is_fullscreen():
                pygame.display.set_mode(size)
            else:
                pygame.display.set_mode(size, pygame.FULLSCREEN | pygame.SCALED)
            played = True

    text = font.render(str(n), True, color, black)
    textRect = text.get_rect()
    textRect.center = (width // 2, height // 2)
    screen.fill(black)
    screen.blit(text, textRect)
    pygame.display.flip()
    clock.tick(10)
