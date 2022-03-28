import nextcord
from nextcord import ButtonStyle
from nextcord.ext import commands
from nextcord.utils import get

from main import BOT_DATA


class button_roles(nextcord.ui.View):
    def __init__(self, bot: commands.Bot = None, guild: nextcord.Guild = None):
        super().__init__(timeout=None)
        if guild:
            for buttonrole in BOT_DATA.find_one()["buttonroles"]:
                if get(guild.roles, id=buttonrole):
                    self.add_item(
                        AddButton(
                            label=get(guild.roles, id=buttonrole).name,
                            style=ButtonStyle.primary,
                            custom_id=str(buttonrole),
                        )
                    )
        if bot:
            for guild in bot.guilds:
                for buttonrole in BOT_DATA.find_one()["buttonroles"]:
                    if get(guild.roles, id=buttonrole):
                        self.add_item(
                            AddButton(
                                label=get(guild.roles, id=buttonrole).name,
                                style=ButtonStyle.primary,
                                custom_id=str(buttonrole),
                            )
                        )

    async def handle_click(
        self, button: nextcord.ui.Button, interaction: nextcord.Interaction
    ):
        if role := get(interaction.guild.roles, id=int(button.custom_id)):
            if role not in interaction.user.roles:
                await interaction.user.add_roles(role)
                await interaction.response.send_message(
                    f'The "{role.name}" role has successfully been added!',
                    ephemeral=True,
                )

            else:
                await interaction.user.remove_roles(role)
                await interaction.response.send_message(
                    f'The "{role.name}" role has successfully been removed!',
                    ephemeral=True,
                )
        else:
            await interaction.response.send_message(
                f'The "{role.name}" role is not found\nPlease contact an admin to fix this',
                ephemeral=True,
            )


class AddButton(nextcord.ui.Button):
    async def callback(self, interaction: nextcord.Interaction):
        await self.view.handle_click(self, interaction)
