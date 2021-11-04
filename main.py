# Press the green button in the gutter to run the script.

import time
import pygame
from pygame.locals import *
import random

size = 40
BACKGROUND_COLOR = (80, 199, 199)

class Apple:
    def __init__(self, parent_screen):
        self.apple = pygame.image.load("Resources/apple.jpg").convert()
        self.parent_screen = parent_screen
        self.x = size * 3
        self.y = size * 3

    def draw(self):
        self.parent_screen.blit(self.apple, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(0, 24)*size # 1000/40
        self.y = random.randint(0, 17)*size # 720/40


class Snake:
    def __init__(self, surface, lenght):
        self.lenght = lenght
        self.parent_screen = surface
        self.block = pygame.image.load("Resources/block.jpg").convert()
        # Set the image on the background location
        self.x = [size] * lenght
        self.y = [size] * lenght
        self.lenght = lenght
        self.direction = 'down'

    def increase_length(self):
        self.lenght += 1
        self.x.append(-1)
        self.y.append(-1)

    def draw(self):
        for i in range(self.lenght):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))
        pygame.display.flip()

    def move_left(self):
        self.direction = 'left'
        self.draw()

    def move_right(self):
        self.direction = 'right'
        self.draw()

    def move_up(self):
        self.direction = 'up'
        self.draw()

    def move_down(self):
        self.direction = 'down'
        self.draw()

    def walk(self):
        for i in range(self.lenght - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        if self.direction == 'left':
            self.x[0] -= size
        if self.direction == 'right':
            self.x[0] += size
        if self.direction == 'up':
            self.y[0] -= size
        if self.direction == 'down':
            self.y[0] += size
        self.draw()


class Game:
    def __init__(self):
        # initializing pygame
        pygame.init()
        pygame.mixer.init()
        # creating surface
        self.play_background_music()
        self.surface = pygame.display.set_mode(size=(1000, 720))
        # Change the color of the background
        self.surface.fill((80, 199, 199))
        self.snake = Snake(self.surface, 1)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()

    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 +size:
            if y1 >= y2 and y1 < y2 + size:
                return True

    def render_background(self):
        bg = pygame.image.load("Resources/background.jpg")
        self.surface.blit(bg, (0,0))

    # Plays continouse music
    def play_background_music(self):
        pygame.mixer.music.load("Resources/bg_music_1.mp3")
        pygame.mixer.music.play()

    # Plays just a one time
    def play_sound(self, sound):
        sound = pygame.mixer.Sound(f"Resources/{sound}.mp3")
        pygame.mixer.Sound.play(sound)

    def play(self):
        self.render_background()
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

        # Snake Colliding with apple
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.play_sound("1_snake_game_resources_ding")
            self.snake.increase_length()
            self.apple.move()

        # Snake Colliding with itself
        for i in range(3, self.snake.lenght):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.play_sound("1_snake_game_resources_crash")
                raise "Game Over"

        # snake colliding with the boundries of the window
        if not (0 <= self.snake.x[0] <= 1000 and 0 <= self.snake.y[0] <= 720):
            self.play_sound('crash')
            raise "Hit the boundry error"

    def display_score(self):
        font = pygame.font.SysFont('arial', 30)
        score = font.render(f"Score: {self.snake.lenght*10}", True, (200, 200, 200))
        self.surface.blit(score, (720, 10))

    def reset(self):
        self.snake = Snake(self.surface, 1)
        self.apple = Apple(self.surface)

    def show_game_over(self):
        self.render_background()
        font = pygame.font.SysFont('arial', 30)
        ln1 = font.render(f"Hey Turtle.. Game is Over!, Try and play like me.. Your Score is : {self.snake.lenght * 10}.", True, (250, 250, 250))
        self.surface.blit(ln1, (200, 300))
        ln2 = font.render("To Play again press Enter. To exit press Escape!!!", True, (250, 250, 250))
        self.surface.blit(ln2, (200, 350))
        pygame.display.flip()
        pygame.mixer.music.pause()

    def Run(self):
        running = True
        pause = False

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                    if event.key == K_RETURN:
                        pause = False
                        pygame.mixer.music.unpause()

                    if event.key == K_ESCAPE:
                        exit(0)

                    if not pause:
                        if event.key == K_UP:
                            self.snake.move_up()

                        if event.key == K_DOWN:
                            self.snake.move_down()

                        if event.key == K_LEFT:
                            self.snake.move_left()

                        if event.key == K_RIGHT:
                            self.snake.move_right()

                elif event.type == QUIT:
                    running = False
            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()

            time.sleep(0.2)


if __name__ == '__main__':
    game = Game()
    game.Run()
