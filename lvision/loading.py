''''Module for loading screen related '''


def get_is_loading_screen(img):
    '''Returns if in loading screen'''
    return (img[758, 9] == (156, 156, 157)).all()
