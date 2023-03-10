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
        self.fps = int(1000 / fps)
        self.running = False
        self.curses_init(height, width)

    def curses_init(self, height, width):
        ''' Initialize curses '''
        self.height = height
        self.width = width
        self.screen = curses.initscr()
        self.screen.resize(height, width)
        self.screen.nodelay(True)
        self.game_help_window = curses.newwin(height // 4, width, height, 0)

        curses.noecho()             # No echo keys
        curses.cbreak()             # No pressing enter
        curses.curs_set(0)          # Hide cursor
        curses.start_color()        # Start color
        curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)

    def check_snake_collision(self, snake):
        ''' Collision 2-d phisics for snake '''
        if (snake.y_pos >= self.height - 1 or snake.y_pos <= 0) \
                or (snake.x_pos >= self.width - 1 or snake.x_pos <= 0):
            time.sleep(0.5)
            self.screen.erase()

            self.screen.addstr(
                    0, 2,
                    f"You chash by the WALL!\n  SCORE: {len(self.snake.tail)}",
                    curses.color_pair(1)
                    )

            self.screen.refresh()
            self.running = False
            time.sleep(3)

        elif [snake.y_pos, snake.x_pos] in snake.tail[:-1]:
            self.screen.erase()
            self.screen.addstr(
                    0, 2,
                    f"You eat your self!\n  SCORE: {len(self.snake.tail)}",
                    curses.color_pair(1)
                    )
            self.screen.refresh()
            self.running = False
            time.sleep(3)

    def render_message(self, message: str) -> None:
        ''' Render any message to screen '''
        self.screen.addstr(
                0,
                2,
                message,
                curses.color_pair(1)
                )

    def update(self):
        ''' Update, not blit'''
        match self.screen.getch():
            case 119: self.snake.direction = 'up'       # ord('w')
            case 97:  self.snake.direction = 'left'     # ord('a')
            case 115: self.snake.direction = 'down'     # ord('s')
            case 100: self.snake.direction = 'right'    # ord('d')
            case 113: self.running = False              # ord('q'):
            case 32: self.snake.direction = None        # ord(' ')
            case _: pass

        if self.snake.direction:
            self.snake.move()

        # Spawn new fruit if snake ate it
        if self.snake.y_pos == self.fruit.y_pos \
                and self.snake.x_pos == self.fruit.x_pos:
            self.snake.tail.append([self.snake.y_pos, self.snake.x_pos])
            self.snake.speed += 4.5
            self.fruit = Fruit(
                    random.randint(2, self.width - 2),
                    random.randint(2, self.height - 2)
                    )

        # Collision with body and border
        self.check_snake_collision(self.snake)

    def render_game(self):
        ''' Draw the Game '''
        self.screen.refresh()
        self.screen.erase()
        self.screen.border()

        self.screen.addstr(
                0,
                2,
                f"SCORE: {len(self.snake.tail)}",
                curses.color_pair(1)
                )

        self.snake.render(self.screen)
        self.fruit.render(self.screen)

        self.game_help_window.refresh()
        self.game_help_window.border()
        self.game_help_window.addstr(1, 2, '"w a s d" keys for move')
        self.game_help_window.addstr(1, 28, '-press any for start')
        self.game_help_window.addstr(3, 2, '"q" for quit')
        self.game_help_window.addstr(4, 2, '"space" for pause')

    def run_loop(self):
        ''' Run game '''
        self.running = True

        self.snake = Snake(self.width // 2, self.height // 2)
        self.fruit = Fruit(
                random.randint(2, self.width - 2),
                random.randint(2, self.height - 2)
                )
        while self.running:
            self.update()
            self.render_game()
            curses.napms(self.fps)
        self.screen.clear()
        curses.endwin()

class BaseSprite:
    ''' Base object with abstract phisics '''
    def __init__(self, x_pos: int, y_pos:int, speed: int = 0):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.speed = speed


class Snake(BaseSprite):
    ''' Snake object with phisics '''
    def __init__(self, x_pos:int, y_pos:int):
        super().__init__(x_pos, y_pos, speed=10)
        self.direction = None
        self.tail = [[self.y_pos, self.x_pos - 1, ]]
        self.clock = time.time()

    def render(self, screen):
        ''' Draw snake '''
        # Render head
        screen.addstr(self.y_pos, self.x_pos, '@', curses.color_pair(1))
        # Render body
        for body in self.tail:
            y_pos, x_pos = body[0],  body[1]
            screen.addstr(y_pos, x_pos, 'o', curses.color_pair(2))

    def move(self) -> None:
        ''' Snake move with specified speed'''
        if time.time() - self.clock > 1 / self.speed:
            # Move snake body
            self.tail.append([self.y_pos, self.x_pos])
            self.tail.pop(0)
            # Move snake head, step need to be one, because we use terminal
            match self.direction:
                case 'up':    self.y_pos -= 1
                case 'down':  self.y_pos += 1
                case 'left':  self.x_pos -= 1
                case 'right': self.x_pos += 1
            self.clock = time.time()


class Fruit(BaseSprite):
    ''' Create fruit object '''
    def __init__(self, x_pos, y_pos):
        super().__init__(x_pos, y_pos, speed=15)
        self.glyph = random.choice(['🍓', '🍎', '🍌'])
        self.rotten = False

    def render(self, screen):
        ''' Draw fruit '''
        screen.addstr(self.y_pos, self.x_pos, self.glyph)

    def rot_randomly(self):
        ''' All food can spoils '''
        pass


if __name__ == '__main__':
    game = Game()
    game.run_loop()
