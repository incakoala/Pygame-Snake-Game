"""
Hungry Python
vy
"""

import pygame
import sys  # to call sys.exit()
import random

# ---------------------------------------------------------------
#                         GLOBAL ASSETS
# ---------------------------------------------------------------
# Colors
pink = pygame.Color(217, 115, 130)
green = pygame.Color(176, 209, 148)
darkgreen = pygame.Color(143, 171, 120)
blue = pygame.Color(74, 155, 194)
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)

# Screen size
screen_x = 720
screen_y = 480

# Initialize game screen
screen = pygame.display.set_mode((screen_x, screen_y))


# ---------------------------------------------------------------
#                           GAME ACTIONS
# ---------------------------------------------------------------
def draw_background():
    """
    Draw game background
    :return: none (this function draws directly inside the main game loop)
    """
    screen.fill(green)
    square_size = screen_y // (screen_y // 10)
    x = 0
    y = 0
    # Draw vertical and horizontal lines across the screen to simulate tiles
    for row in range(screen_y):
        x += square_size
        y += square_size
        pygame.draw.line(screen, darkgreen, (x, 0), (x, screen_x))
        pygame.draw.line(screen, darkgreen, (0, y), (screen_x, y))


def draw_snake(snake_body):
    """
    Draw snake
    :param snake_body: list that holds dimensions of the body of the snake
    :return: none (this function draws directly inside the main game loop)
    """
    # Draw snake body using the coordinates in snake_body variable
    for pos in snake_body:
        # draw.rect(screen, color, rect)
        # rect: Rect(x-coord, y-coord, size_x, size_y)
        pygame.draw.rect(screen, blue, pygame.Rect(pos[0], pos[1], 10, 10))
#                                                      x      y     w    h


def draw_food(food_pos):
    """
    Draw food
    :param food_pos: list that holds random x and y coordinates of food
    :return: none (this function draws directly inside the main game loop)
    """
    pygame.draw.rect(screen, pink, pygame.Rect(food_pos[0], food_pos[1], 10, 10))


def randomize_food():
    """
    Randomize food position on the screen
    :return: list that holds random x and y coordinates of food
    """
    return [random.randrange(1, (screen_x // 10)) * 10,
            random.randrange(1, (screen_y // 10)) * 10]


def game_over(score):
    """
    Game Over screen
    """
    screen.fill(green)
    gameover_font = pygame.font.SysFont('icielbrushupotf', 95)

    # Create a game-over surface by rendering message
    game_over_surface = gameover_font.render('YOU DIED', True, pink)

    # Create a rectangle with the size of game-over surface and set coordinates of the rect
    # Note: this step is basically for us to set the coordinates of where we want to put our surface
    # to, since the rect can hold this information. Alternatively, you can skip this step and jump
    # to the screen.blit and make it screen.blit(game_over_surface, [insert x and y coords here])
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (screen_x / 2, screen_y / 4)

    # Draw game_over_surface onto center position -- blit(source, destination)
    screen.blit(game_over_surface, game_over_rect)

    # Do the same set of things but this time to print out 'Press r to play again'. There must be
    # a way to simplify though..
    playgain_font = pygame.font.SysFont('kohinoortelugutt', 30)
    playagain_surface = playgain_font.render('Press r to play again', True, white)
    playagain_rect = playagain_surface.get_rect()
    playagain_rect.midtop = (screen_x / 2, screen_y / 1.7)
    screen.blit(playagain_surface, playagain_rect)

    # Display score
    draw_score(0, pink, 'kohinoortelugutt', 30, score)

    # Update contents of the entire display
    pygame.display.flip()


def draw_score(choice, color, font, size, score):
    """
    Draw score
    :param choice: 1 for when game's in session / 0 for when you're dead
    :param color: font color
    :param font: font
    :param size: font size
    :param score: game score
    :return: one (this function draws directly inside the main game loop)
    """
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render('Score : ' + str(score), True, color)

    # Create rectangle of the score surface
    score_rect = score_surface.get_rect()

    # where score should be displayed while the game is in session
    if choice == 1:
        score_rect.midtop = (screen_x / 11, 10)
    # where score should be displayed in game over screen
    else:
        score_rect.midtop = (screen_x / 2, screen_y / 1.25)

    # Blit the score surface into our game screen
    screen.blit(score_surface, score_rect)

    # Remember to flip display
    pygame.display.flip()


# ---------------------------------------------------------------
#                           GAME LOGIC
# ---------------------------------------------------------------
def play_game():
    # Initialize the game
    pygame.init()

    # screen caption
    pygame.display.set_caption('Hungry Python')

    # set difficulty
    difficulty = 10

    # clock/frame-per-second controller -- this gets the game moving
    clock = pygame.time.Clock()

    # Game variables
    # initial position of the snake on the screen
    snake_pos = [100, 50]
    # dimensions of the snake body
    snake_body = [[100, 50], [100 - 10, 50], [100 - (2 * 10), 50]]  # 3 pairs of x & y coords
    # draw first food
    food_pos = randomize_food()

    # Variable to keep track of whether or not food has been spawned
    food_spawn = True

    # Initialize direction of snake to right
    direction = 'RIGHT'

    # Variable to keep track of direction from user
    change_to = direction

    # Initialize score
    score = 0

    # GAME LOOP
    while True:
        # Process events in the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # pygame.QUIT == closing the game screen
                pygame.quit()
                sys.exit()
            # Process the appropriate key when pressed
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    change_to = 'UP'
                if event.key == pygame.K_DOWN:
                    change_to = 'DOWN'
                if event.key == pygame.K_LEFT:
                    change_to = 'LEFT'
                if event.key == pygame.K_RIGHT:
                    change_to = 'RIGHT'
                if event.key == pygame.K_r:
                    play_game()
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

        # Prevent the snake from moving in the opposite direction instantly
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
        # Insert a new list to snake_body[0] to make it longer
        snake_body.insert(0, list(snake_pos))
        # If snake ate the food, increase the score
        if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
            score += 1
            food_spawn = False
        # If not pop the last part of the snake out (so that snake body doesn't accumulate from the
        # original position)
        else:
            snake_body.pop()

        # Spawning food on the screen
        if not food_spawn:
            food_pos = randomize_food()
        food_spawn = True

        # Draw game background, snake and food
        draw_background()
        draw_snake(snake_body)
        draw_food(food_pos)

        # Display score
        draw_score(1, white, 'kohinoortelugutt', 30, score)

        # Game Over conditions
        # Getting out of bounds
        if snake_pos[0] < 0 or snake_pos[0] > screen_x - 10 or snake_pos[1] < 0 or snake_pos[
            1] > screen_y - 10:
            game_over(score)
        # Touching the snake body
        for block in snake_body[1:]:
            if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
                game_over(score)
                return False

        # These last two lines must always be called at the END of the loop
        # Update game
        pygame.display.update()
        # Set clock rate: how fast the snake moves/num of iterations of the game are drawn per second
        clock.tick(difficulty)


# Run the game logic
play_game()
