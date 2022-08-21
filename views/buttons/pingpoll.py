import nextcord
from nextcord import Button, ButtonStyle, Embed, Interaction


class PingPoll(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=900)

    async def update(self, interaction: Interaction, embed: Embed, button_index: int):
        user = interaction.user

        for index, field in enumerate(embed.to_dict()["fields"]):
            name = field["name"]
            value = field["value"]

            if value == "Nobody":
                value = ""

            if f"<@{user.id}>" in value:
                mention = f"<@{user.id}>"
            elif f"<@!{user.id}>" in value:
                mention = f"<@!{user.id}>"
            else:
                mention = None

            if mention:
                value = value.replace(f"{mention}", "").replace("\n\n", "\n")
            elif index == button_index:
                value = value + "\n" + user.mention

            if value == "":
                value = "Nobody"

            embed.set_field_at(index, name=name, value=value)

        await interaction.message.edit(embed=embed)

    @nextcord.ui.button(label="Accept", style=ButtonStyle.green)
    async def accept(self, button: Button, interaction: Interaction):
        embed = interaction.message.embeds[0]
        await self.update(interaction, embed, 0)

    @nextcord.ui.button(label="In a moment", style=ButtonStyle.blurple)
    async def in_a_moment(self, button: Button, interaction: Interaction):
        embed = interaction.message.embeds[0]
        await self.update(interaction, embed, 1)

    @nextcord.ui.button(label="Deny", style=ButtonStyle.red)
    async def deny(self, button: Button, interaction: Interaction):
        embed = interaction.message.embeds[0]
        await self.update(interaction, embed, 2)
