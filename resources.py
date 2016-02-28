from os.path import join

def get_font(name):
    return join('resources', 'fonts', name)

def get_hiscores(name):
    return join('resources', 'hiscores', name)

def get_sound(name):
    return join('resources', 'sounds', name)

def get_music(name):
    return join('resources', 'music', name)

def get_image(name):
    return join('resources', 'images', name)

def get_sprite(name):
    return join('resources', 'sprites', name)
