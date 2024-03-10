class Command:
    """ Interface for commands in the game. """
    def execute(self):
        raise NotImplementedError()

class MoveCommand(Command):
    def __init__(self, entity, direction):
        self.entity = entity
        self.direction = direction

    def execute(self):
        # Implement movement logic based on direction
        self.entity.location = self.entity.location + self.direction  # Simplistic

class UseItemCommand(Command):
    def __init__(self, player, item):
        self.player = player
        self.item = item

    def execute(self):
        # Implement the effects of using the item on the player
        if self.item.name == "Healing Potion":
            self.player.hp += 20


# from textual.widgets import Button
#
# # ... other Textual setup...
#
# def on_heal_button_clicked(event):
#     player = get_current_player()  # Assuming you can get the player
#     potion = player.inventory.find_item("Healing Potion")
#     command = UseItemCommand(player, potion)
#     command_processor.execute_command(command)  # Assuming you have a command processor
#
# # ... Add the button to your Textual interface ...
# self.main_content.mount(Button("Drink Potion", on_click=on_heal_button_clicked))

# Inside your Textual App class

# def handle_item_clicked(self, message):
#     clicked_item = message.data  # Assuming data contains the Item instance
#     command = ExamineCommand(clicked_item)
#     command.execute()  # Or add to a queue to be executed in the game loop