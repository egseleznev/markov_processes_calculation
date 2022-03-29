import sys
import os
from cx_Freeze import setup, Executable

# ADD FILES
files = ['ASD.ico', 'themes/', 'images/', 'DejaVuSansCondensed.ttf']

# TARGET
target = Executable(
    script="main.py",
    base="Win32GUI",
    icon="ASD.ico",
    shortcut_name='Калькулятор марковских процессов',
    shortcut_dir='ProgramMenuFolder'
)

# SETUP CX FREEZE
setup(
    name="Калькулятор марковских процессов",
    version="1.0.1",
    description="Расчет марковских процессов",
    author="Seleznev Egor",
    options={'build_exe': {'include_files': files}},
    executables=[target]

)
