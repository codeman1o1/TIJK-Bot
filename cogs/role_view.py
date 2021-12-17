import nextcord
from nextcord import ButtonStyle


class RoleView(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    async def handle_click(
        self, button: nextcord.ui.Button, interaction: nextcord.Interaction
    ):
        role = nextcord.utils.get(interaction.guild.roles, name=button.label)
        if not role in interaction.user.roles:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(
                f"The {button.label} role has successfully been added!", ephemeral=True
            )
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message(
                f"The {button.label} role has successfully been removed!",
                ephemeral=True,
            )

    @nextcord.ui.button(
        label="Hypixel Ping", style=ButtonStyle.primary, custom_id="hypixel_ping"
    )
    async def hypixel_ping_button(self, button, interaction):
        await self.handle_click(button, interaction)

    @nextcord.ui.button(
        label="Clash Royale Ping",
        style=ButtonStyle.primary,
        custom_id="clash_royale_ping",
    )
    async def hypixel__royale_ping_button(self, button, interaction):
        await self.handle_click(button, interaction)

    @nextcord.ui.button(
        label="Homework Ping",
        style=ButtonStyle.primary,
        custom_id="homework_ping",
    )
    async def homework_ping_button(self, button, interaction):
        await self.handle_click(button, interaction)
