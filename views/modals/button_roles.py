import nextcord


class ButtonRolesModal(nextcord.ui.Modal):
    def __init__(self, view):
        super().__init__(
            title="Button Roles", custom_id="button_roles_text_modal", timeout=None
        )
        self.view = view

        self.text = nextcord.ui.TextInput(
            label="Text that will be used as the message",
            placeholder="e.g. Click a button to add/remove that role!",
            required=True,
            style=nextcord.TextInputStyle.paragraph,
            custom_id="button_roles_text_modal:text",
        )
        self.add_item(self.text)

    async def callback(self, interaction: nextcord.Interaction):
        embed = nextcord.Embed(color=0x0DD91A, title="The message has been sent!")
        await interaction.response.send_message(embed=embed, ephemeral=True)
        embed = nextcord.Embed(color=0x0DD91A, title=self.text.value)
        await interaction.channel.send(embed=embed, view=self.view)
