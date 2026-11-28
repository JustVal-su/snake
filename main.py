"""Un jeu de snake fait par Valentin Jardon et Maxime Madignier 
pour un projet de NSI en 2026. Le jeu tourne dans un terminal."""
import random
import math
import time
import curses
import json
import platform

#arrows
# up 259
# down 258
# left 261
# right 260

#pad
#up 258
#down 259

# o 11
# esc 27
# z 122
#         q 113
#         s 115     
# d 100    
# c 99
def initialize_keys():
    """Initialize the keys used in the program considerint the user's operating system"""
    keys = {}
    # windows keys
    if platform.system() == "Windows":
        keys = {
        "up": 450,
        "down": 456,
        "left": 452,
        "right": 454
    } 
    # MacOS / Linux keys
    else:
        keys = {
            "up": 259,
            "down": 258,
            "left": 260,
            "right": 261
        }
    return keys


def place_snake_head(map_height):
    """Initial position of the snake head"""
    snake_head_y = int(map_height/2)
    snake_head_x = 3
    return (snake_head_x, snake_head_y)

def get_high_score():
    """Search for high score stored in high_score.txt"""
    with open("high_score.txt", "r") as text_file:
        content = text_file.read()
        if content == '':
            return 0
        return int(content)

def update_high_score(new_score):
    """Update high score when players hit a better one"""
    with open("high_score.txt", "w+") as text_file:
        text_file.write(str(new_score))
    

def read_json():
    """Read titles.json to get the ascii art titles"""
    with open("titles.json", "r") as file:
        data = json.load(file)
    return (data["threeD"], data["game"], data["over"])

def append_body(map, snake_body):
    """Append all the snake cells to the map"""
    for i in snake_body:
        map[i[1]][i[0]] = "1"

def body_update(snake_body, snake_head_x, snake_head_y, snake_length):
    """Update snake body display"""
    if len(snake_body) >= snake_length:
        snake_body.pop()
    snake_body.insert(0, [snake_head_x, snake_head_y])

def check_apple(snake_head_coordonates, apple_coordonates, is_apple_eaten, stdscr):
    """Check if snake is eating an apple"""
    return snake_head_coordonates == apple_coordonates

def change_direction(direction: str, snake_head_x, snake_head_y, stdscr, keys):
    key = stdscr.getch()
    """Changes snake direction if a key is pressed"""
    if key == keys["up"] and direction != "down":
        direction = "up"
        is_moving = True
        #snake_head_y -= 1
    elif key == keys["down"] and direction != "up":
        direction = "down"
        is_moving = True
        #snake_head_y += 1
    elif key == keys["right"] and direction != "left":
        direction = "right"
        is_moving = True
        #snake_head_x += 1
    elif key == keys["left"] and direction != "right":
        direction = "left" 
    return (direction, key)

def move_snake(snake_head_x, snake_head_y, direction, map, is_touching_edge, x, y):
    """Handle snake movements"""
    map_min_x = 0
    map_max_x = x - 1
    map_min_y = 0
    map_max_y = y - 1

    if direction == "up":
        if snake_head_y == map_min_y:
            snake_head_y = map_max_y + 1
        snake_head_y -= 1
    elif direction == "down":
        if snake_head_y == map_max_y:
            snake_head_y = map_min_y - 1
        snake_head_y += 1
    elif direction == "right":
        if snake_head_x == map_max_x:
            snake_head_x = map_min_x - 1
        snake_head_x += 1
    elif direction == "left":
        if snake_head_x == map_min_x:
            snake_head_x = map_max_x + 1
        snake_head_x -= 1
    return (snake_head_x, snake_head_y, is_touching_edge)

def check_alive(snake_body, snake_head_x, snake_head_y, snake_length):
    """Check if player is alive"""
    for i in snake_body[1:]:
        if [snake_head_x, snake_head_y] == i:
            return False
    return True

def game_scene(stdscr, snake_body, snake_length, x, y, text, high_score, timeout): 
    """Detects the user input"""

    is_moving = False
    is_apple_eaten = False
    direction = "right"
    player_alive = True
    stdscr.timeout(timeout)

    keys  = initialize_keys()

    map = map_creation(x, y)
    (snake_head_x, snake_head_y) = place_snake_head(y)

    for i in range(snake_length):
        snake_body.append([snake_head_x - i, snake_head_y])
    append_body(map, snake_body)

    (random_x, random_y) = place_fruit(x, y)
    map[random_y][random_x] = "🍎"
    score = snake_length - 3
    
    render(stdscr, map, score, text, high_score, is_moving)

    key = -1

    is_touching_edge = False
    while True:
        (direction, key) = change_direction(direction, snake_head_x, snake_head_y, stdscr, keys)
        if key != -1:
            is_moving = True

        if key == 113:
            return (score, "Quitting")
            
        if is_moving == True:
            (snake_head_x, snake_head_y, is_touching_edge) = move_snake(snake_head_x, snake_head_y, direction, map, is_touching_edge, x, y)
            body_update(snake_body, snake_head_x, snake_head_y, snake_length)
        is_apple_eaten = check_apple((random_x, random_y), (snake_head_x, snake_head_y), is_apple_eaten, stdscr)
        if is_apple_eaten:
            snake_length += 1
            (random_x, random_y) = place_fruit(x, y)
            score += 1
            is_apple_eaten = False

        player_alive = check_alive(snake_body, snake_head_x, snake_head_y, snake_length)
        map = map_creation(x, y)
        map[random_y][random_x] = "🍎"
        append_body(map, snake_body)
        score = snake_length - 3
        if player_alive:
            render(stdscr, map, score, text, high_score, is_moving)
        else:
            return (score, "Game Over")
        

def initialize_colors():
    """Creates the colors and color pairs used in the game"""
    curses.start_color()
    curses.init_color(1, 236, 28, 40)
    curses.init_color(2, 352, 112, 540)
    curses.init_color(3, 672, 340, 988)
    curses.init_color(4, 296, 888, 512)

    curses.init_color(5, 588, 204, 936)
    curses.init_color(6, 1000, 1000, 1000)


    curses.init_pair(10, 1, 2)
    curses.init_pair(11, 2, 1)
    curses.init_pair(12, 2, 3)
    curses.init_pair(13, 4, 4)
    curses.init_pair(14, 6, 5)


def print_pixel(x, y, stdscr, string):
    if string == "0":
        stdscr.addstr(y, x, "▄", curses.color_pair(10))
        stdscr.addstr(y, x+1, "▄", curses.color_pair(11))
    elif string == "1":
        stdscr.addstr(y, x, "▄", curses.color_pair(13))
        stdscr.addstr(y, x+1, "▄", curses.color_pair(13))
    else:
        stdscr.addstr(y, x, string, curses.color_pair(10))

def map_creation (width, height=None):
    """Crée un tableau de longueur de côté MAP_SIZE""" 
    if height == None:
        height = width
    map_line = []
    map = []
    for i in range(width):
        map_line.append("0")
    for i in range(height):
        map.append(map_line.copy())
    return map

def return_center(stdscr, map_len, amount):
    """Return the abciss an element should have to be centered"""
    (height,width) = stdscr.getmaxyx()
    window_center = int(width / 2)
    map_center = math.ceil(map_len / 2) * amount
    return window_center - map_center

def print_text(stdscr, text, y=0):
    """Handle title display"""
    
    max_width = 0 
    for i in range(len(text)):
        if len(text[i]) > max_width:
            max_width = len(text[i])
    base_x = return_center(stdscr, max_width, 1)
    x = base_x
    for i in range(len(text)):
        for j in range(len(text[i])):
            stdscr.addstr(y, x, text[i][j])
            x += 1
        y += 1
        x = base_x


def render(stdscr, map, score, text, high_score, is_moving):
    """The function rendering the map on the screen"""
    
    print_text(stdscr, text)
    base_x = return_center(stdscr, len(map[0]), 2)
    score_x = return_center(stdscr, len(text[0]), 1)
    stdscr.addstr(len(text), score_x + 5, f"Score : {str(score).zfill(6)}")
    stdscr.addstr(len(text), score_x + 5 + 39, f"HI : {str(high_score).zfill(6)}")
    x = base_x
    y = len(text) + 2
    for i in range(len(map)):
        for j in range(len(map[i])):
            #print(map[i][j], end="")
            print_pixel(x, y, stdscr, map[i][j])
            x += 2
        x = base_x
        y += 1
    if is_moving != True:
        infos = "Press any key to start"
        infos_x = return_center(stdscr, len(infos), 1)
        stdscr.addstr(y + 1, infos_x, infos)
        infos = "Move with arrows · Press q to quit"
        infos_x = return_center(stdscr, len(infos), 1)
        stdscr.addstr(y + 2, infos_x, infos)
    else:
        infos = "                      "
        infos_x = return_center(stdscr, len(infos), 1)
        stdscr.addstr(y + 1, infos_x, infos)
        infos = "                                  "
        infos_x = return_center(stdscr, len(infos), 1)
        stdscr.addstr(y + 2, infos_x, infos)

def place_fruit(max_x, max_y=None):
    """Place a fruit on a random case"""
    if max_y == None:
        max_y = max_x

    random_x = random.randint(0, max_x - 1)
    random_y = random.randint(0, max_y - 1)
    return (random_x, random_y)

def menu_scene(stdscr, text, high_score):
    keys  = initialize_keys()
    selected = "New game"
    print_text(stdscr, text)

    high_score_string = f"High score : {str(high_score).zfill(6)}"
    high_score_x = return_center(stdscr, len(high_score_string), 1)
    stdscr.addstr(len(text), high_score_x, high_score_string)
    base_x = return_center(stdscr, len(">New game"), 1)
    stdscr.addstr(len(text) + 3, base_x, ">New game", curses.color_pair(14) | curses.A_BOLD)
    stdscr.addstr(len(text) + 4, base_x, " Options")

    infos = "Navigate with up and down arrows, select with enter."
    infos_x = return_center(stdscr, len(infos), 1)
    stdscr.addstr(len(text) + 7, infos_x, infos)
    while True:
        key = stdscr.getch()
        if key == keys["down"]:
            stdscr.addstr(len(text) + 3, base_x, " New game")
            stdscr.addstr(len(text) + 4, base_x, ">Options", curses.color_pair(14) | curses.A_BOLD)
            selected = "Options"
        elif key == keys["up"]:
            stdscr.addstr(len(text) + 3, base_x, ">New game", curses.color_pair(14) | curses.A_BOLD)
            stdscr.addstr(len(text) + 4, base_x, " Options")
            selected = "New game"
        elif key == 10:
            return selected

def game_over_scene(game, over, new_score, high_score, stdscr):
    keys  = initialize_keys()
    text_height = len(game) + 1 + len(over)
    selected = "New game"
    print_text(stdscr, game)
    print_text(stdscr, over, len(game))
    #stdscr.addstr("HI : 00000")
    base_x = return_center(stdscr, len(">Main menu"), 1)
    stdscr.addstr(text_height, base_x, ">Retry", curses.color_pair(14) | curses.A_BOLD)
    stdscr.addstr(text_height + 1, base_x, " Main menu")
    while True:
        key = stdscr.getch()
        if key == keys["down"]:
            stdscr.addstr(text_height, base_x, " Retry")
            stdscr.addstr(text_height + 1, base_x, ">Main menu", curses.color_pair(14) | curses.A_BOLD)
            selected = "Menu"
        elif key == keys["up"]:
            stdscr.addstr(text_height, base_x, ">Retry", curses.color_pair(14) | curses.A_BOLD)
            stdscr.addstr(text_height + 1, base_x, " Main menu")
            selected = "New game"
        elif key == 10:
            return selected

def options_scene(stdscr, map_len, timeout):
    stdscr.addstr("<press enter to save and quit")
    keys = initialize_keys()
    base_x = return_center(stdscr, len("Snake speed : 30 (Number between 10 and 30)"), 1)
    stdscr.addstr(3, base_x, f"Map width : {map_len} (Number between 10 and 30)", curses.color_pair(14) | curses.A_BOLD)
    stdscr.addstr(4, base_x, f"Snake speed : {int(6 - timeout/100)} (Number between 1 and 5)")

    error_speed_x = return_center(stdscr, len("Please only enter a number between 1 and 5 as speed."), 1)
    watching = True
    while watching:
        key = stdscr.getch()
        stdscr.addstr(14, 0, str(key))
        if key == 113:
            watching = False
        elif key == keys["down"]:
            stdscr.addstr(3, base_x, f"Map width : {map_len} (Number between 10 and 30)")
            stdscr.addstr(4, base_x, f"Snake speed : {int(6 - timeout/100)} (Number between 1 and 5)", curses.color_pair(14) | curses.A_BOLD)
            second_key = stdscr.getkey()
            if second_key.isdigit() and 1 <= int(second_key) <= 5:
                timeout = (6 - int(second_key)) * 100
                stdscr.addstr(4, base_x, f"Snake speed : {int(6 - timeout/100)} (Number between 1 and 5)", curses.color_pair(14) | curses.A_BOLD)
            else:
                stdscr.addstr(6, error_speed_x, "Please only enter a number between 1 and 5 as speed.")
        elif key == keys["up"]:
            stdscr.addstr(3, base_x, f"Map width : {map_len} (Number between 10 and 30)", curses.color_pair(14) | curses.A_BOLD)
            stdscr.addstr(4, base_x, f"Snake speed : {int(6 - timeout/100)} (Number between 1 and 5)")
            second_key = stdscr.getkey()
            third_key = stdscr.getkey()
            if second_key.isdigit() and 10 <= int(second_key + third_key) <= 30:
                map_len = int(second_key + third_key)
                stdscr.addstr(3, base_x, f"Map width : {map_len} (Number between 10 and 30)", curses.color_pair(14) | curses.A_BOLD)
            else:
                stdscr.addstr(6, error_speed_x, " " * len("Please only enter a number between 1 and 5 as speed."))
                stdscr.addstr(6, error_speed_x + 1, "Please only enter a number between 10 and 30 as width.")
    stdscr.clear()
    return "Menu"
        
def quitting_scene(stdscr):
    stdscr.clear()
    stdscr.timeout(300)
    stdscr.addstr("Quitting")
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.reset_prog_mode()


def main(stdscr): 
    """Entry point"""
    x = 15
    y = 15
    initialize_colors()
    (text, game, over) = read_json()
    next_scene = None
    high_score = get_high_score()
    new_score = 0
    timeout = 300
    

    #detect_keys(stdscr, snake_body, snake_length, x, y, text)
    
    #with open("high_score.txt", "w+") as text_file:
    #    text_file.write(str("000000"))
    next_scene = menu_scene(stdscr, text, high_score)
    while True:
        stdscr.clear()
        if next_scene == "New game":
            snake_body = []
            snake_length = 3
            (new_score, next_scene) = game_scene(stdscr, snake_body, snake_length, x, y, text, high_score, timeout)
        elif next_scene == "Game Over":
            next_scene = game_over_scene(game, over, new_score, high_score, stdscr)
        elif next_scene == "Menu":
            next_scene = menu_scene(stdscr, text, high_score)
        elif next_scene == "Options":
            next_scene == options_scene(stdscr, 15, timeout)
        elif next_scene == "Quitting":
            quitting_scene(stdscr)


        if high_score < new_score:
            update_high_score(new_score)
    
    stdscr.clear()
    
curses.wrapper(main)
