import nextcord
from nextcord import ButtonStyle
from nextcord.ext.commands import Context
from nextcord.utils import get

from main import BOT_DATA


class RoleView(nextcord.ui.View):
    def __init__(self, ctx: Context = None):
        super().__init__(timeout=None)
        if ctx:
            for role in BOT_DATA.find_one()["roles"]:
                if get(ctx.guild.roles, id=role):
                    self.add_item(
                        AddButton(
                            label=get(ctx.guild.roles, id=role).name,
                            style=ButtonStyle.primary,
                            custom_id=str(role),
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
