import random
from time import time, sleep
import socket
from _thread import *
import sys
import pickle
import json

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server = 'localhost'
port = 12345

server_ip = socket.gethostbyname(server)

try:
    s.bind((server, port))

except socket.error as e:
    print(str(e))

s.listen(2)
print("Waiting for a connection")

starttime = time()

client1, addr1 = s.accept()
#client2, addr2 = s.accept()


def send_data(request, field, highscore_1, highscore_2, snake_length_1, snake_length_2):
    if request == "field":
        client1.send(json.dumps(field).encode())
        return 0
    if request == "highscore_1":
        client1.send(str(highscore_1).encode())
        return 0
    if request == "highscore_2":
        client1.send(str(highscore_2).encode())
        return 0
    if request == "snake_length_1":
        client1.send(str(snake_length_1).encode())
        return 0
    if request == "snake_length_2":
        client1.send(str(snake_length_2).encode())
        return 0
    if request == "ready":
        return 1


def snake(field_width, field_height, tile_size, player_number, items_on, open_border, snake_start_length, speed):
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

    for i in range(0, 40):
        field.append(30*[0])

    pos_x_1 = random.randint(5, field_width-1-5)
    pos_y_1 = random.randint(5, field_height-1-5)
    field[pos_x_1][pos_y_1] = snake_length_1

    if player_number > 1:
        pos_x_2 = random.randint(5, field_width-1-5)
        pos_y_2 = random.randint(5, field_height-1-5)
        field[pos_x_2][pos_y_2] = 2000 + snake_length_2

    direction_1 = 0
    direction_2 = 4

    temp_direction_1 = 2
    temp_direction_2 = 4

    highscore_1 = 0
    highscore_2 = 0

    if items_on:
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
        for i in range(0, 10):
            pos_x = random.randint(0, field_width-1)
            pos_y = random.randint(0, field_height-1)
            while (field[pos_x][pos_y] != 0):
                pos_x = random.randint(0, field_width-1)
                pos_y = random.randint(0, field_height-1)
            field[pos_x][pos_y] = -3

    corona_1 = 0
    corona_2 = 0
    running = True
    starttime = time()
    while running:
        if direction_1 == 1:
            # Wenn ich am Bildrand bin ...
            if pos_y_1 == 0:
                # Wenn die Grenze offen ist ...
                if open_border:
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
        if direction_1 == 0:
            if pos_x_1 == field_width-1:
                if open_border:
                    pos_x_1 = 0
                else:
                    running = False
            else:
                pos_x_1 = pos_x_1 + 1

        # Code analog zu Spieler 1 und Richtung 1 mit Anpassung an Richtung 3
        if direction_1 == 3:
            if pos_y_1 == field_height-1:
                if open_border:
                    pos_y_1 = 0
                else:
                    running = False
            else:
                pos_y_1 = pos_y_1 + 1

        # Code analog zu Spieler 1 und Richtung 1 mit Anpassung an Richtung 4
        if direction_1 == 4:
            if pos_x_1 == 0:
                if open_border:
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
                    if open_border:
                        pos_y_2 = field_height-1
                    else:
                        running = False
                else:
                    pos_y_2 = pos_y_2 - 1

            # Code analog zu Spieler 1 und Richtung 1 mit Anpassung an Richtung 2
            # für Spieler 2
            if direction_2 == 0:
                if pos_x_2 == field_width-1:
                    if open_border:
                        pos_x_2 = 0
                    else:
                        running = False
                else:
                    pos_x_2 = pos_x_2 + 1

            # Code analog zu Spieler 1 und Richtung 1 mit Anpassung an Richtung 3
            # für Spieler 2
            if direction_2 == 3:
                if pos_y_2 == field_height-1:
                    if open_border:
                        pos_y_2 = 0
                    else:
                        running = False
                else:
                    pos_y_2 = pos_y_2 + 1

            # Code analog zu Spieler 1 und Richtung 1 mit Anpassung an Richtung 4
            # für Spieler 2
            if direction_2 == 4:
                if pos_x_2 == 0:
                    if open_border:
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
            if field[pos_x_1][pos_y_1] == -3:
                corona_1 += 30
                pos_x = random.randint(0, field_width-1)
                pos_y = random.randint(0, field_height-1)
                while (field[pos_x][pos_y] != 0):
                    pos_x = random.randint(0, field_width-1)
                    pos_y = random.randint(0, field_height-1)
                field[pos_x][pos_y] = -3

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

                if field[pos_x_2][pos_y_2] == -3:
                    corona_2 += 30
                    pos_x = random.randint(0, field_width-1)
                    pos_y = random.randint(0, field_height-1)
                    while (field[pos_x][pos_y] != 0):
                        pos_x = random.randint(0, field_width-1)
                        pos_y = random.randint(0, field_height-1)
                    field[pos_x][pos_y] = -3

                field[pos_x_2][pos_y_2] = 2000 + snake_length_2 + 1

        elif running != True:
            print("Died.")

        for x in range(0, field_width):
            for y in range(0, field_height):
                if field[x][y] in range(1, 1999) or field[x][y] in range(2001, 3999):
                    field[x][y] = field[x][y] - 1
        reply = 0
        while (reply != 1):
            data = client1.recv(1024).decode()
            reply = send_data(data, field, highscore_1,
                              highscore_2, snake_length_1, snake_length_2)
            print("got data")
        """print(json.dumps(field))
        client1.send(json.dumps(field).encode())
        client1.send(str(highscore_1).encode())
        client1.send(str(highscore_2).encode())
        client1.send(str(snake_length_1).encode())
        client1.send(str(snake_length_2).encode())"""


def main():
    args = [3, 5, 2]
    snake(40, 28, 20, int(args[2]),
          True, True, int(args[1]), int(args[0]))


if __name__ == "__main__":
    main()
