#
#  ngcf
#  Node-based general computing framework.
#  Copyright Patrick Huang 2021
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "y"

import pygame
import default_nodes
import events
from constants import *
from wm import WindowManager
pygame.init()


def gui():
    pygame.display.set_caption("Node-Based General Computing Framework")
    surface = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)

    clock = pygame.time.Clock()
    wm = WindowManager()

    click_start = [(0, 0)] * 3

    while True:
        clock.tick(FPS)
        pygame.display.update()

        pressed = pygame.mouse.get_pressed()
        events.mouse_down = [False] * 3
        events.mouse_up = [False] * 3
        events.mouse_pressed = [pressed[i] for i in (0, 1, 2)]
        events.mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                events.mouse_down[event.button-1] = True
            elif event.type == pygame.MOUSEBUTTONUP:
                events.mouse_up[event.button-1] = True

        for i in range(3):
            events.mouse_drag[i] = False
            if events.mouse_down[i]:
                click_start[i] = events.mouse_pos
            if events.mouse_pressed[i]:
                if (abs(events.mouse_pos[0]-click_start[i][0]) >= 3) or (abs(events.mouse_pos[1]-click_start[i][1]) >= 3):
                    events.mouse_drag[i] = True
                    events.mouse_drag_start[i] = click_start[i]
                    events.mouse_drag_end[i] = events.mouse_pos

        surface.fill((0, 0, 0))
        wm.draw(surface)


def main():
    default_nodes.register()
    gui()


main()
