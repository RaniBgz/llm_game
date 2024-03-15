from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static, Button
from textual.containers import ScrollableContainer
from textual.reactive import Reactive
from textual.containers import Container
from textual.widgets import Welcome

''' [LAYOUT] Will be useful: https://textual.textualize.io/guide/layout/#__tabbed_6_3'''
#TODO: understand how to do something when clicking a button (handling event)
#TODO: understand how to change the current scene or clean the layout

class ItemLine(Static):
    """A widget to display an item."""

class GameTitle(Static):
    """A widget to display the game title."""


class GameInterface(App):
    BINDINGS = [("q", "quit", "Quit"), ("d", "toggle_dark", "Toggle dark mode")]
    # Track the current scene
    current_scene: Reactive[str] = Reactive("menu")

    # def compose(self) -> ComposeResult:
    #     yield Header()
    #     yield Footer()
    #     yield ScrollableContainer(ItemLine("Item 1"), ItemLine("Item 2"), ItemLine("Item 3"))

    def compose(self) -> ComposeResult:
        yield Header()

        if self.current_scene == "menu":
            yield Container(
                Static("My Game Title"),
                Button("Play", id="play"),
                Button("Quit", id="quit"),
                id="main_menu"
            )
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Event handler called when a button is pressed."""
        if event.button.id == "play":
            pass
        elif event.button.id == "quit":
            pass

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.dark = not self.dark




# class Stopwatch(Static):
#     """A stopwatch widget."""
#     def compose(self) -> ComposeResult:
#         """Create child widgets of a stopwatch."""
#         yield Button("Start", id="start", variant="success")
#         yield Button("Stop", id="stop", variant="error")
#         yield Button("Reset", id="reset")