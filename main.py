# Debugger
from icecream import ic

# String
import unicodedata
import re

# System
import sys
from pathlib import Path, PosixPath, WindowsPath, PurePath

# Defaults
from dataclasses import dataclass

# Graphical
from PyQt5 import uic;
from PyQt5.QtCore import Qt
from PyQt5.QtGui import (
    QIcon, QPixmap
)
from PyQt5.QtWidgets import (
    QApplication, QMainWindow,
    QWidget
)

# Graphical Resources
import resources

###############################################
#                 CONST                       #
###############################################

GODOT_PROJECTS_PATH: str = "."
REDOT_PROJECTS_PATH: str = "."
URSINA_PROJECTS_PATH: str = "."

###############################################


app = QApplication([])
window: QMainWindow = uic.loadUi("main.ui")


################################################
#               DATACLASSES                    #
################################################

@dataclass
class AppInfo:
    logo:  str
    image: str
    color: str
    name:  str
    description: str
    work_path: Path

    def __post_init__(self):
        self.name = f' {self.name}'
        self.showfunc = lambda: Screens.changeWindow(self)


@dataclass
class CreationRequest:
    current_engine: AppInfo
    project_name:str
    fpc_enabler: bool
    prototype_textures: bool
    default_shaders: bool
    environment: bool
    
    def __post_init__(self):
        self.project_name = MainAppTols().clear_string(self.project_name)

################################################


################################################
#                  ENGINES                    #
###############################################

current_engine: AppInfo | None = None
Godot = AppInfo(name="GODOT", 
                description="Your free, open-source game engine.",
                logo=":/logo/godot_monochrome.svg", 
                image=":logo/godot_normal.svg",
                color="#4d9fdc",
                work_path=Path(GODOT_PROJECTS_PATH))

Redot = AppInfo(name="REDOT",
                description="Open-source engine for everyone.",
                logo=":/logo/redot_monochrome.svg", 
                image=":/lateral_images/redot_chan.png",
                color="#760b1e",
                work_path=Path(REDOT_PROJECTS_PATH))

Ursina = AppInfo(name="Ursina",
                description="A Python powered, open source game engine",
                logo=":/logo/ursina.webp",
                image=":/lateral_images/ursina_base.png",
                color="#aa65c3",
                work_path=Path(URSINA_PROJECTS_PATH))


class MainAppTols():
    def __init__(self):
        pass

    def createApp(self):
        content: dict = self.getInputs()
        path: Path = Path(current_engine.work_path) / content.project_name
        creationDirs = [
            "autoloads",
            "addons",
            "assets/models",
            "assets/textures",
            "resources/materials/3d",
            "resources/materials/2d",
            "resources/materials/canvas",
            "resources/scenes/characters",
            "resources/scenes/maps",
            "resources/scenes/experimental",
            "resources/scripts/local",
            "resources/scripts/experimental",
            "resources/shaders/spatial",
            "resources/shaders/canvas",
            "resources/visual_shaders/spatial",
            "resources/visual_shaders/canvas"
        ]
        
        splitted_folders: list = [Path(*x.split('/')) for x in creationDirs]
        full_paths: list = [path / item for item in splitted_folders]

        for current_path in full_paths:
            current_path.mkdir(parents=True, exist_ok=True)
            ic(current_path)



    def clear_string(self, content: str) -> str:
        content = unicodedata\
                    .normalize('NFKC', content)\
                    .encode('ascii', 'ignore')\
                    .decode('ascii')

        content = re.sub(r'[^a-zA-Z0-9._-]', '_', content)
        content = content.strip('_')
        return content.lower()


    def getInputs(self) -> CreationRequest:
        content = CreationRequest(
            current_engine=current_engine,
            project_name=window.project_name.text(),
            fpc_enabler=window.fpc_enabler.isChecked(),
            prototype_textures=window.prototype_txt_enabler.isChecked(),
            default_shaders=window.shaders_enabler.isChecked(),
            environment=window.environment_enabler.isChecked()
        )
        
        return content



    # TODO: Fix this function
    def changeObjectProperty(self, obj: QWidget, object_color: str, property: str):
        entire_stylesheet = obj.styleSheet()
        oldline = [x for x in entire_stylesheet.split("\n") if property in x][0]
        newline = f"\t{property}: {object_color};"

        obj.setStyleSheet(entire_stylesheet.replace(oldline, newline))


    def ok_change_my_checkable_buttons(self, color: str):
        w = window
        
        [self.changeObjectProperty(
                x,
                color,
                "border-bottom-color"
            ) for x in [
                w.fpc_enabler, 
                w.prototype_txt_enabler, 
                w.camera_preview_enabler,
                w.shaders_enabler, 
                w.environment_enabler
            ]
        ]
        

class Screens:
    def changeWindow(appinfo: AppInfo):
        mat = MainAppTols()
        
        icon: QIcon = QIcon(appinfo.logo)
        image: QPixmap = QPixmap(appinfo.image)
        
        window.engine_logo.setIcon(icon)
        window.main_image.setPixmap(image)
        window.engine_logo.setText(appinfo.name)
        window.phrase_label.setText(appinfo.description)

        mat.ok_change_my_checkable_buttons(appinfo.color)
        mat.changeObjectProperty(window.create_btn, appinfo.color, "background-color")
        mat.changeObjectProperty(window.project_name, appinfo.color, "border-bottom-color")
        
        global current_engine
        current_engine = appinfo


class ButtonLinker:
    def __init__(self):
        createapp = lambda: MainAppTols().createApp()
        
        window.exit_btn.clicked.connect(sys.exit)
        window.minimize_btn.clicked.connect(window.showMinimized)
        
        window.godot_btn.clicked.connect(Godot.showfunc)
        window.redot_btn.clicked.connect(Redot.showfunc)
        window.ursina_btn.clicked.connect(Ursina.showfunc)
        window.create_btn.clicked.connect(createapp)


def main() -> None:
    
    window.setWindowFlags(Qt.FramelessWindowHint)
    window.setAttribute(Qt.WA_TranslucentBackground)
    
    ButtonLinker()
    
    # Make it run!!!!
    Redot.showfunc()
    window.show()


if __name__ == "__main__":
    main()
    app.exec()