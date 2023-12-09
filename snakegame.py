import pygame
import time
import random

def read_high_score():
    try:
        with open("highscore.txt", "r") as file:
            return int(file.read())
    except FileNotFoundError:
        return 0

def write_high_score(score):
    with open("highscore.txt", "w") as file:
        file.write(str(score))

pygame.init()

dis_width = 800
dis_height = 600
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake Game')

clock = pygame.time.Clock()

snake_block = 20

font_style = pygame.font.SysFont("bahnschrift", 25)

background_image = pygame.image.load("background.png")
background_image = pygame.transform.scale(background_image, (dis_width, dis_height))

eat_sound = pygame.mixer.Sound("eat.wav")
game_over_sound = pygame.mixer.Sound("gameover.wav")

def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.circle(dis, (0, 0, 0), (x[0] + snake_block // 2, x[1] + snake_block // 2), snake_block // 2)

def display_info(username, highest_score, current_score, snake_speed):
    score_text = font_style.render(f"Score: {current_score}", True, (0, 0, 0))
    highest_score_text = font_style.render(f"Highest Score: {highest_score}", True, (0, 0, 0))
    level_text = font_style.render(f"Speed: {snake_speed}", True, (0, 0, 0))
    
    if username and current_score > highest_score:
        congrats_text = pygame.font.SysFont("comicsansms", 25, bold=True).render(f"Congratulations {username}! You are the highest scorer!", True, (0, 255, 0))
        dis.blit(congrats_text, [dis_width / 6, dis_height / 2 + 30])

    dis.blit(score_text, [10, 10])
    dis.blit(highest_score_text, [dis_width - 200, 10])
    dis.blit(level_text, [dis_width - 200, 30])

    pygame.display.update()

def game_over_screen(username, highest_score, current_score):
    score_text = font_style.render(f"Score: {current_score}", True, (0, 0, 0))
    highest_score_text = font_style.render(f"Highest Score: {highest_score}", True, (0, 0, 0))

    if username and current_score > highest_score:
        congrats_text = pygame.font.SysFont("comicsansms", 25, bold=True).render(f"Congratulations {username}! You are the highest scorer!", True, (0, 255, 0))
        dis.blit(congrats_text, [dis_width / 6, dis_height / 2 + 30])

    dis.blit(score_text, [dis_width / 6, dis_height / 3])
    dis.blit(highest_score_text, [dis_width / 6, dis_height / 3 + 30])

    continue_text = pygame.font.SysFont("comicsansms", 20, bold=True).render("Press C to Continue or Q to Quit", True, (0, 0, 0))
    dis.blit(continue_text, [dis_width / 6, dis_height / 2 + 60])

    pygame.display.update()

def continue_screen():
    continue_text = pygame.font.SysFont("comicsansms", 20, bold=True).render("Press C to Continue or Q to Quit", True, (0, 0, 0))
    dis.blit(continue_text, [dis_width / 6, dis_height / 2 + 60])
    pygame.display.update()

def gameLoop():
    play_again = True

    while play_again:
        game_over = False

        x1 = dis_width / 2
        y1 = dis_height / 2

        x1_change = 0
        y1_change = 0

        snake_direction = 'RIGHT'
        last_direction = 'RIGHT'

        snake_List = []
        Length_of_snake = 1

        foodx = round(random.randrange(0, dis_width - snake_block) / 20.0) * 20.0
        foody = round(random.randrange(0, dis_height - snake_block) / 20.0) * 20.0

        highest_score = read_high_score()
        player_name = ""

        snake_speed = 10
        max_speed = 17
        speed_increase_interval = 10000
        last_speed_increase_time = pygame.time.get_ticks()

        input_str = ""
        cursor_blink = True
        cursor_blink_timer = pygame.time.get_ticks()

        while player_name == "":
            dis.fill((0, 0, 0))
            input_font = pygame.font.SysFont("comicsansms", 35)
            input_text = input_font.render("Enter your name: " + input_str, True, (255, 255, 102))

            current_time = pygame.time.get_ticks()
            if current_time - cursor_blink_timer > 500:
                cursor_blink_timer = current_time
                cursor_blink = not cursor_blink

            if cursor_blink:
                cursor_surface = input_font.render("|", True, (255, 255, 102))
                dis.blit(cursor_surface, [dis_width / 2 - 200 + input_text.get_width(), dis_height / 2 - 50])

            dis.blit(input_text, [dis_width / 2 - 200, dis_height / 2 - 50])
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        player_name = input_str
                    elif event.key == pygame.K_BACKSPACE:
                        input_str = input_str[:-1]
                    else:
                        input_str += event.unicode

        while not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                    play_again = False
                    break

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT and last_direction != 'RIGHT':
                        x1_change = -snake_block
                        y1_change = 0
                        snake_direction = 'LEFT'
                    elif event.key == pygame.K_RIGHT and last_direction != 'LEFT':
                        x1_change = snake_block
                        y1_change = 0
                        snake_direction = 'RIGHT'
                    elif event.key == pygame.K_UP and last_direction != 'DOWN':
                        y1_change = -snake_block
                        x1_change = 0
                        snake_direction = 'UP'
                    elif event.key == pygame.K_DOWN and last_direction != 'UP':
                        y1_change = snake_block
                        x1_change = 0
                        snake_direction = 'DOWN'

            if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
                game_over = True

            x1 += x1_change
            y1 += y1_change
            dis.blit(background_image, (0, 0))
            pygame.draw.rect(dis, (255, 0, 0), [foodx, foody, snake_block, snake_block])

            snake_Head = []
            snake_Head.append(x1)
            snake_Head.append(y1)
            snake_List.append(snake_Head)

            if len(snake_List) > Length_of_snake:
                del snake_List[0]

            for x in snake_List[:-1]:
                if x == snake_Head:
                    game_over = True

            our_snake(snake_block, snake_List)

            current_time = pygame.time.get_ticks()
            elapsed_time = current_time - last_speed_increase_time
            if elapsed_time > speed_increase_interval and snake_speed < max_speed:
                snake_speed += 1
                last_speed_increase_time = current_time

            display_info(player_name, highest_score, Length_of_snake - 1, snake_speed)

            pygame.display.update()

            if x1 == foodx and y1 == foody:
                eat_sound.play()
                foodx = round(random.randrange(0, dis_width - snake_block) / 20.0) * 20.0
                foody = round(random.randrange(0, dis_height - snake_block) / 20.0) * 20.0
                Length_of_snake += 1

            last_direction = snake_direction

            clock.tick(snake_speed)

        if Length_of_snake - 1 > highest_score:
            highest_score = Length_of_snake - 1
            write_high_score(highest_score)

        game_over_sound.play()
        game_over_screen(player_name, highest_score, Length_of_snake - 1)
        continue_screen()

        wait_for_input = True
        while wait_for_input:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    play_again = False
                    wait_for_input = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        wait_for_input = False
                    elif event.key == pygame.K_q:
                        play_again = False
                        wait_for_input = False

    pygame.quit()
    quit()

gameLoop()
