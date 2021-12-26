import nextcord
from nextcord import ButtonStyle
from dotenv import load_dotenv
from pymongo import MongoClient
import os

load_dotenv(os.path.join(os.getcwd() + "\.env"))

MongoPassword = os.environ["MongoPassword"]
MongoUsername = os.environ["MongoUsername"]
MongoWebsite = os.environ["MongoWebsite"]
cluster = MongoClient(f"mongodb+srv://{MongoUsername}:{MongoPassword}@{MongoWebsite}")
Data = cluster["Data"]
UserData = Data["UserData"]
BotData = Data["BotData"]


class RoleView(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

        for objects in BotData.find():
            for role in objects["roles"]:
                self.add_item(
                    AddButton(label=role, style=ButtonStyle.primary, custom_id=role)
                )

    async def handle_click(
        self, button: nextcord.ui.Button, interaction: nextcord.Interaction
    ):
        role = nextcord.utils.get(interaction.guild.roles, name=button.label)

        if not role in interaction.user.roles:
            try:
                await interaction.user.add_roles(role)
                await interaction.response.send_message(
                    f'The "{button.label}" role has successfully been added!',
                    ephemeral=True,
                )
            except AttributeError:
                await interaction.response.send_message(
                    f'The "{button.label}" role is not found\nPlease contact an admin to fix this',
                    ephemeral=True,
                )

        elif role in interaction.user.roles:
            try:
                await interaction.user.remove_roles(role)
                await interaction.response.send_message(
                    f'The "{button.label}" role has successfully been removed!',
                    ephemeral=True,
                )
            except AttributeError:
                await interaction.response.send_message(
                    f'The "{button.label}" role is not found\nPlease contact an admin to fix this',
                    ephemeral=True,
                )


class AddButton(nextcord.ui.Button):
    async def callback(self, interaction: nextcord.Interaction):
        await self.view.handle_click(self, interaction)
