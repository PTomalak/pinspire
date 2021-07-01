import os,sys, ctypes, json, math
import pygame as pg
from pygame import draw
from pygame import key
from pygame.display import update
from pygame.event import get
from pygame.locals import *
from pygame import gfxdraw
from simpleimage import SimpleImage




#########################################################



def main():

    #anti - stretch for pygame
    ctypes.windll.user32.SetProcessDPIAware()
    pg.init()
    pg.font.init()
    pg.mouse.set_visible(True)
    

    background_color = pg.Color("black")
    active_color = pg.Color("white")
    morpheon = pg.Color(38, 50, 56)

    


    sans = pg.font.Font(os.path.join('fonts', 'FantasqueSansMono-Regular.ttf'), 35)

    font = sans

    initial_size = [1920,1080]

    flags = pg.RESIZABLE

    screen = pg.display.set_mode(initial_size, flags)
    
    divide_screen()

    pg.display.set_caption("π nspire")


    #debug_startup()

    
    
    clock = pg.time.Clock()
    continue_running = True




#########################################################

    scale = 1
    active_function = "x**2"
    key = "no"


    while continue_running:

        window_info = divide_screen()

        clock.tick(60)

        background = pg.Surface(screen.get_size())
        background = background.convert()
        background.fill(background_color)
    
        mouse_pos = pg.mouse.get_pos()

        graph = pg.Surface(window_info[0].size)
        graph.fill(pg.Color("black"))
        graph_info = pg.Surface(window_info[1].size)
        graph_info.fill(pg.Color(morpheon))
        console = pg.Surface(window_info[2].size)
        console.fill(pg.Color(morpheon))
        
        

        
        graph_function(active_function, graph, scale)


        #text = pg.font.Font.render(sans, "text", True, active_color)
        

        for event in pg.event.get():
            if event.type == pg.QUIT:
                continue_running = False
            elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                continue_running = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 4:
                    key = "left"
                elif event.button == 5:
                    key = "right"
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_BACKSPACE:
                    active_function = active_function[:-1]
                else:
                    active_function += event.unicode
                
                pg.time.wait(200)
                
        
        scale = handle_scale(key, scale)

        
        screen.blit(background, (0, 0))
        
        screen.blit(graph_info, window_info[1].topleft)
        screen.blit(console, window_info[2].topleft)
        screen.blit(right_window_info(scale, font, active_color), window_info[1].topleft)
        screen.blit(console_info(font, active_color, active_function), window_info[2].topleft)
        

        #debug_running()
        
        #to_update = pg.Surface.get_rect(graph)
        try:
            x=1
            eval(active_function)
            screen.blit(graph, (0, 0))
            backup_graph = pg.Surface.copy(graph)
        except:
            screen.blit(backup_graph, (0, 0))
        


        pg.display.update()

        key = "no"
            
    
    pg.quit()


#########################################################


def get_display_info():
    print("DP INFO")
    print(pg.display.Info())
    print("DP MODES")
    print(pg.display.list_modes())
    print("DP OK?")
    print(pg.display.mode_ok((3840,2160)))
    print("DP DRIVER")
    print(pg.display.get_driver())

def get_screen_size():
    screen_info = pg.display.Info()
    x = screen_info.current_w
    y = screen_info.current_h
    screen_size = [x,y]
    return screen_size

def detect_screen_size_change():
    pass

def debug_startup():
    get_display_info()
    print("")

def debug_running():
    print("screen size", get_screen_size())
    print("mouse position", pg.mouse.get_pos())
    print("")

def initialize_colors():
    with open(os.path.join('settings', 'colors.json')) as f:
        data = json.load(f)
        color = []
        for value in data:
            R = data[value][0]
            G = data[value][1]
            B = data[value][2]
            value = pg.Color(R,G,B)
            color.append(value)
        print(color)
        return color

def divide_screen():
    screen_size = get_screen_size()
    screen_ratio_x = 0.7
    screen_ratio_y = (screen_size[1]-40) / screen_size[1]
    
    main_window_x = int(screen_size[0] * screen_ratio_x)
    main_window_y = int(screen_size[1] * screen_ratio_y)
    main_window = [0, 0, main_window_x, main_window_y]
    right_window = [main_window_x, 0, screen_size[0]-main_window_x, main_window_y]
    bottom_window = [0, main_window_y, screen_size[0], screen_size[1]-main_window_y]
    window_info = []
    window_info.append(Rect(main_window))
    window_info.append(Rect(right_window))
    window_info.append(Rect(bottom_window))
    #print(window_info)
    return window_info

def draw_corners(surface):
    color = pg.Color("orange")
    x = surface.get_width() - 1
    y = surface.get_height() - 1
    gfxdraw.pixel(surface, 0, 0, color)
    gfxdraw.pixel(surface, x, 0, color)
    gfxdraw.pixel(surface, 0, y, color)
    gfxdraw.pixel(surface, x, y, color)

def graph_function(function, surface, scale):
    pix_width = surface.get_width()
    pix_height = surface.get_height()
    pix_width_center = pix_width//2 + 1
    x_left = ((-1) * pix_width_center + 1) * scale
    y_plot = []
    for column in range(pix_width):
        result = 0
        x_current = x_left + scale * column
        result = calculate_y(x_current, function, y_plot, column)
        y_plot.append(result)
    #print(y_plot)
    draw_graph(y_plot, surface, pix_width_center, pix_height, pix_width, scale)

def calculate_y(x, function, y_plot, column):
    try:
        y_value = y_plot[column]
    except IndexError:
        y_value = 0
        
    try:
        y_value = eval(function)
    except:
        pass

    try:
        return(float(y_value))
    except:
        return 0

def draw_graph(y_plot, surface, center_x, height, width, scale):
    for column in range(len(y_plot)):
        if y_plot[column] < height//2 * scale and y_plot[column] > (-1)* height//2 * scale:
            gfxdraw.pixel(surface, column, int(-y_plot[column]//scale + height//2), pg.Color("white"))
    for x in range(width):
        gfxdraw.pixel(surface, x, int(height//2), pg.Color("yellow"))
        if x == center_x:
            for y in range(height):
                gfxdraw.pixel(surface, center_x-1, y, pg.Color("yellow"))


def console_info(font, active_color, active_function):
    
    text = pg.font.Font.render(font, "F(x) = " + active_function + "|", True, active_color)
    return text

def handle_scale(key, scale):
    if key == "right":
        scale = scale*1.1
        return scale
    elif key == "left":
        scale = scale*0.9
        return scale
    else:
        return scale

def right_window_info(scale, font, active_color):
    to_print = "scale = " + str(scale)
    text = pg.font.Font.render(font, to_print[:13], True, active_color)
    return text

#########################################################


if __name__ == '__main__':
    main()