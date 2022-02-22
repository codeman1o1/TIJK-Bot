import nextcord
from nextcord.ext import commands
from nextcord.ext.commands import Context
from nextcord.ext.commands.errors import *
from difflib import SequenceMatcher
import basic_logger as bl


class error_handler(commands.Cog, name="Error Handler"):
    """A cog for customized error messages"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx: Context, error: commands.CommandError):
        """Called when a command error occurs"""
        if isinstance(error, CommandNotFound):
            message = ctx.message.content[1:].split(" ")[0]
            cmds = {
                command: round(SequenceMatcher(None, command, message).ratio() * 100, 1)
                for command in self.bot.all_commands.keys()
            }
            sorted_keys = list(sorted(cmds, key=cmds.get))
            sorted_keys.reverse()
            sorted_cmds = {w: cmds[w] for w in sorted_keys}
            best_cmd = list(sorted_cmds.keys())[0]
            best_cmd_2 = ""
            best_cmd_full = self.bot.get_command(best_cmd)
            if best_cmd != best_cmd_full.name and best_cmd_full is not None:
                best_cmd_2 = f" ({best_cmd_full})"
            best_cmd_perc = list(sorted_cmds.values())[0]
            error = (
                str(error)
                + f"\nDid you mean `.{best_cmd}{best_cmd_2}`? ({best_cmd_perc}% match)"
            )
            embed = nextcord.Embed(color=0xFF0000)

        if isinstance(error, MemberNotFound):
            embed = nextcord.Embed(
                color=0xFF0000, title=f'"{error.argument}" is not a valid user!'
            )

        await ctx.send(embed=embed)
        bl.error(error, __file__)


def setup(bot: commands.Bot):
    bot.add_cog(error_handler(bot))
