from typing import Iterable
import nextcord
from nextcord import ButtonStyle
from main import USER_DATA

from slash.custom_checks import is_bot_owner


class DatabaseCheck(nextcord.ui.View):
    def __init__(self, add: Iterable[nextcord.Member], remove: Iterable[int]):
        super().__init__()
        self.add = add
        self.remove = remove
        self.add_item(
            nextcord.ui.Button(
                label="Lookup ID's",
                url="https://discord.id/",
                style=ButtonStyle.blurple,
            )
        )

    @nextcord.ui.button(
        label="Add users to the database",
        style=ButtonStyle.blurple,
    )
    @is_bot_owner()
    async def add_users(
        self, button: nextcord.ui.Button, interaction: nextcord.Interaction
    ):
        for user in self.add:
            USER_DATA.insert_one({"_id": user.id, "messages": 0, "warns": 0})

    @nextcord.ui.button(
        label="Remove users from the database",
        style=ButtonStyle.blurple,
    )
    @is_bot_owner()
    async def remove_users(
        self, button: nextcord.ui.Button, interaction: nextcord.Interaction
    ):
        for user_id in self.remove:
            USER_DATA.delete_one({"_id": user_id})
