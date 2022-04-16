import nextcord
from nextcord import ButtonStyle

from main import logger


class ChangeNameBack(nextcord.ui.View):
    def __init__(self, user: nextcord.Member, name: str):
        super().__init__(timeout=None)
        self.user = user
        self.name = name

    @nextcord.ui.button(
        label="Change name back",
        style=ButtonStyle.blurple,
        custom_id="change_name_back",
    )
    async def change_name_back(
        self, button: nextcord.Button, interaction: nextcord.Interaction
    ):
        owner_role = nextcord.utils.get(interaction.user.guild.roles, name="Owner")
        admin_role = nextcord.utils.get(interaction.user.guild.roles, name="Admin")
        tijk_bot_developer_role = nextcord.utils.get(
            interaction.user.guild.roles, name="TIJK-Bot Developer"
        )
        roles = (owner_role, admin_role, tijk_bot_developer_role)
        if any(role in interaction.user.roles for role in roles):
            ORIGINAL_NAME = self.user.display_name
            await self.user.edit(nick=self.name)
            embed = nextcord.Embed(
                color=0x0DD91A,
                title=f"Successfully changed the name back to {self.name}!",
            )
            await interaction.response.send_message(embed=embed)
            await logger(
                interaction,
                f"{ORIGINAL_NAME}'s nickname has been changed to {self.name}",
            )
        else:
            embed = nextcord.Embed(
                color=0xFF0000, title="You must be an admin to do this!"
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
