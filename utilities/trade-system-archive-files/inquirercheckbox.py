import os
import sys
from pprint import pprint

from inquirer.themes import Default

sys.path.append(os.path.realpath("."))
import inquirer 

class WorkplaceFriendlyTheme(Default):
    """Custom theme replacing X with Y and o with N"""

    def __init__(self):
        super().__init__()
        self.Checkbox.selected_icon = "Y"
        self.Checkbox.unselected_icon = "N"


strategy_questions = [
    inquirer.Checkbox(
        "list_strategies",
        message="What are you interested in?",
        choices=["DeviL", "DeviS"]
    ),
]

answers = inquirer.prompt(strategy_questions, theme=WorkplaceFriendlyTheme())

pprint(answers["list_strategies"])
