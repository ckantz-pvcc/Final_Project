import pygame
import sys
import random

# Grid square variables
GRID_SIZE = 25
GRID_NUMBER = 20
SCREEN_SIZE = GRID_SIZE * GRID_NUMBER

# Colors (rbg)
GRID_RGB_1 = (139, 247, 72)
SNAKE_RGB_1 = (60, 186, 240)
SNAKE_RGB_2 = (47, 128, 163)
FRUIT_RGB = (255, 0, 0)
SCORE_AREA_RGB = (0, 0, 0)
GRID_RGB_2 = (76, 133, 41)

# Pygame import and screen setup
pygame.init()

# +50 reserves space for score outside of game grid
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE + 50))  
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)


class Snake:
    def __init__(self):

        #instantiate snake
        self.body = [pygame.math.Vector2(5, 10), pygame.math.Vector2(4, 10), pygame.math.Vector2(3, 10)]
        self.direction = pygame.math.Vector2(1, 0)
        self.new_block = False

    def draw(self):

        #puts the snake on the grid
        for block in self.body:
            x = int(block.x * GRID_SIZE)
            y = int(block.y * GRID_SIZE)
            block_rect = pygame.Rect(x, y, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(screen, SNAKE_RGB_1, block_rect)
            pygame.draw.rect(screen, SNAKE_RGB_2, block_rect, 2)


    def move(self):

        #makes the snake move by removing rearmost rect and adding frontmost rect
        if self.new_block:
            body_copy = self.body[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
        body_copy.insert(0, body_copy[0] + self.direction)
        self.body = body_copy


    def grow(self):

        # pauses the removal of rearmost block after eating
        self.new_block = True

    def reset(self):

        #restarts game when snake dies
        self.__init__()

    def check_collision(self):
        head = self.body[0]
        # collision with grid boundary
        if not 0 <= head.x < GRID_NUMBER or not 0 <= head.y < GRID_NUMBER:
            return True
        # collision with snake body
        if head in self.body[1:]:
            return True
        return False

class Fruit:

    def __init__(self, snake_body):

        #ensures fruit doesnt spawn in the snake's body position
        self.position = self.random_position(snake_body)

    def random_position(self, snake_body):

        #randomizes fruit spawn location
        while True:

            pos = pygame.math.Vector2(random.randint(0, GRID_NUMBER - 1),
                                      random.randint(0, GRID_NUMBER - 1))
            if pos not in snake_body:
                return pos

    def draw(self):

        #instantiates fruit on grid
        x = int(self.position.x * GRID_SIZE)
        y = int(self.position.y * GRID_SIZE)
        fruit_rect = pygame.Rect(x, y, GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(screen, FRUIT_RGB, fruit_rect)

# Main Method
class Game:

    #instantiates snake on board
    def __init__(self):
        self.snake = Snake()
        self.fruit = Fruit(self.snake.body)
        self.score = 0
        self.update_event = pygame.USEREVENT
        #snake movement speed (ms)
        pygame.time.set_timer(self.update_event, 125)

    #instantiates game area
    def draw_grid(self):
        
        for row in range(GRID_NUMBER):
            for col in range(GRID_NUMBER):
                rect = pygame.Rect(col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE)
                color = GRID_RGB_1 if (row + col) % 2 == 0 else GRID_RGB_2
                pygame.draw.rect(screen, color, rect)

    #broken
    #adds score area to display
    def draw_score(self):
        score_surface = font.render(f"Score: {self.score}", True, SCORE_AREA_RGB)
        screen.blit(score_surface, (10, SCREEN_SIZE + 10))

    #broken
    #displays score int
    def reset(self):
        self.snake.reset()
        self.fruit = Fruit(self.snake.body)
        self.score = 0

    #Checks for collision and score on each timer update
    def update(self):
        self.snake.move()
        if self.snake.check_collision():
            self.reset()

        if self.snake.body[0] == self.fruit.position:
            self.snake.grow()
            self.score += 1

            #respawns fruit
            self.fruit = Fruit(self.snake.body)

    def draw(self):
        self.draw_grid()
        self.snake.draw()
        self.fruit.draw()
        self.draw_score()

# pyame Game loop
game = Game()
running = True

while running:
    #allows exiting game window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        #game update/movement clock
        if event.type == game.update_event:
            game.update()

        #applies user input to snake movement
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game.snake.direction.y != 1:
                game.snake.direction = pygame.math.Vector2(0, -1)
            if event.key == pygame.K_DOWN and game.snake.direction.y != -1:
                game.snake.direction = pygame.math.Vector2(0, 1)
            if event.key == pygame.K_LEFT and game.snake.direction.x != 1:
                game.snake.direction = pygame.math.Vector2(-1, 0)
            if event.key == pygame.K_RIGHT and game.snake.direction.x != -1:
                game.snake.direction = pygame.math.Vector2(1, 0)

    #instantiates screen, game boundary, clock speed
    screen.fill(SCORE_AREA_RGB)
    game.draw()
    pygame.display.update()
    clock.tick(60)
