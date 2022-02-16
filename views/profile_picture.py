import nextcord
from nextcord import ButtonStyle


class profile_picture(nextcord.ui.View):
    def __init__(self, url: str):
        super().__init__(timeout=None)
        self.add_item(
            nextcord.ui.Button(
                label="Download profile picture",
                url=url,
                style=ButtonStyle.url,
            )
        )
