import pygame
import view.view_constants as view_cst

def wrap_text(text, max_width, font, color):
    font = font
    wrapped_lines = []
    words = text.split()
    line = []
    line_width = 0

    for word in words:
        word_surface = font.render(word, True, color)
        word_width, word_height = word_surface.get_size()

        if line_width + word_width > max_width-10:
            wrapped_lines.append(font.render(' '.join(line), True, color))
            line = [word]
            line_width = word_width
        else:
            line.append(word)
            line_width += word_width

    if line:
        wrapped_lines.append(font.render(' '.join(line), True, color))

    return wrapped_lines
