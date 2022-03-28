import nextcord
from nextcord import ButtonStyle


class report_issue(nextcord.ui.View):
    def __init__(self, issue: str):
        super().__init__(timeout=None)
        self.add_item(
            nextcord.ui.Button(
                label="Report issue",
                url=f"https://github.com/codeman1o1/TIJK-Bot/issues/new?assignees=&labels=bug&template=error.yaml&title=%5BERROR%5D+{issue}",
                style=ButtonStyle.url,
            )
        )
