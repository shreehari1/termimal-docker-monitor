from datetime import datetime
import time
from rich.console import Console
from rich.layout import Layout
from rich.live import Live
from rich.text import Text

from resources import docker,host


console = Console()
layout = Layout()

layout.split(
    Layout(name="header", size=1),
    Layout(ratio=1, name="main"),
    Layout(size=10, name="footer"),
)

layout["main"].split_row(Layout(name="left"), Layout(name="right"))

layout["left"].update(docker.docker_stats())
layout["right"].update(docker.docker_container_info())

class Clock:
    """Renders the time in the center of the screen."""

    def __rich__(self) -> Text:
        return Text(datetime.now().ctime(), style="bold magenta", justify="center")

layout["header"].update(Clock())



with Live(layout, screen=True, redirect_stderr=False) as live:
    try:
        while True:
            layout["footer"].update(host.updateStats())
            time.sleep(1)
    except KeyboardInterrupt:
        pass


