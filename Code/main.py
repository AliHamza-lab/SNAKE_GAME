import pygame
import random

WIDTH = 600
HEIGHT = 400
SNAKE_BLOCK = 20
SNAKE_SPEED = 10

WHITE = (255, 255, 255)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)
SNAKE_COLOR = (0, 255, 0)
EYE_COLOR = (0, 0, 0)

class Snake:
    def __init__(self):
        self.x = WIDTH / 2
        self.y = HEIGHT / 2
        self.x_change = 0
        self.y_change = 0
        self.snake_list = []
        self.length_of_snake = 1

    def move(self):
        self.x += self.x_change
        self.y += self.y_change

    def check_boundaries(self):
        return self.x >= WIDTH or self.x < 0 or self.y >= HEIGHT or self.y < 0

    def check_self_collision(self):
        snake_head = [self.x, self.y]
        return snake_head in self.snake_list[:-1]

class Game:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Snake Game')
        self.clock = pygame.time.Clock()
        self.font_style = pygame.font.SysFont("bahnschrift", 25)
        self.score_font = pygame.font.SysFont("comicsansms", 35)

    def draw_snake(self, snake, snake_list):
        for x in snake_list[:-1]:
            pygame.draw.circle(self.window, SNAKE_COLOR, (int(x[0]), int(x[1])), SNAKE_BLOCK // 2)

        head = snake_list[-1]
        pygame.draw.circle(self.window, SNAKE_COLOR, (int(head[0]), int(head[1])), SNAKE_BLOCK // 2)
        
        eye_radius = SNAKE_BLOCK // 5
        eye_offset = SNAKE_BLOCK // 4
        
        if snake.x_change > 0:
            left_eye = (int(head[0] - eye_offset), int(head[1] - eye_radius))
            right_eye = (int(head[0] - eye_offset), int(head[1] + eye_radius))
        elif snake.x_change < 0:
            left_eye = (int(head[0] + eye_offset), int(head[1] - eye_radius))
            right_eye = (int(head[0] + eye_offset), int(head[1] + eye_radius))
        elif snake.y_change > 0:
            left_eye = (int(head[0] - eye_radius), int(head[1] - eye_offset))
            right_eye = (int(head[0] + eye_radius), int(head[1] - eye_offset))
        else:
            left_eye = (int(head[0] - eye_radius), int(head[1] + eye_offset))
            right_eye = (int(head[0] + eye_radius), int(head[1] + eye_offset))
        
        pygame.draw.circle(self.window, EYE_COLOR, left_eye, eye_radius)
        pygame.draw.circle(self.window, EYE_COLOR, right_eye, eye_radius)

    def draw_food(self, foodx, foody):
        pygame.draw.circle(self.window, GREEN, [foodx, foody], SNAKE_BLOCK // 2)

    def score_display(self, score):
        score_surface = self.score_font.render(f"Score: {score}", True, WHITE)
        self.window.blit(score_surface, [0, 0])

    def message(self, msg, color):
        message_surface = self.font_style.render(msg, True, color)
        self.window.blit(message_surface, [WIDTH / 6, HEIGHT / 3])

    def handle_events(self, snake):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and snake.x_change == 0:
                    snake.x_change = -SNAKE_BLOCK
                    snake.y_change = 0
                elif event.key == pygame.K_RIGHT and snake.x_change == 0:
                    snake.x_change = SNAKE_BLOCK
                    snake.y_change = 0
                elif event.key == pygame.K_UP and snake.y_change == 0:
                    snake.y_change = -SNAKE_BLOCK
                    snake.x_change = 0
                elif event.key == pygame.K_DOWN and snake.y_change == 0:
                    snake.y_change = SNAKE_BLOCK
                    snake.x_change = 0

    def game_loop(self):
        snake = Snake()
        foodx = round(random.randrange(0, WIDTH - SNAKE_BLOCK) / 10.0) * 10.0
        foody = round(random.randrange(0, HEIGHT - SNAKE_BLOCK) / 10.0) * 10.0

        while True:
            self.handle_events(snake)

            snake.move()

            if snake.check_boundaries() or snake.check_self_collision():
                self.window.fill(BLUE)
                self.message("You Lost! Press C-Play Again or Q-Quit", RED)
                self.score_display(snake.length_of_snake - 1)
                pygame.display.update()

                while True:
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_q:
                                pygame.quit()
                                quit()
                            elif event.key == pygame.K_c:
                                self.game_loop()

            self.window.fill(BLUE)

            self.draw_food(foodx, foody)

            snake_head = [snake.x, snake.y]
            snake.snake_list.append(snake_head)
            if len(snake.snake_list) > snake.length_of_snake:
                del snake.snake_list[0]

            self.draw_snake(snake, snake.snake_list)

            self.score_display(snake.length_of_snake - 1)
            pygame.display.update()

            if snake.x == foodx and snake.y == foody:
                foodx = round(random.randrange(0, WIDTH - SNAKE_BLOCK) / 10.0) * 10.0
                foody = round(random.randrange(0, HEIGHT - SNAKE_BLOCK) / 10.0) * 10.0
                snake.length_of_snake += 1

            self.clock.tick(SNAKE_SPEED)

if __name__ == "__main__":
    game = Game()
    game.game_loop()
