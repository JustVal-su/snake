"""A snake game, directly in the terminal"""
import random
import math
import curses
import json

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

def place_snake_head(map_height):
    """Initial position of the snake head"""
    snake_head_y = int(map_height/2)
    snake_head_x = 3
    return (snake_head_x, snake_head_y)

def read_json(stdscr):
    with open("titles.json", "r") as file:
        data = json.load(file)
    return data["threeD"]

def body_follow(map, snake_head_x, snake_head_y, snake_body, snake_length):
    """Updates and stores body coordinates and length"""
    if map[snake_head_x][snake_head_y] == "🍎" :
        snake_body.append([snake_head_x, snake_head_y])
    if len(snake_body) <= snake_length:
        snake_body.append([snake_head_x, snake_head_y])
    if len(snake_body) > snake_length:
        snake_body.pop(0)
    
def append_body(map, snake_body):
    """Append all the snake cells to the map"""
    for i in snake_body:
        map[i[1]][i[0]] = "1"

def body_update(snake_body, snake_head_x, snake_head_y):
    """Update snake body display"""
    snake_body.pop()
    snake_body.insert(0, [snake_head_x, snake_head_y])

def check_apple(snake_head_coordonates, apple_coordonates, is_eaten, stdscr):
    """Check if snake is eating an apple"""
    if snake_head_coordonates == apple_coordonates:
        return True
    return False

def detect_keys(stdscr, snake_body, snake_length, x, y): 
    """Detects the user input"""
    map = map_creation(x, y)
    (snake_head_x, snake_head_y) = place_snake_head(y)

    for i in range(snake_length):
        snake_body.append([snake_head_x - i, snake_head_y])
    append_body(map, snake_body)

    (random_x, random_y) = place_fruit(x, y)
    map[random_y][random_x] = "🍎"
    render(stdscr, map)
    
    is_moving = False
    is_eaten = False #todo: rename to is_apple_eaten
    direction = "right"
    player_alive = True
    while player_alive == True:
        key = stdscr.getch()
        if key == 259 and direction != "down":
            direction = "up"
            is_moving = True
            snake_head_y -= 1
            body_update(snake_body, snake_head_x, snake_head_y)
        elif key == 258 and direction != "up":
            direction = "down"
            is_moving = True
            snake_head_y += 1
            body_update(snake_body, snake_head_x, snake_head_y)
        elif key == 261 and direction != "left":
            direction = "right"
            is_moving = True
            snake_head_x += 1
            body_update(snake_body, snake_head_x, snake_head_y)
        elif key == 260 and direction != "right":
            direction = "left"
            snake_head_x -= 1
            body_update(snake_body, snake_head_x, snake_head_y)
        
        stdscr.clear()

        is_eaten = check_apple((random_x, random_y), (snake_head_x, snake_head_y), is_eaten, stdscr)
        if is_eaten == True:
            (random_x, random_y) = place_fruit(x, y)
            stdscr.addstr(str(is_eaten))
            is_eaten = False
            stdscr.addstr(str(random_x))
        
        map = map_creation(x, y)
        #(random_x, random_y) = place_fruit(12, 12)
        #body_follow(map, snake_head_x, snake_head_y, snake_body, snake_length)
        map[random_y][random_x] = "🍎"
        stdscr.addstr(str(random_x))
        

        #map[snake_head_y][snake_head_x] = "1"
        
        append_body(map, snake_body)
        #map[snake_head_y][snake_head_x] = "1" 
        #for y in range(snake):
        #    for x in range(len(snake_body[y])):
        #        map[snake_body[y]][snake_body[x]] = "1"
        render(stdscr, map)
    #game_over()

def initialize_colors():
    """Creates the colors and color pairs used in the game"""
    curses.start_color()
    curses.init_color(1, 236, 28, 40)
    curses.init_color(2, 352, 112, 540)
    curses.init_color(3, 672, 340, 988)
    curses.init_color(4, 296, 888, 512)
    curses.init_pair(10, 1, 2)
    curses.init_pair(11, 2, 1)
    curses.init_pair(12, 2, 3)
    curses.init_pair(13, 4, 4)


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
    print(map)
    return map

def return_center(stdscr, map_len, amount):
    """Return the abciss an element should have to be centered"""
    (height,width) = stdscr.getmaxyx()
    window_center = int(width / 2)
    map_center = math.ceil(map_len / 2) * amount
    return window_center - map_center

def print_text(stdscr, text):
    """Handle title display"""
    
    max_width = 0 
    for i in range(len(text)):
        if len(text[i]) > 0:
            max_width = len(text[i])
    base_x = return_center(stdscr, max_width, 1)
    x = base_x
    y = 0
    for i in range(len(text)):
        for j in range(len(text[i])):
            stdscr.addstr(y, x, text[i][j])
            x += 1
        y += 1
        x = base_x


def render(stdscr, map):
    """The function rendering the map on the screen"""
    text = read_json(stdscr)
    print_text(stdscr, text)
    base_x = return_center(stdscr, len(map[0]), 2)
    x = base_x
    y = len(text) + 1
    for i in range(len(map)):
        for j in range(len(map[i])):
            #print(map[i][j], end="")
            print_pixel(x, y, stdscr, map[i][j])
            x += 2
        x = base_x
        y += 1

def place_fruit(max_x, max_y=None):
    """Place a fruit on a random case"""
    if max_y == None:
        max_y = max_x

    random_x = random.randint(0, max_x - 1)
    random_y = random.randint(0, max_y - 1)

    return (random_x, random_y)

def main(stdscr):
    """Entry point"""
    x = 15
    y = 15
    snake_body = []
    snake_length = 3
    initialize_colors()
    #blank_map = map_creation(x, y)
    #map = blank_map 
    
    #print(random_x, random_y)
    detect_keys(stdscr, snake_body, snake_length, x, y)
    


curses.wrapper(main)
