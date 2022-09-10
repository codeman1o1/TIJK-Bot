import datetime
from typing import Iterable
import nextcord
from nextcord import Button, ButtonStyle, Interaction

from views.dropdowns.pingpoll_in_a_moment import InAMomentView


class PingPoll(nextcord.ui.View):
    def __init__(self, del_after: datetime.datetime):
        super().__init__(timeout=900)
        self.del_after = del_after

    async def update(
        self,
        user: nextcord.Member,
        message: nextcord.Message,
        button_index: int,
        *,
        custom_message: str = "",
        remove_only: bool = False,
        replace_mode: bool = False,
        fields: Iterable[str] = None,
    ):
        if fields is None:
            fields = ["Accepted", "In a moment", "Denied"]

        if remove_only and replace_mode:
            raise ValueError("remove_only and replace_mode cannot both be True")

        embed = message.embeds[0]
        for index, field in enumerate(embed.to_dict()["fields"]):
            name = field["name"]
            if name not in fields:
                continue
            value = field["value"]
            if value == "Nobody":
                value = ""
            values = value.split("\n")
            values = list(filter(None, values))
            if f"<@{user.id}>" in value:
                mention = f"<@{user.id}>"
            elif f"<@!{user.id}>" in value:
                mention = f"<@!{user.id}>"
            else:
                mention = None
            if mention:
                if replace_mode and name == "In a moment":
                    for v_index, v in enumerate(values):
                        if mention in v:
                            values[v_index] = f"{user.mention} {custom_message}"
                else:
                    for v in values:
                        if mention in v:
                            values.remove(v)
                value = "\n".join(values)
            elif index == button_index and not remove_only:
                value = value + "\n" + user.mention + " " + custom_message
            if value == "":
                value = "Nobody"
            embed.set_field_at(index, name=name, value=value)
        await message.edit(embed=embed)

    @nextcord.ui.button(label="Accept", style=ButtonStyle.green)
    async def accept(self, button: Button, interaction: Interaction):
        await self.update(interaction.user, interaction.message, 0)  # type: ignore[arg-type]

    @nextcord.ui.button(label="In a moment", style=ButtonStyle.blurple)
    async def in_a_moment(self, button: Button, interaction: Interaction):
        minutes_left = (self.del_after - nextcord.utils.utcnow()).seconds // 60
        if minutes_left >= 5:
            await interaction.response.send_message(
                view=InAMomentView(interaction.message, self.del_after), ephemeral=True
            )
        else:
            await self.update(interaction.user, interaction.message, 1)  # type: ignore[arg-type]

    @nextcord.ui.button(label="Deny", style=ButtonStyle.red)
    async def deny(self, button: Button, interaction: Interaction):
        await self.update(interaction.user, interaction.message, 2)  # type: ignore[arg-type]
