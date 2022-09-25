import datetime
from typing import List

import nextcord


def verify_options(
    options: List[nextcord.SelectOption],
    del_after: datetime.datetime,
) -> List[str]:
    """
    Verifies that the given options are still available

    Parameters
    ----------
    options : List[nextcord.SelectOption]
        The options to verify
    del_after : datetime.datetime
        When the PingPoll will be deleted

    Returns
    -------
    List[str]
        The options that are still available
    """
    new_options: List[str] = []
    for option in options:
        new_options.append(option.value)

        if option.value == "remove":
            continue

        new_date = nextcord.utils.utcnow() + datetime.timedelta(
            seconds=int(option.value)
        )
        if del_after <= new_date:
            new_options.remove(option.value)

    return new_options


class InAMoment(nextcord.ui.Select):
    def __init__(self, message: nextcord.Message, del_after: datetime.datetime):
        self.message = message
        self.del_after = del_after
        self.minutes_left: int = (del_after - nextcord.utils.utcnow()).seconds // 60

        options = [
            nextcord.SelectOption(label=f"{i} minutes", value=str(i * 60))
            for i in range(5, self.minutes_left + 1, 5)
        ]
        options.append(nextcord.SelectOption(label="Remove", value="remove", emoji="❌"))

        super().__init__(
            placeholder="Please select a time",
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, interaction: nextcord.Interaction):
        selected: str = self.values[0]
        if selected not in verify_options(self.options, self.del_after):
            await interaction.response.send_message(
                "You have selected an option that is no longer available",
                ephemeral=True,
            )
            return

        from views.buttons.pingpoll import (  # pylint: disable=import-outside-toplevel
            PingPoll,
        )

        if selected == "remove":
            await PingPoll.update(
                self,
                interaction.user,
                self.message,
                1,
                remove_only=True,
                fields=("In a moment",),
            )
            return

        choice = int(selected)

        new_datetime = int(
            (nextcord.utils.utcnow() + datetime.timedelta(seconds=choice)).timestamp()
        )

        await PingPoll.update(
            self,
            interaction.user,
            self.message,
            1,
            custom_message=f"<t:{new_datetime}:R>",
            replace_mode=True,
        )


class InAMomentView(nextcord.ui.View):
    def __init__(self, message: nextcord.Message, del_after: datetime.datetime):
        date = (del_after - nextcord.utils.utcnow()).seconds
        super().__init__(timeout=date)
        self.add_item(InAMoment(message, del_after))
