import nextcord
from nextcord import ButtonStyle

class github_button(nextcord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(
            nextcord.ui.Button(
                label="Open in browser",
                url="https://github.com/codeman1o1/TIJK-Bot",
                style=ButtonStyle.url,
            )
        )
