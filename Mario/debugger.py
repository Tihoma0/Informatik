import pygame as pg
to_log = []
primary_to_log = []
needed_key_to_log = pg.K_1
is_needed_key_to_log_pressed = False
has_to_log = False

normal_title = ""

def log(*args, **kwargs):
    to_log.append((args, kwargs))

def primary_log(*args, **kwargs):
    primary_to_log.append((args, kwargs))

def setup():
    global normal_title
    normal_title = pg.display.get_caption()

def print_log(keys: list[bool]):
    global is_needed_key_to_log_pressed, has_to_log
    if keys[needed_key_to_log] and not is_needed_key_to_log_pressed:
        is_needed_key_to_log_pressed = True
        has_to_log = not has_to_log
    is_needed_key_to_log_pressed = keys[needed_key_to_log]
    if has_to_log:
        for args, kwargs in to_log:
            print(*args, **kwargs)
        caption = normal_title[0] + " - Primary Log: "
        for args, kwargs in primary_to_log:
            caption += str(*args, **kwargs) + ", "
        pg.display.set_caption(caption)
    else:
        pg.display.set_caption(normal_title[0])
    to_log.clear()
    primary_to_log.clear()