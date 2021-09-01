import pygame
import sys
import time
import random

global game_difficulty

# Colors (R, G, B)
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)

# Window size
frame_size_x = 720
frame_size_y = 480

# Checks for errors encountered
check_errors = pygame.init()

# second number in tuple gives number of errors
if check_errors[1] > 0:
    print(f'[!] Had {check_errors[1]} errors when initialising game, exiting...')
    sys.exit(-1)
else:
    print('[+] Game successfully initialised')


# Initialise game window
pygame.display.set_caption('Snake Game')
game_window = pygame.display.set_mode((frame_size_x, frame_size_y))
my_font = pygame.font.SysFont('times new roman', 35)

# FPS (frames per second) controller
fps_controller = pygame.time.Clock()

# Game variables
difficulty_options = ['Easy', 'Medium', 'Hard', 'Impossible']
snake_pos = [100, 50]
snake_body = [[100, 50], [100-10, 50], [100-(2*10), 50]]

food_pos = [random.randrange(1, (frame_size_x//10)) * 10, random.randrange(1, (frame_size_y//10)) * 10]
food_spawn = True

direction = 'RIGHT'
change_to = direction
score = 0

def write_options(difficulty_options, my_font):

    difficulty_options_title_surface = my_font.render('Select the game difficulty:', True, blue)
    difficulty_options_position = difficulty_options_title_surface.get_rect()
    difficulty_options_position.midtop = (frame_size_x / 2, (frame_size_y / 12))
    game_window.blit(difficulty_options_title_surface, difficulty_options_position)

    top_margin = 0
    for option in difficulty_options:
        difficulty_options_surface = my_font.render(option, True, white)
        difficulty_options_position = difficulty_options_surface.get_rect()
        difficulty_options_position.midtop = (frame_size_x / 2, (frame_size_y / 3) + top_margin)
        game_window.blit(difficulty_options_surface, difficulty_options_position)
        top_margin = top_margin + 60

def start_menu(difficulty_options, my_font):
    global game_difficulty
    selected_option_marker_position = [225, 170]
    write_options(difficulty_options, my_font)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Whenever a key is pressed down
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == ord('w'):
                    if(selected_option_marker_position[1] > 170):
                        selected_option_marker_position[1] = selected_option_marker_position[1] - 60
                        game_window.fill((0, 0, 0))
                        write_options(difficulty_options, my_font)
                if event.key == pygame.K_DOWN or event.key == ord('s'):
                    if (selected_option_marker_position[1] < 350):
                        selected_option_marker_position[1] = selected_option_marker_position[1] + 60
                        game_window.fill((0, 0, 0))
                        write_options(difficulty_options, my_font)
                # Esc -> Create event to quit the game
                if event.key == pygame.K_ESCAPE:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))
                if event.key == pygame.K_RETURN:
                    if selected_option_marker_position[1] == 170:
                        game_difficulty = 20
                    elif selected_option_marker_position[1] == 230:
                        game_difficulty = 35
                    elif selected_option_marker_position[1] == 290:
                        game_difficulty = 50
                    elif selected_option_marker_position[1] == 350:
                        game_difficulty = 80
                    return

            pygame.draw.rect(game_window, white, pygame.Rect(selected_option_marker_position[0], selected_option_marker_position[1], 10, 10))
            pygame.display.update()

# Game Over
def game_over(score):
    my_font = pygame.font.SysFont('times new roman', 80)
    game_over_surface = my_font.render('Game Over', True, red)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (frame_size_x/2, frame_size_y/4)
    game_window.fill(black)
    game_window.blit(game_over_surface, game_over_rect)
    show_score(0, red, 'times', 20, score)
    pygame.display.flip()
    time.sleep(3)
    pygame.quit()
    sys.exit()


# Score
def show_score(choice, color, font, size, score):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render('Score : ' + str(score), True, color)
    score_rect = score_surface.get_rect()
    if choice == 1:
        score_rect.midtop = (frame_size_x/10, 15)
    else:
        score_rect.midtop = (frame_size_x/2, frame_size_y/1.25)
    game_window.blit(score_surface, score_rect)
    pygame.display.flip()

def starGame(score, direction, change_to, food_pos, food_spawn):
    global game_difficulty
    while True:
        # Main logic
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Whenever a key is pressed down
            elif event.type == pygame.KEYDOWN:
                # W -> Up; S -> Down; A -> Left; D -> Right
                if event.key == pygame.K_UP or event.key == ord('w'):
                    change_to = 'UP'
                if event.key == pygame.K_DOWN or event.key == ord('s'):
                    change_to = 'DOWN'
                if event.key == pygame.K_LEFT or event.key == ord('a'):
                    change_to = 'LEFT'
                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    change_to = 'RIGHT'
                # Esc -> Create event to quit the game
                if event.key == pygame.K_ESCAPE:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))

        # Making sure the snake cannot move in the opposite direction instantaneously
        if change_to == 'UP' and direction != 'DOWN':
            direction = 'UP'
        if change_to == 'DOWN' and direction != 'UP':
            direction = 'DOWN'
        if change_to == 'LEFT' and direction != 'RIGHT':
            direction = 'LEFT'
        if change_to == 'RIGHT' and direction != 'LEFT':
            direction = 'RIGHT'

        # Moving the snake
        if direction == 'UP':
            snake_pos[1] -= 10
        if direction == 'DOWN':
            snake_pos[1] += 10
        if direction == 'LEFT':
            snake_pos[0] -= 10
        if direction == 'RIGHT':
            snake_pos[0] += 10

        # Snake body growing mechanism
        snake_body.insert(0, list(snake_pos))
        if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
            score += 1
            food_spawn = False
        else:
            snake_body.pop()

        # Spawning food on the screen
        if not food_spawn:
            food_pos = [random.randrange(1, (frame_size_x//10)) * 10, random.randrange(1, (frame_size_y//10)) * 10]
        food_spawn = True

        # GFX
        game_window.fill(black)
        for pos in snake_body:
            # Snake body
            pygame.draw.rect(game_window, green, pygame.Rect(pos[0], pos[1], 10, 10))

        # Snake food
        pygame.draw.rect(game_window, white, pygame.Rect(food_pos[0], food_pos[1], 10, 10))

        # Game Over conditions
        # Getting out of bounds
        if snake_pos[0] < 0 or snake_pos[0] > frame_size_x-10:
            game_over(score)
        if snake_pos[1] < 0 or snake_pos[1] > frame_size_y-10:
            game_over(score)
        # Touching the snake body
        for block in snake_body[1:]:
            if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
                game_over(score)

        show_score(1, white, 'consolas', 22, score)
        # Refresh game screen
        pygame.display.update()
        # Refresh rate
        fps_controller.tick(game_difficulty)

start_menu(difficulty_options, my_font)
starGame(score, direction, change_to, food_pos, food_spawn)