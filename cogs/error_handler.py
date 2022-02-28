import nextcord
from nextcord.ext import commands
from nextcord.ext.commands import Context
from nextcord.ext.commands.errors import *
from difflib import SequenceMatcher
import basic_logger as bl
from views.report_issue import report_issue
from urllib.parse import quote


class error_handler(commands.Cog, name="Error Handler"):
    """A cog for customized error messages"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx: Context, error: commands.CommandError):
        """Called when a command error occurs"""

        if isinstance(error, CommandNotFound):
            message = ctx.message.content.split(".", 1)[1]
            while message.startswith(" "):
                message = message.split(" ", 1)[1]
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
            if best_cmd_perc >= 60:
                embed = nextcord.Embed(
                    color=0xFF0000,
                    title=f"That is not a command!\nDid you mean `.{best_cmd}{best_cmd_2}`? ({best_cmd_perc}% match)",
                )
            else:
                embed = nextcord.Embed(
                    color=0xFF0000,
                    title="That is not a command!\nI did not find any close matching commands",
                )

        elif isinstance(error, CommandOnCooldown):
            COOLDOWN = str(round(error.retry_after, 1)).replace(".", ",")
            embed = nextcord.Embed(
                color=0xFF0000,
                title=f"This command is on cooldown!\nPlease retry after {COOLDOWN} seconds",
            )

        elif isinstance(error, GuildNotFound):
            embed = nextcord.Embed(
                color=0xFF0000,
                title=f'"{error.argument}" is not a guild or I can\'t access it!',
            )

        elif isinstance(error, GuildStickerNotFound):
            embed = nextcord.Embed(
                color=0xFF0000,
                title=f'"{error.argument}" is not a Guild Sticker or I can\'t access it!',
            )

        elif isinstance(error, MemberNotFound):
            embed = nextcord.Embed(
                color=0xFF0000,
                title=f'"{error.argument}" is not a user or I can\'t access it!',
            )

        elif isinstance(error, RoleNotFound):
            embed = nextcord.Embed(
                color=0xFF0000,
                title=f'"{error.argument}" is not a role or I can\'t access it!',
            )

        elif isinstance(error, ChannelNotFound):
            embed = nextcord.Embed(
                color=0xFF0000,
                title=f'"{error.argument}" is not a channel or I can\'t access it!',
            )

        elif isinstance(error, ChannelNotReadable):
            embed = nextcord.Embed(
                color=0xFF0000,
                title=f'I can\'t read messages in the "{error.argument}" channel',
            )

        elif isinstance(error, MessageNotFound):
            embed = nextcord.Embed(
                color=0xFF0000,
                title=f'"{error.argument}" is not a message or I can\'t access it!',
            )

        elif isinstance(error, MissingRequiredArgument):
            embed = nextcord.Embed(
                color=0xFF0000,
                title=f'"{error.param.name}" is a required argument that is missing!',
            )

        elif isinstance(error, MissingAnyRole):
            if error.missing_roles == ["Owner", "Admin", "TIJK-Bot developer"]:
                embed = nextcord.Embed(
                    color=0xFF0000, title="You must be an admin to do this!"
                )

            else:
                missing_roles = ", ".join(error.missing_roles)
                embed = nextcord.Embed(
                    color=0xFF0000,
                    title=f"You are missing any of the following roles: {missing_roles}",
                )

        elif isinstance(error, MissingRole):
            embed = nextcord.Embed(
                color=0xFF0000,
                title=f"You are missing the following role: {error.missing_role}",
            )

        elif isinstance(error, NotOwner):
            OWNER = self.bot.get_user(self.bot.owner_id)
            embed = nextcord.Embed(
                color=0xFF0000,
                title=f"Only the owner of TIJK Bot ({OWNER}) can do this!",
            )

        elif isinstance(error, BotMissingPermissions):
            missing_permissions = ", ".join(error.missing_permissions)
            embed = nextcord.Embed(
                color=0xFF0000,
                title=f"I am missing the following permission(s): {missing_permissions}",
            )

        elif isinstance(error, BotMissingAnyRole):
            MISSING_ROLES = ", ".join(error.missing_roles)
            embed = nextcord.Embed(
                color=0xFF0000,
                title=f"I am missing any of the following role(s): {MISSING_ROLES}",
            )

        elif isinstance(error, BotMissingRole):
            embed = nextcord.Embed(
                color=0xFF0000,
                title=f"I am missing the following role: {error.missing_role}",
            )

        else:
            embed = nextcord.Embed(color=0xFF0000, title=f"An unkown error occurred!")
            embed.add_field(
                name="Error:",
                value=error,
                inline=True,
            )
            embed.set_footer(text="Click the button below to report this error")
            await ctx.send(embed=embed, view=report_issue(quote(str(error))))
            bl.error(error, __file__)
            return

        await ctx.send(embed=embed)
        bl.error(error, __file__)


def setup(bot: commands.Bot):
    bot.add_cog(error_handler(bot))
