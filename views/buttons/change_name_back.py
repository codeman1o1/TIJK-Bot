import nextcord
from nextcord import ButtonStyle

from main import log
from utils.check_message_sender import CheckMessageSender as CMS


class ChangeNameBack(nextcord.ui.View, CMS):
    def __init__(self, user: nextcord.Member, name: str, sender_id: int):
        super().__init__()
        CMS.__init__(self, sender_id)
        self.user = user
        self.name = name

    @nextcord.ui.button(
        label="Change name back",
        style=ButtonStyle.blurple,
    )
    async def change_name_back(
        self, button: nextcord.ui.Button, interaction: nextcord.Interaction
    ):
        original_name = self.user.display_name
        await self.user.edit(nick=self.name)
        embed = nextcord.Embed(
            color=0x0DD91A,
            title=f"Successfully changed the name back to {self.name}!",
        )
        await interaction.response.send_message(embed=embed)
        await log(
            interaction,
            f"{original_name}'s nickname has been changed to {self.name}",
        )
