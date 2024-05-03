import pygame
from view.ui.popup_box import PopupBox
from view import view_constants as view_cst
from view.ui.utils import wrap_text
from view.ui.button import Button

class DialogueBox(PopupBox):
    def __init__(self, screen):
        width, height = view_cst.WIDTH - 20, view_cst.HEIGHT // 3-20
        super().__init__(screen, width, height)
        self.default_button_image = None #pygame.image.load("./assets/buttons/wood_button.png").convert_alpha()
        self.default_pressed_button_image = None #pygame.image.load("./assets/buttons/wood_button_pressed.png").convert_alpha()
        self.accept_button = None
        self.decline_button = None
        self.text_offsets = {
            "small": 2,
            "medium": 4,
            "large": 6,
        }

        self.fonts = {
            "name": pygame.font.SysFont("Arial", 26),
            "text": pygame.font.SysFont("Arial", 18),
            "exit": pygame.font.SysFont("Arial", 24),
            "button": pygame.font.SysFont("Arial", 20),
            "accept_deny": pygame.font.SysFont("Arial", 20)
        }
        self.background_color = view_cst.PARCHMENT_COLOR
        self.name_color = view_cst.COFFEE_BROWN_3

    def set_background_color(self, color):
        self.background_color = color

    def set_name_color(self, color):
        self.name_color = color

    def set_button_images(self, default_button_image, default_pressed_button_image):
        self.default_button_image = pygame.image.load(default_button_image).convert_alpha()
        self.default_pressed_button_image = pygame.image.load(default_pressed_button_image).convert_alpha()

    def create_dialogue(self, npc_name, dialogue_text):
        #Width and Height offset compared to the parent surface
        self.width_offset = 10
        self.height_offset = 2*view_cst.HEIGHT // 3-50
        self.rect.topleft = (self.width_offset, self.height_offset)
        self.surface.fill(self.background_color)

        name_rendered = self.fonts["name"].render(npc_name, True, self.name_color)
        name_pos = (10 + self.width // 2 - name_rendered.get_width() // 2, 10)
        self.surface.blit(name_rendered, name_pos)

        # Use the wrap_text function to get the lines of dialogue
        lines = wrap_text(dialogue_text, self.width - 20, self.fonts["text"], view_cst.TEXT_COLOR)
        y_offset = 80  # Start below the name
        for line_surface in lines:
            # Calculate the x position to center the line
            line_width = line_surface.get_width()
            x_offset = 20 + (self.width - 20 - line_width) // 2  # Adjust to center the line

            # Blit each line of text, incrementing the y_offset for each line
            self.surface.blit(line_surface, (x_offset, y_offset))
            y_offset += line_surface.get_height() + 5  # Adjust spacing between lines

        # self.show = True

    def reinitialize_close_button(self):
        self.close_button = None

    def create_close_button(self):
        button_width = 30
        button_height = 35
        #TODO: fix this when changing dialogue type: previous button will be re-displayed
        if getattr(self, 'close_button', None):
            self.render_close_button()
        else:
            self.close_button = Button(self.default_button_image, self.fonts["exit"], button_width, button_height, self.text_offsets["small"],
                                        (self.width - button_width - 10, 10), "X", self.rect.topleft,
                                        pressed_image=self.default_pressed_button_image)
            self.render_close_button()

    def create_prev_button(self):
        button_width = 80
        button_height = 40
        if getattr(self, 'prev_button', None):
            self.render_prev_button()
        else:
            self.prev_button = Button(self.default_button_image, self.fonts["button"], button_width, button_height, self.text_offsets["medium"],
                                      (10, self.height - button_height - 10), "Prev", self.rect.topleft,
                                      pressed_image=self.default_pressed_button_image)
            self.render_prev_button()

    def create_next_button(self):
        button_width = 80
        button_height = 40
        if getattr(self, 'next_button', None):
            self.render_next_button()
        else:
            self.next_button = Button(self.default_button_image, self.fonts["button"], button_width, button_height, self.text_offsets["medium"],
                                      (self.width - button_width - 10, self.height - button_height - 10), "Next", self.rect.topleft,
                                      pressed_image=self.default_pressed_button_image)
            self.render_next_button()



    def create_accept_decline_buttons(self):
        button_width = 150
        button_height = 50
        if getattr(self, 'accept_button', None) and getattr(self, 'decline_button', None):
            self.render_accept_decline_buttons()
        else:
            self.accept_button = Button(self.default_button_image, self.fonts["accept_deny"], button_width, button_height, self.text_offsets["large"],
                                        (self.width // 3 - button_width/2, self.height - button_height - 10),
                                        "Accept", self.rect.topleft, pressed_image=self.default_pressed_button_image)
            self.decline_button = Button(self.default_button_image, self.fonts["accept_deny"], button_width, button_height, self.text_offsets["large"],
                                         (2*self.width // 3 - button_width/2, self.height - button_height - 10),
                                         "Decline", self.rect.topleft, pressed_image=self.default_pressed_button_image)
            self.render_accept_decline_buttons()

    def create_end_quest_button(self):
        button_width = 150
        button_height = 50
        if getattr(self, 'end_quest_button', None):
            self.render_end_quest_button()
        else:
            self.end_quest_button = Button(self.default_button_image, self.fonts["accept_deny"], button_width, button_height, self.text_offsets["large"],
                                        (self.width // 2 - button_width/2, self.height - button_height - 10),
                                        "End quest", self.rect.topleft, pressed_image=self.default_pressed_button_image)
            self.render_end_quest_button()


    def create_generate_quest_button(self):
        button_width = 200
        button_height = 50
        if getattr(self, 'generate_quest_button', None):
            self.render_generate_quest_button()
        else:
            self.generate_quest_button = Button(self.default_button_image, self.fonts["accept_deny"], button_width, button_height, self.text_offsets["large"],
                                        (self.width // 2 - button_width/2, self.height - button_height - 10),
                                        "Generate quest", self.rect.topleft, pressed_image=self.default_pressed_button_image)
            self.render_generate_quest_button()


    def render_close_button(self):
        self.close_button.draw(self.surface)

    def render_accept_decline_buttons(self):
        self.accept_button.draw(self.surface)
        self.decline_button.draw(self.surface)

    def render_end_quest_button(self):
        self.end_quest_button.draw(self.surface)

    def render_prev_button(self):
        self.prev_button.draw(self.surface)

    def render_next_button(self):
        self.next_button.draw(self.surface)

    def render_generate_quest_button(self):
        self.generate_quest_button.draw(self.surface)

    def handle_events(self, event):
        pass