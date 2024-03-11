from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static, Button
from textual.containers import ScrollableContainer

class ItemLine(Static):
    """A widget to display an item."""

class GameInterface(App):
    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]
    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield ScrollableContainer(ItemLine("Item 1"), ItemLine("Item 2"), ItemLine("Item 3"))
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