##################
## Kapitel 6.4  ##
##################

import pygame
import random
from time import sleep


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


class Button(pygame.sprite.Sprite):
    """Class used to create a button, use setCords to set 
        position of topleft corner. Method pressed() returns
        a boolean and should be called inside the input loop."""

    def __init__(self, image_path, text_str, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.image = load_image(image_path)
        self.rect = self.image.get_rect()

        font = pygame.font.Font("fonts/font.ttf", 20)
        text = font.render(str(text_str), True, (0, 0, 0))
        self.image.blit(text, (int(self.image.get_width() / 2 - text.get_width() / 2),
                               int(self.image.get_height() / 2 - text.get_height() / 2)))

        self.rect.topleft = int(
            x - self.image.get_width() / 2), int(y - self.image.get_height() / 2)

    def setCords(self, x, y):
        self.rect.topleft = int(
            x - self.image.get_width() / 2), int(y - self.image.get_height() / 2)

    def pressed(self, mouse):
        if mouse[0] > self.rect.topleft[0]:
            if mouse[1] > self.rect.topleft[1]:
                if mouse[0] < self.rect.bottomright[0]:
                    if mouse[1] < self.rect.bottomright[1]:
                        return True
                    else:
                        return False
                else:
                    return False
            else:
                return False
        else:
            return False


def title_screen(screen, screen_width, screen_height):
    buttons = pygame.sprite.Group()
    font_gr = pygame.font.Font("fonts/font.ttf", 20)
    font_sm = pygame.font.Font("fonts/font.ttf", 16)
    font_hu = pygame.font.Font("fonts/font.ttf", 50)

    clock = pygame.time.Clock()
    title_image = load_image("gfx/title_screen.png")

    classic_snake_button = Button(
        "gfx/button1.png", "Classic Snake Game", 400, 300)
    two_player_snake_button = Button(
        "gfx/button2.png", "Classic Snake with two players", 400, 350)
    tron_button = Button("gfx/button1.png", "Tron (two players)", 400, 400)
    quit_button = Button("gfx/button2.png", "Quit", 400, 450)
    buttons.add(classic_snake_button, two_player_snake_button,
                tron_button, quit_button)

    running = True
    while running:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "Quit"

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                # Button's pressed method is called
                if classic_snake_button.pressed(mouse):
                    return [3, 5, 1]

                if two_player_snake_button.pressed(mouse):
                    return [3, 5, 2]

                if tron_button.pressed(mouse):
                    return [2, 1000, 2]

                if quit_button.pressed(mouse):
                    return "Quit"

        screen.blit(title_image, (0, 0))

        buttons.draw(screen)
        pygame.display.flip()


def snake(screen, field_width, field_height, tile_size, player_number, items_on, open_border, snake_start_length, speed):

    font_gr = pygame.font.Font("fonts/font.ttf", 20)
    font_sm = pygame.font.Font("fonts/font.ttf", 16)
    font_hu = pygame.font.Font("fonts/font.ttf", 40)

    clock = pygame.time.Clock()

    field = []

    died_1 = 0
    died_2 = 0

    snake_length_1 = snake_start_length

    if player_number > 1:
        snake_length_2 = snake_start_length
    else:
        snake_length_2 = 0

    for i in range(0, field_width):
        field.append(field_height*[0])

    if player_number > 1:
        snake_body_1_image = load_image(
            'gfx/tron_'+str(tile_size)+'x'+str(tile_size)+'_1.png')
        snake_body_2_image = load_image(
            'gfx/tron_'+str(tile_size)+'x'+str(tile_size)+'_2.png')
    else:
        snake_body_1_image = load_image(
            'gfx/snake_'+str(tile_size)+'x'+str(tile_size)+'_1.png')

    for i in range(0, 40):
        field.append(30*[0])

    pos_x_1 = random.randint(5, field_width-1-5)
    pos_y_1 = random.randint(5, field_height-1-5)
    field[pos_x_1][pos_y_1] = snake_length_1

    if player_number > 1:
        pos_x_2 = random.randint(5, field_width-1-5)
        pos_y_2 = random.randint(5, field_height-1-5)
        field[pos_x_2][pos_y_2] = 2000 + snake_length_2

    direction_1 = 2
    direction_2 = 4

    highscore_1 = 0
    highscore_2 = 0

    if items_on:
        apple_image = load_image(
            'gfx/apple_'+str(tile_size)+'x'+str(tile_size)+'.png')
        coin_image = load_image(
            'gfx/coin_'+str(tile_size)+'x'+str(tile_size)+'.png')

        for i in range(0, 10):
            pos_x = random.randint(0, field_width-1)
            pos_y = random.randint(0, field_height-1)
            while (field[pos_x][pos_y] != 0):
                pos_x = random.randint(0, field_width-1)
                pos_y = random.randint(0, field_height-1)
            field[pos_x][pos_y] = -1
        for i in range(0, 20):
            pos_x = random.randint(0, field_width-1)
            pos_y = random.randint(0, field_height-1)
            while (field[pos_x][pos_y] != 0):
                pos_x = random.randint(0, field_width-1)
                pos_y = random.randint(0, field_height-1)
            field[pos_x][pos_y] = -2

    timer = 0
    running = True
    while running:
        clock.tick(30)
        timer = timer + 1
        if timer == speed:
            timer = 0

            if direction_1 == 1:
                # Wenn ich am Bildrand bin ...
                if pos_y_1 == 0:
                    # Wenn die Grenze offen ist ...
                    if open_border == True:
                        pos_y_1 = field_height-1
                        # Wenn die Grenze geschlossen ist ...
                    else:
                        running = False
                # Wenn ich nicht am Bildrand bin ...
                else:
                    pos_y_1 = pos_y_1 - 1
                    # Anpassung an die Speicherung der Schlangenlänge

                    # Die Schlange bewegt sich nicht mehr hier auf das neue Feld, sondern später.
            # Code analog zu Spieler 1 und Richtung 1 mit Anpassung an Richtung 2
            if direction_1 == 2:
                if pos_x_1 == field_width-1:
                    if open_border == True:
                        pos_x_1 = 0
                    else:
                        running = False
                else:
                    pos_x_1 = pos_x_1 + 1

            # Code analog zu Spieler 1 und Richtung 1 mit Anpassung an Richtung 3
            if direction_1 == 3:
                if pos_y_1 == field_height-1:
                    if open_border == True:
                        pos_y_1 = 0
                    else:
                        running = False
                else:
                    pos_y_1 = pos_y_1 + 1

            # Code analog zu Spieler 1 und Richtung 1 mit Anpassung an Richtung 4
            if direction_1 == 4:
                if pos_x_1 == 0:
                    if open_border == True:
                        pos_x_1 = field_width-1
                    else:
                        running = False
                else:
                    pos_x_1 = pos_x_1 - 1
            if field[pos_x_1][pos_y_1] in range(2, 1999) or field[pos_x_1][pos_y_1] in range(2002, 3999):
                running = False
            # Falls mehr als ein Spieler spielen möchte, wird die Bewegung von Schlange 2 berechnet und überwacht.

            if running == False:
                died_1 = 1

            if player_number > 1:
                # Code analog zu Spieler 1 und Richtung 1 mit Anpassung an Richtung 4
                # für Spieler 2
                if direction_2 == 1:
                    if pos_y_2 == 0:
                        if open_border == True:
                            pos_y_2 = field_height-1
                        else:
                            running = False
                    else:
                        pos_y_2 = pos_y_2 - 1

                # Code analog zu Spieler 1 und Richtung 1 mit Anpassung an Richtung 2
                # für Spieler 2
                if direction_2 == 2:
                    if pos_x_2 == field_width-1:
                        if open_border == True:
                            pos_x_2 = 0
                        else:
                            running = False
                    else:
                        pos_x_2 = pos_x_2 + 1

                # Code analog zu Spieler 1 und Richtung 1 mit Anpassung an Richtung 3
                # für Spieler 2
                if direction_2 == 3:
                    if pos_y_2 == field_height-1:
                        if open_border == True:
                            pos_y_2 = 0
                        else:
                            running = False
                    else:
                        pos_y_2 = pos_y_2 + 1

                # Code analog zu Spieler 1 und Richtung 1 mit Anpassung an Richtung 4
                # für Spieler 2
                if direction_2 == 4:
                    if pos_x_2 == 0:
                        if open_border == True:
                            pos_x_2 = field_width-1
                        else:
                            running = False
                    else:
                        pos_x_2 = pos_x_2 - 1
                if field[pos_x_2][pos_y_2] in range(2, 1999) or field[pos_x_2][pos_y_2] in range(2002, 3999):
                    running = False

                if running == False and died_1 == 0:
                    died_2 = 1
                # Die Variable running wäre False, wenn die Schlange sich selbst oder die andere gefressen
                # oder mit einer geschlossenen Wand kollidiert wäre. Wenn running True ist, bewegt sich die
                # Schlange nun auf das neue Schlangenkopffeld vor. Außerdem finden hier Anpassungen an die
                # nun variable Schlangenlänge statt.
            if running:
                if field[pos_x_1][pos_y_1] == -1:
                    highscore_1 += 500
                    snake_length_1 += 5
                    for x in range(0, field_width):
                        for y in range(0, field_height):
                            if field[x][y]in range(1, 1990):
                                field[x][y] += 5
                    pos_x = random.randint(0, field_width-1)
                    pos_y = random.randint(0, field_height-1)
                    while (field[pos_x][pos_y] != 0):
                        pos_x = random.randint(0, field_width-1)
                        pos_y = random.randint(0, field_height-1)
                    field[pos_x][pos_y] = -1
                if field[pos_x_1][pos_y_1] == -2:
                    highscore_1 += 1000
                    pos_x = random.randint(0, field_width-1)
                    pos_y = random.randint(0, field_height-1)
                    while (field[pos_x][pos_y] != 0):
                        pos_x = random.randint(0, field_width-1)
                        pos_y = random.randint(0, field_height-1)
                    field[pos_x][pos_y] = -2

                field[pos_x_1][pos_y_1] = snake_length_1 + 1

                # Wenn es mehr als einen Spieler gibt, bewegt sich natürlich auch Schlange zwei.
                if player_number > 1:
                    if field[pos_x_2][pos_y_2] == -1:
                        highscore_2 += 500
                        snake_length_2 += 5
                        for x in range(0, field_width):
                            for y in range(0, field_height):
                                if field[x][y]in range(2001, 3990):
                                    field[x][y] += 5
                        pos_x = random.randint(0, field_width-1)
                        pos_y = random.randint(0, field_height-1)
                        while (field[pos_x][pos_y] != 0):
                            pos_x = random.randint(0, field_width-1)
                            pos_y = random.randint(0, field_height-1)
                        field[pos_x][pos_y] = -1
                    if field[pos_x_2][pos_y_2] == -2:
                        highscore_2 += 1000
                        pos_x = random.randint(0, field_width-1)
                        pos_y = random.randint(0, field_height-1)
                        while (field[pos_x][pos_y] != 0):
                            i += 1
                            pos_x = random.randint(0, field_width-1)
                            pos_y = random.randint(0, field_height-1)
                        field[pos_x][pos_y] = - 2

                    field[pos_x_2][pos_y_2] = 2000 + snake_length_2 + 1

            elif running != True:
                print("Died.")

            for x in range(0, field_width):
                for y in range(0, field_height):
                    if field[x][y] in range(1, 1999) or field[x][y] in range(2001, 3999):
                        field[x][y] = field[x][y] - 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))

                if event.key == pygame.K_UP:
                    direction_1 = 1

                if event.key == pygame.K_DOWN:
                    direction_1 = 3

                if event.key == pygame.K_LEFT:
                    direction_1 = 4

                if event.key == pygame.K_RIGHT:
                    direction_1 = 2

                if event.key == pygame.K_w:
                    direction_2 = 1

                if event.key == pygame.K_s:
                    direction_2 = 3

                if event.key == pygame.K_a:
                    direction_2 = 4

                if event.key == pygame.K_d:
                    direction_2 = 2

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

        pygame.draw.rect(screen, (127, 127, 127), (0, tile_size *
                                                   field_height, tile_size * field_width, 2))
        text_str = 'Highscore: ' + str(highscore_1)
        text = font_gr.render(text_str, True, (255, 10, 10))
        screen.blit(text, (10, tile_size * field_height + 2))
        text_str = 'Länge: ' + str(snake_length_1)
        text = font_sm.render(text_str, True, (255, 10, 10))
        screen.blit(text, (int((tile_size * field_width) / 2) -
                           10 - text.get_width(), tile_size * field_height + 2))

        if player_number > 1:
            text_str = 'Highscore: ' + str(highscore_2)
            text = font_gr.render(text_str, True, (10, 10, 255))
            screen.blit(text, (tile_size * field_width - 10 -
                               text.get_width(), tile_size * field_height + 2))
            text_str = 'Länge: ' + str(snake_length_2)
            text = font_sm.render(text_str, True, (10, 10, 255))
            screen.blit(text, (int((tile_size * field_width) / 2) +
                               10, tile_size * field_height + 2))

        pygame.display.flip()

    if player_number > 1:
        if died_1 == 1:
            text_str = "Snake yellow died, Snake blue Wins!"

        if died_2 == 1:
            text_str = "Snake blue died, Snake yellow wins!"

    else:
        text_str = "You died!"

    running = True

    while running:

        if i == 1:
            screen.fill((0, 0, 0))
            text = font_hu.render(text_str, True, (255, 255, 255))
        if i == 2:
            screen.fill((255, 255, 255))
            text = font_hu.render(text_str, True, (0, 0, 0))

        screen.blit(text, (int((tile_size * field_width) / 2) - int(text.get_width() / 2),
                           (int((tile_size * field_height) / 2) - int(text.get_height() / 2))))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                running = False

        if i == 1:
            i += 1
        else:
            i = 1

        sleep(0.1)

    pygame.quit()


def main():
    screen_width = 800
    screen_height = 600

    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_icon(pygame.image.load("gfx/snake_20x20_1.png"))
    pygame.display.set_caption("Snäik bai Lili mit einem 'l' und Emil")
    pygame.mouse.set_visible(1)
    pygame.key.set_repeat(0, 30)

    args = title_screen(screen, screen_width, screen_height)

    pygame.mouse.set_visible(0)

    if not args == "Quit":
        snake(screen, 40, 28, 20, int(args[2]),
              True, True, int(args[1]), int(args[0]))


if __name__ == '__main__':
    main()
