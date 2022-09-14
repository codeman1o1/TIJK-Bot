import datetime

import nextcord

from utils.check_message_sender import CheckMessageSender as CMS
from views.buttons.pingpoll import PingPoll


class PingPollTime(nextcord.ui.Select, CMS):
    def __init__(self):
        options = [
            nextcord.SelectOption(label=f"{i} minutes", value=str(i * 60))
            for i in range(5, 30 + 1, 5)
        ]

        super().__init__(
            placeholder="Please select a time",
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, interaction: nextcord.Interaction):
        time = int(self.values[0])
        time_dt = nextcord.utils.utcnow() + datetime.timedelta(seconds=time)
        await interaction.response.edit_message(
            delete_after=time, view=PingPoll(time_dt)
        )


class PingPollTimeView(nextcord.ui.View):
    def __init__(self, sender_id: int):
        super().__init__()
        CMS.__init__(self, sender_id)
        self.add_item(PingPollTime())
