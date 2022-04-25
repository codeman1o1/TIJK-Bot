import nextcord
from nextcord import ButtonStyle


class Link(nextcord.ui.View):
    def __init__(self, link: str, label: str = "Open in browser"):
        super().__init__()
        self.add_item(
            nextcord.ui.Button(
                label=label,
                url=link,
                style=ButtonStyle.url,
            )
        )
