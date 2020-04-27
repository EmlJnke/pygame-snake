import random
import pygame
import socket
import pickle
import json
from time import sleep, time

# Create a socket object
s = socket.socket()

# Define the port on which you want to connect
port = 12345

# connect to the server on local computer
s.connect(('127.0.0.1', port))


def recieve(buff, is_list):
    if is_list == 1:
        data = s.recv(buff).decode()
        print(type(data))
        return json.dumps(data)
    else:
        data = s.recv(buff).decode()
        return int(data)


def load_image(filename, colorkey=None):
    image = pygame.image.load(filename)
    if image.get_alpha() is None:
        image = image.convert()
    else:
        image = image.convert_alpha()

    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, pygame.RLEACCEL)

    return image


def snake(screen, field_width, field_height, tile_size, player_number, items_on, open_border, snake_start_length, speed):
    font_gr = pygame.font.Font("fonts/font.ttf", 20)
    font_sm = pygame.font.Font("fonts/font.ttf", 16)
    font_hu = pygame.font.Font("fonts/font.ttf", 40)

    if player_number > 1:
        snake_body_1_image = load_image(
            'gfx/tron_'+str(tile_size)+'x'+str(tile_size)+'_1.png')
        snake_body_2_image = load_image(
            'gfx/tron_'+str(tile_size)+'x'+str(tile_size)+'_2.png')
    else:
        snake_body_1_image = load_image(
            'gfx/snake_'+str(tile_size)+'x'+str(tile_size)+'_1.png')

    if items_on:
        apple_image = load_image(
            'gfx/apple_'+str(tile_size)+'x'+str(tile_size)+'.png')
        coin_image = load_image(
            'gfx/coin_'+str(tile_size)+'x'+str(tile_size)+'.png')
        virus_image = load_image(
            'gfx/virus_'+str(tile_size)+'x'+str(tile_size)+'.png')

    running = True
    starttime = time()
    while running:
        sleep((1/30) - ((time() - starttime) % (1/30)))
        if (time() >= starttime + 1):
            starttime = time()
        s.send("field".encode())
        field = recieve(10240, 1)
        s.send("highscore_1".encode())
        highscore_1 = recieve(1024, 0)
        s.send("highscore_2".encode())
        highscore_2 = recieve(1024, 0)
        s.send("snake_length_1".encode())
        snake_length_1 = recieve(1024, 0)
        s.send("snake_length_2".encode())
        snake_length_2 = recieve(1024, 0)
        s.send("ready".encode())

        screen.fill((153, 204, 255))

        for x in range(0, field_width):
            for y in range(0, field_height):
                if field[x][y] in range(1, 1999):
                    screen.blit(snake_body_1_image, (tile_size*x, tile_size*y))

                if field[x][y] in range(2001, 3999):
                    screen.blit(snake_body_2_image, (tile_size*x, tile_size*y))

                if field[x][y] == -1:
                    screen.blit(apple_image, (tile_size*x, tile_size*y))
                if field[x][y] == -2:
                    screen.blit(coin_image, (tile_size * x, tile_size * y))
                if field[x][y] == -3:
                    screen.blit(virus_image, (tile_size * x, tile_size * y))

        pygame.draw.rect(screen, (127, 127, 127), (0, tile_size *
                                                   field_height, tile_size * field_width, 2))
        text_str = 'Score: ' + str(highscore_1)
        text = font_gr.render(text_str, True, (255, 10, 10))
        screen.blit(text, (10, tile_size * field_height + 2))
        text_str = 'Länge: ' + str(snake_length_1)
        text = font_sm.render(text_str, True, (255, 10, 10))
        screen.blit(text, (int((tile_size * field_width) / 2) -
                           10 - text.get_width(), tile_size * field_height + 2))

        if player_number > 1:
            text_str = 'Score: ' + str(highscore_2)
            text = font_gr.render(text_str, True, (10, 10, 255))
            screen.blit(text, (tile_size * field_width - 10 -
                               text.get_width(), tile_size * field_height + 2))
            text_str = 'Länge: ' + str(snake_length_2)
            text = font_sm.render(text_str, True, (10, 10, 255))
            screen.blit(text, (int((tile_size * field_width) / 2) +
                               10, tile_size * field_height + 2))

        pygame.display.flip()


def main():
    screen_width = 800
    screen_height = 600

    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_icon(pygame.image.load("gfx/python_logo_20x20.png"))
    pygame.display.set_caption("Snäik bai Lili mit einem 'l' und Emil")
    pygame.mouse.set_visible(0)
    pygame.key.set_repeat(0, 30)
    args = [3, 5, 2]
    snake(screen, 40, 28, 20, int(args[2]),
          True, True, int(args[1]), int(args[0]))


if __name__ == "__main__":
    main()
