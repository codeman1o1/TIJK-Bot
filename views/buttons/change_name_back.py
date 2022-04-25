import nextcord
from nextcord import ButtonStyle
from slash.custom_checks import has_role_or_above

from main import log


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
        if has_role_or_above(interaction.user, interaction.guild, "Admin"):
            ORIGINAL_NAME = self.user.display_name
            await self.user.edit(nick=self.name)
            embed = nextcord.Embed(
                color=0x0DD91A,
                title=f"Successfully changed the name back to {self.name}!",
            )
            await interaction.response.send_message(embed=embed)
            await log(
                interaction,
                f"{ORIGINAL_NAME}'s nickname has been changed to {self.name}",
            )
        else:
            embed = nextcord.Embed(
                color=0xFF0000, title="You must be an admin to do this!"
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
