'''
module snake.py
Simple snake game made with python and love <3
'''
import time
import curses
import random


class Game:
    ''' Create game '''
    def __init__(self, height: int = 24, width: int = 50, fps: int = 30):
        pass

    def check_snake_collision(self, snake):
        ''' Collision 2-d phisics for snake '''
        pass

    def render_message(self, message: str) -> None:
        ''' Render any message to screen '''
        pass

    def update(self):
        ''' Update, not blit'''
        pass

    def render_game(self):
        ''' Draw the Game '''
        pass

    def run_loop(self):
        ''' Run game '''
        pass

class BaseSprite:
    ''' Base object with abstract phisics '''
    def __init__(self, x_pos: int, y_pos:int, speed: int = 0):
        pass


class Snake(BaseSprite):
    ''' Snake object with phisics '''
    def __init__(self, x_pos:int, y_pos:int):
        super().__init__(x_pos, y_pos, speed=15)
        pass

    def render(self, screen):
        ''' Draw snake '''
        pass

    def move(self) -> None:
        ''' Snake move with specified speed'''
        pass


class Fruit(BaseSprite):
    ''' Create fruit object '''
    def __init__(self, x_pos, y_pos):
        super().__init__(x_pos, y_pos, speed=15)
        pass

    def render(self, screen):
        ''' Draw fruit '''
        pass

    def rot_randomly(self):
        ''' All food can spoils '''
        pass


if __name__ == '__main__':
    game = Game()
    game.run_loop()
