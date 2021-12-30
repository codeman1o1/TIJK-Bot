from nextcord.ext import commands
import os
from neuralintents import GenericAssistant


class ai_chat(
    commands.Cog,
    name="AI chat cog",
    description="AI chat cog",
):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.chatbot = GenericAssistant(os.path.join(os.getcwd() + "\intents.json"))
        self.chatbot.train_model()
        self.chatbot.save_model()

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.author.bot and message.channel.name == "ai-chat":
            response = self.chatbot.request(message.content)
            if "{user}" in response:
                response = response.replace("{user}", message.author.display_name)
            await message.channel.send(response)


def setup(bot: commands.Bot):
    bot.add_cog(ai_chat(bot))
