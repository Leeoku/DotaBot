from datetime import datetime
from .colour import color
from os import system, name 
from time import sleep 

_time = datetime.now()

def fmtTime():
    return _time.strftime("%b %d %Y %H:%M:%S")

red = color.RED
green = color.GREEN
cyan = color.CYAN
dcyan = color.DARKCYAN
blue = color.BLUE
yellow = color.YELLOW
purple = color.PURPLE
bold = color.BOLD
underline = color.UNDERLINE
end = color.END

  
def clearterm():  
    _ = system('cls') if name == 'nt' else system('clear') 
  

def cd(place, color):
    if color == "red":
        return f"{red}{place}{end}"
    if color == "green":
        return f"{green}{place}{end}"
    if color == "cyan":
        return f"{cyan}{place}{end}"
    if color == "dcyan":
        return f"{dcyan}{place}{end}"
    if color == "blue":
        return f"{blue}{place}{end}"
    if color == "yellow":
        return f"{yellow}{place}{end}"
    if color == "purple":
        return f"{purple}{place}{end}"
    if color == "bold":
        return f"{bold}{place}{end}"
    if color == "underline":
        return f"{underline}{place}{end}"




