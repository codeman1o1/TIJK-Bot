import nextcord
from nextcord import ButtonStyle


class VerifyView(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(
            AddButton(
                label="Verify",
                style=ButtonStyle.primary,
                custom_id="verify",
            )
        )

    async def handle_click(
        self, button: nextcord.Button, interaction: nextcord.Interaction
    ):
        member_role = nextcord.utils.get(interaction.guild.roles, name="Member")
        if member_role not in interaction.user.roles:
            await interaction.user.add_roles(member_role, reason="Verified user")
            await interaction.response.send_message("You have been verfied!", ephemeral=True)
        else:
            await interaction.response.send_message("You are already verfied", ephemeral=True)


class AddButton(nextcord.ui.Button):
    async def callback(self, interaction: nextcord.Interaction):
        await self.view.handle_click(self, interaction)
