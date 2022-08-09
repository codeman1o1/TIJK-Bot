from nextcord import Embed, Interaction


class CheckMessageSender:
    def __init__(self, sender_id: int):
        self.sender_id = sender_id

    async def interaction_check(self, interaction: Interaction) -> bool:
        """Check if the user who clicked the button is the user who sent the message"""
        if self.sender_id == interaction.user.id:
            return True
        embed = Embed(color=0xFF0000, title="You are not allowed to do that!")
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return False
