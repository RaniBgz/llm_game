
from model.character import Character
from model.item import Item
from model.object import Object
import random  # For a bit of randomness later

from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Placeholder, Label, TextArea

class GameInterface(App):
    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]
    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.dark = not self.dark


if __name__ == "__main__":
    app = GameInterface()
    app.run()



    # def on_mount(self) -> None:
    #
    #     # Initialize your widgets here directly or store them from compose
    #     self.main_content = Placeholder(name="main_content")
    #     self.set_interval(1, self.update_content)  # Assuming you have a method to update content regularly
    # async def update_content(self):
    #     # Example method to update content; adjust as needed
    #     player = Character("Bard", "A friendly language model.", 100)
    #     sword = Item("Rusty Sword", "A slightly worn sword.", 10, 2)
    #     # Update the main_content directly
    #     self.main_content.update(Label(f"Character: {player.name}\nDescription: {player.description}"))
    #     self.main_content.update(Label(f"\nItem: {sword.name}\nDescription: {sword.description}"))

    # def on_mount(self) -> None:
    #     self.set_interval(1, self.update_content)
    #
    # async def update_content(self):
    #     player = Character("Bard", "A friendly language model.", 100)
    #     sword = Item("Rusty Sword", "A slightly worn sword.", 10, 2)
    #     # Remove existing children if needed
    #     self.main_content.clear()
    #     # Add new labels as children
    #     self.main_content.mount(
    #         Label(f"Character: {player.name}\nDescription: {player.description}"),
    #         Label(f"\nItem: {sword.name}\nDescription: {sword.description}")
    #     )