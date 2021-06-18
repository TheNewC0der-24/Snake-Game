import pygame
import random
import os

pygame.mixer.init()
pygame.init()

# COLOURS
white = (255, 255, 255 )
red = (255, 0, 0)
black = (0, 0, 0)
aqua = (26, 198, 217)
yellow = (252, 186, 3)

# CREATING WINDOW
screen_width = 900
screen_height = 600
gameWindow = pygame.display.set_mode((screen_width,screen_height))

# BACKGROUND IMAGE
bgimg = pygame.image.load("Snakes.png")
bgimg1 = pygame.image.load("gameover.png")
bgimg = pygame.transform.scale(bgimg, (screen_width, screen_height)).convert_alpha()
bgimg1 = pygame.transform.scale(bgimg1, (screen_width, screen_height)).convert_alpha()


# GAME TITLE
pygame.display.set_caption("Snake Game")
pygame.display.update()

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 55)

with open("HiScore.txt", "r") as f:
    hiscore = f.read()

# SET SCORE ON SCREEN
def score_screen(text ,color, x, y):
    screen_score = font.render(text, True, color)
    gameWindow.blit(screen_score, [x,y])

def plot_snake(gameWindow, color, snake_list, snake_size):
    for x,y in snake_list:
        pygame.draw.rect(gameWindow, color, [x, y, snake_size, snake_size])

# WELCOME SCREEN
def welcome():
    exit_game = False
    while not exit_game:
        gameWindow.fill((233,220,229))
        score_screen("Welcome to Snakes", black, 260, 250)
        score_screen("Press Spacebar to Play", black, 230, 300)
        gameWindow.blit(bgimg, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.mixer.music.load("back.mp3")
                    pygame.mixer.music.play()
                    gameloop()

        pygame.display.update()
        clock.tick(60)
# GAME LOOP
def gameloop():

    # GAME SPECIFIC VARIABLE
    exit_game = False
    game_over = False
    snake_x = 45
    snake_y = 55
    velocity_x = 0
    velocity_y = 0
    snake_list = []
    snake_length = 1

    # CHECK IF HISCORE FILE EXISTS
    if (not os.path.exists("HiScore.txt")):
        with open("HiScore", "w") as f:
            f.write("0")

    #  READ HIGHSCORE
    with open("HiScore.txt", "r") as f:
        hiscore = f.read()

    food_x = random.randint(20, screen_width / 2)
    food_y = random.randint(20, screen_height / 2)
    score = 0
    init_velocity = 5
    snake_size = 20
    fps = 60

    while not exit_game:
        if game_over:
            with open("HiScore.txt", "w") as f:
                f.write(str(hiscore))
            gameWindow.fill(white)
            score_screen("Game over! Press Enter To Continue", aqua, 110, 250)
            gameWindow.blit(bgimg1, (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        welcome()

        else:
            # HANDLING EVENTS
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                # HANDLING KEY
                if event.type == pygame.KEYDOWN:
                    # HANDLING RIGHT KEY
                    if event.key == pygame.K_RIGHT:
                        velocity_x = init_velocity
                        velocity_y = 0

                    # HANDLING LEFT KEY
                    if event.key == pygame.K_LEFT:
                        velocity_x = - init_velocity
                        velocity_y = 0

                    # HANDLING UP KEY
                    if event.key == pygame.K_UP:
                        velocity_y = - init_velocity
                        velocity_x = 0

                    # HANDLING DOWN KEY
                    if event.key == pygame.K_DOWN:
                        velocity_y = + init_velocity
                        velocity_x = 0

                    if event.key == pygame.K_q:
                        score += 5

            snake_x = snake_x + velocity_x
            snake_y = snake_y + velocity_y

            if abs(snake_x - food_x) < 10 and abs(snake_y - food_y) < 10:
                score += 10

                # RANDOMLY PLACING FOOD
                food_x = random.randint(20, screen_width / 2)
                food_y = random.randint(20, screen_height / 2)

                #INCREASING LENGTH
                snake_length += 5
                if score > int(hiscore):
                    hiscore = score

            # COLORING GAME WINDOW
            gameWindow.fill(black)

            # SHOW SCORE ON SCREEN
            score_screen("Score: " + str(score ) , aqua, 5, 5)
            score_screen("HiScore" + str(hiscore), yellow, 5, 40)
            # CREATING FOOD OF SNAKE
            pygame.draw.rect(gameWindow, red, [food_x, food_y, snake_size, snake_size])
            # CREATING HEAD OF SNAKE
            pygame.draw.rect(gameWindow, white, [snake_x, snake_y, snake_size, snake_size])

            # INCREASING LENGTH
            head = []
            head.append(snake_x)
            head.append(snake_y)
            snake_list.append(head)

            if len(snake_list)>snake_length:
                del snake_list[0]

            if head in snake_list[:-1]:
                game_over = True
                pygame.mixer.music.load("gameover.mp3")
                pygame.mixer.music.play()

            if snake_x < 0 or snake_x > screen_width or snake_y < 0 or snake_y > screen_height:
                game_over = True
                pygame.mixer.music.load("gameover.mp3")
                pygame.mixer.music.play()


            plot_snake(gameWindow, white, snake_list, snake_size)

        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()
welcome()
