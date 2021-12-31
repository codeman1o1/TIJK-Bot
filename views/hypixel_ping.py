import nextcord
from nextcord import ButtonStyle


class hypixel_ping_buttons(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @nextcord.ui.button(label="Accept", style=ButtonStyle.green, custom_id="accept")
    async def accept(self, button: nextcord.Button, interaction: nextcord.Interaction):
        embed = interaction.message.embeds[0]
        embed_name_0 = embed.to_dict()["fields"][0]["name"]
        embed_value_0 = embed.to_dict()["fields"][0]["value"]
        embed_name_1 = embed.to_dict()["fields"][1]["name"]
        embed_value_1 = embed.to_dict()["fields"][1]["value"]
        embed_name_2 = embed.to_dict()["fields"][2]["name"]
        embed_value_2 = embed.to_dict()["fields"][2]["value"]
        if embed_value_0 == "None":
            if interaction.user.display_name in embed_value_1:
                embed_value_1 = embed_value_1.strip(
                    "\n" + interaction.user.display_name
                )
                if embed_value_1 == "":
                    embed_value_1 = "None"
                embed.set_field_at(1, name=embed_name_1, value=embed_value_1)
            if interaction.user.display_name in embed_value_2:
                embed_value_2 = embed_value_2.strip(
                    "\n" + interaction.user.display_name
                )
                if embed_value_2 == "":
                    embed_value_2 = "None"
                embed.set_field_at(2, name=embed_name_2, value=embed_value_2)
            embed_value_0 = interaction.user.display_name
            embed.set_field_at(0, name=embed_name_0, value=embed_value_0)
            await interaction.message.edit(embed=embed)
        elif interaction.user.display_name not in embed_value_0:
            if interaction.user.display_name in embed_value_1:
                embed_value_1 = embed_value_1.strip(
                    "\n" + interaction.user.display_name
                )
                if embed_value_1 == "":
                    embed_value_1 = "None"
                embed.set_field_at(1, name=embed_name_1, value=embed_value_1)
            if interaction.user.display_name in embed_value_2:
                embed_value_2 = embed_value_2.strip(
                    "\n" + interaction.user.display_name
                )
                if embed_value_2 == "":
                    embed_value_2 = "None"
                embed.set_field_at(2, name=embed_name_2, value=embed_value_2)
            embed_value_0 = embed_value_0 + "\n" + interaction.user.display_name
            embed.set_field_at(0, name=embed_name_0, value=embed_value_0)
            await interaction.message.edit(embed=embed)
        else:
            await interaction.response.send_message(
                f"You are already in the `{embed_name_0}` category!", ephemeral=True
            )

    @nextcord.ui.button(
        label="In a moment", style=ButtonStyle.blurple, custom_id="in_a_moment"
    )
    async def in_a_moment(
        self, button: nextcord.Button, interaction: nextcord.Interaction
    ):
        embed = interaction.message.embeds[0]
        embed_name_0 = embed.to_dict()["fields"][0]["name"]
        embed_value_0 = embed.to_dict()["fields"][0]["value"]
        embed_name_1 = embed.to_dict()["fields"][1]["name"]
        embed_value_1 = embed.to_dict()["fields"][1]["value"]
        embed_name_2 = embed.to_dict()["fields"][2]["name"]
        embed_value_2 = embed.to_dict()["fields"][2]["value"]
        if embed_value_1 == "None":
            if interaction.user.display_name in embed_value_0:
                embed_value_0 = embed_value_0.strip(
                    "\n" + interaction.user.display_name
                )
                if embed_value_0 == "":
                    embed_value_0 = "None"
                embed.set_field_at(0, name=embed_name_0, value=embed_value_0)
            if interaction.user.display_name in embed_value_2:
                embed_value_2 = embed_value_2.strip(
                    "\n" + interaction.user.display_name
                )
                if embed_value_2 == "":
                    embed_value_2 = "None"
                embed.set_field_at(2, name=embed_name_2, value=embed_value_2)
            embed_value_1 = interaction.user.display_name
            embed.set_field_at(1, name=embed_name_1, value=embed_value_1)
            await interaction.message.edit(embed=embed)
        elif interaction.user.display_name not in embed_value_1:
            if interaction.user.display_name in embed_value_0:
                embed_value_0 = embed_value_0.strip(
                    "\n" + interaction.user.display_name
                )
                if embed_value_0 == "":
                    embed_value_0 = "None"
                embed.set_field_at(0, name=embed_name_0, value=embed_value_0)
            if interaction.user.display_name in embed_value_2:
                embed_value_2 = embed_value_2.strip(
                    "\n" + interaction.user.display_name
                )
                if embed_value_2 == "":
                    embed_value_2 = "None"
                embed.set_field_at(2, name=embed_name_2, value=embed_value_2)
            embed_value_1 = embed_value_1 + "\n" + interaction.user.display_name
            embed.set_field_at(1, name=embed_name_1, value=embed_value_1)
            await interaction.message.edit(embed=embed)
        else:
            await interaction.response.send_message(
                f"You are already in the `{embed_name_1}` category!", ephemeral=True
            )

    @nextcord.ui.button(label="Deny", style=ButtonStyle.red, custom_id="deny")
    async def deny(self, button: nextcord.Button, interaction: nextcord.Interaction):
        embed = interaction.message.embeds[0]
        embed_name_0 = embed.to_dict()["fields"][0]["name"]
        embed_value_0 = embed.to_dict()["fields"][0]["value"]
        embed_name_1 = embed.to_dict()["fields"][1]["name"]
        embed_value_1 = embed.to_dict()["fields"][1]["value"]
        embed_name_2 = embed.to_dict()["fields"][2]["name"]
        embed_value_2 = embed.to_dict()["fields"][2]["value"]
        if embed_value_2 == "None":
            if interaction.user.display_name in embed_value_0:
                embed_value_0 = embed_value_0.strip(
                    "\n" + interaction.user.display_name
                )
                if embed_value_0 == "":
                    embed_value_0 = "None"
                embed.set_field_at(0, name=embed_name_0, value=embed_value_0)
            if interaction.user.display_name in embed_value_1:
                embed_value_1 = embed_value_1.strip(
                    "\n" + interaction.user.display_name
                )
                if embed_value_1 == "":
                    embed_value_1 = "None"
                embed.set_field_at(1, name=embed_name_1, value=embed_value_1)
            embed_value_2 = interaction.user.display_name
            embed.set_field_at(2, name=embed_name_2, value=embed_value_2)
            await interaction.message.edit(embed=embed)
        elif interaction.user.display_name not in embed_value_2:
            if interaction.user.display_name in embed_value_0:
                embed_value_0 = embed_value_0.strip(
                    "\n" + interaction.user.display_name
                )
                if embed_value_0 == "":
                    embed_value_0 = "None"
                embed.set_field_at(0, name=embed_name_0, value=embed_value_0)
            if interaction.user.display_name in embed_value_1:
                embed_value_1 = embed_value_1.strip(
                    "\n" + interaction.user.display_name
                )
                if embed_value_1 == "":
                    embed_value_1 = "None"
                embed.set_field_at(1, name=embed_name_1, value=embed_value_1)
            embed_value_2 = embed_value_2 + "\n" + interaction.user.display_name
            embed.set_field_at(2, name=embed_name_2, value=embed_value_2)
            await interaction.message.edit(embed=embed)
        else:
            await interaction.response.send_message(
                f"You are already in the `{embed_name_2}` category!", ephemeral=True
            )
