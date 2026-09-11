from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static, RichLog, Collapsible, ListView, ListItem, Label, SelectionList, Rule, ListView, Pretty
from textual.containers import VerticalGroup, HorizontalGroup, Container, Vertical, Grid
from textual import on
from textual import events
from pathlib import Path
import subprocess
import os


def get_os_info():
    # 1. Start the first process (e.g., cat /etc/os-release)
    p1 = subprocess.Popen(["cat", "/etc/os-release"],
                          stdout=subprocess.PIPE)
    # 2. Start the second process and plug p1's output into p2's input (e.g., grep ID)
    p2 = subprocess.Popen(["grep", "ID"], stdin=p1.stdout,
                          stdout=subprocess.PIPE, text=True)
    # 3. Allow p1 to receive a SIGPIPE if p2 exits early
    p1.stdout.close()
    # 4. Get the final result
    output, error = p2.communicate()
    return output

# this should be a for loop of the data/ dir to create containers with the Container of such file


def fetch_file(path):
    r_path = "./data/"
    os_path = "os.text"
    de_path = "de.text"
    gs_path = "gs.text"
    compositor_path = "comp.text"
    wm_path = "wm.text"
    panel_path = "panel.text"
    launcher_path = "launch.text"
    terminal_path = "terminal.text"
    f_explorer_path = "fe.text"
    editor_path = "editor.text"

    match path:
        case "OS":
            return r_path+os_path
        case "Desktop-Enviroment":
            return r_path+de_path
        case "Grafical-Server":
            return r_path+gs_path
        case "Compositor":
            return r_path+compositor_path
        case "Window-Manager":
            return r_path+wm_path
        case "Panel":
            return r_path+panel_path
        case "Launcher":
            return r_path+launcher_path
        case "terminal":
            return r_path+terminal_path
        case "file-explorer":
            return r_path+f_explorer_path
        case "editor":
            return r_path+editor_path

# this should be the create containers func


def get_options_list(path):
    filePath = fetch_file(path)
    with open(filePath, "r", encoding="utf-8") as f:
        l = f.read().splitlines()
        o_list = [ListItem(Label(f'{li}'),
                           name=f'{li}',
                           id=f'{
                           li}'.replace(" ", "-"), classes="item",) for li in l]
        for n, line in enumerate(l):
            global indexDict
            indexDict[line] = n

        return o_list



indexDict = {}
os_label = Label("OS", name="OS")
de_label = Label("Desktop-Enviroment", name="Desktop-Enviroment")
gs_label = Label("Grafical-Server", name="Grafical-Server")
comp_label = Label("Compositor", name="Compositor")
wm_label = Label("Window-Manager", name="Window-Manager")
pan_label = Label("panel", name="Panel")
launcher_label = Label("launcher", name="Launcher")
terminal_path_label = Label("terminal", name="terminal")
filex_label = Label("file-explorer", name="file-explorer")
editor_label = Label("editor", name="editor")


class Content(Grid):
    def compose(self):
        with Container(classes="box", id="OS"):
            yield os_label
            yield ListView(*get_options_list(os_label.name), )
        with Container(classes="box",):
            yield de_label
            yield ListView(*get_options_list(de_label.name), )
        with Container(classes="box",):
            with Container(classes="gs-comp",):
                yield gs_label
                yield ListView(*get_options_list(gs_label.name), )
            with Container(classes="gs-comp", id="Compositor"):
                yield comp_label
                yield ListView(*get_options_list(comp_label.name),)
        with Container(classes="box",):
            yield wm_label
            yield ListView(*get_options_list(wm_label.name), )
        with Container(classes="box",):
            yield pan_label
            yield ListView(*get_options_list(pan_label.name),)
        with Container(classes="box",):
            yield launcher_label
            yield ListView(*get_options_list(launcher_label.name), id="Launcher")
        with Container(classes="box",):
            yield filex_label
            yield ListView(*get_options_list(filex_label.name), )
        with Container(classes="box",):
            yield editor_label
            yield ListView(*get_options_list(editor_label.name), )
        with Container(classes="box",):
            yield terminal_path_label
            yield ListView(*get_options_list(terminal_path_label.name), )
        with Container(classes="box log",):
            yield RichLog()


class MyApp(App):
    CSS_PATH = "tuizzard.css"
    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]

    def compose(self):
        yield Header()
        yield Footer()
        yield Content()

    def on_mount(self) -> None:
        self.query_one(RichLog).write((get_os_info()))
        self.query_one(RichLog).write(indexDict)
        elem=self.query_one("#Launcher")
        elem.index=indexDict["Dmenu"]
        elem.disabled=True
        
    def on_key(self, event: events.Key):
        self.query_one(RichLog).write(event)

    def on_list_view_selected(self, event: ListView.Selected):
        self.query_one(RichLog).write(event.item)
        self.query_one(RichLog).write(event.list_view)
        if event.item.id == "X11":
            self.query_one("#Compositor").remove_class("disabled")
        if event.item.id == "Wayland":
            self.query_one("#Compositor").add_class("disabled")
        if event.item.id == "Windows":
            self.app.exit()

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"
        )


if __name__ == "__main__":
    app = MyApp()
    app.run()
