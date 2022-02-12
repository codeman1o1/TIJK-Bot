import datetime
from difflib import SequenceMatcher

import basic_logger as bl
import nextcord
from nextcord.ext import commands
from views.pings import ping_buttons
from nextcord.ext.commands import Context

from main import logger
from main import BOT_DATA, USER_DATA


class event_handler(commands.Cog, name="Event Handler"):
    """A seperate cog for handling events"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.bot.add_view(ping_buttons())

    @commands.Cog.listener()
    async def on_message(self, message: nextcord.Message):
        """Processes messages"""
        user = message.author

        if user is not None and not message.flags.is_crossposted:
            if not user.bot:
                if "pingpolls" in BOT_DATA.find_one():
                    pingpolls = BOT_DATA.find_one()["pingpolls"]
                    for pingpoll in pingpolls:
                        role = nextcord.utils.get(user.guild.roles, id=pingpoll)
                        if role and message.content == f"<@&{role.id}>":
                            embed = nextcord.Embed(
                                color=0x0DD91A,
                                title=f"{user.display_name} has {role.name}ed",
                            )
                            embed.add_field(name="Accepted", value="None")
                            embed.add_field(name="In a moment", value="None")
                            embed.add_field(name="Denied", value="None")
                            await message.channel.send(
                                embed=embed,
                                delete_after=900,
                                view=ping_buttons(),
                            )

                owner_role = nextcord.utils.get(user.guild.roles, name="Owner")
                admin_role = nextcord.utils.get(user.guild.roles, name="Admin")
                tijk_bot_developer_role = nextcord.utils.get(
                    user.guild.roles, name="TIJK-Bot developer"
                )
                anti_mute = (owner_role, admin_role, tijk_bot_developer_role)
                if all(role not in user.roles for role in anti_mute):
                    with open("spam_detect.txt", "r+") as file:
                        file.writelines(f"{user.id}\n")
                        counter = sum(
                            lines.strip("\n") == str(user.id) for lines in file
                        )
                    if counter > 3:
                        await user.edit(
                            timeout=nextcord.utils.utcnow()
                            + datetime.timedelta(seconds=600)
                        )
                        embed = nextcord.Embed(color=0x0DD91A)
                        embed.add_field(
                            name=f"You ({user.display_name}) have been muted",
                            value="You have been muted for 10 minutes.\nIf you think this was a mistake, please contact an owner or admin",
                            inline=True,
                        )
                        await message.channel.send(embed=embed)
                        await logger(
                            await self.bot.get_context(message),
                            f"{user} has been muted for 10 minutes for spam",
                        )

                if not message.content.startswith(".."):
                    await self.bot.process_commands(message)

            query = {"_id": user.id}
            if USER_DATA.count_documents(query) == 0:
                post = {"_id": user.id, "messages": 1}
                USER_DATA.insert_one(post)
            else:
                user2 = USER_DATA.find_one(query)
                messages = user2["messages"]
                messages = messages + 1
                USER_DATA.update_one(query, {"$set": {"messages": messages}})

    @commands.Cog.listener()
    async def on_member_join(self, member: nextcord.Member):
        """Called when a member joins the server"""
        try:
            if member.bot:
                embed = nextcord.Embed(
                    color=0x0DD91A,
                    title=f"Hey {member.display_name} :wave:\nWe hope you add great functionality to {member.guild.name}!",
                )
            else:
                embed = nextcord.Embed(
                    color=0x0DD91A,
                    title=f"Hey {member.display_name} :wave:\nWelcome to {member.guild.name}!\nWe hope you enjoy your stay!",
                )
            if member.guild.system_channel:
                await member.guild.system_channel.send(embed=embed)
            dm = await member.create_dm()
            await dm.send(embed=embed)
        except nextcord.errors.HTTPException:
            pass
        if member.bot:
            bot_role = nextcord.utils.get(member.guild.roles, name="Bot")
            await member.add_roles(bot_role)

    @commands.Cog.listener()
    async def on_member_update(self, before: Context, after: Context):
        """Called when a member updates"""
        tijk_bot_developer_role = nextcord.utils.get(
            after.guild.roles, name="TIJK-Bot developer"
        )
        if tijk_bot_developer_role in after.roles:
            info = await self.bot.application_info()
            owner = info.owner
            if after.id != owner.id:
                await after.remove_roles(tijk_bot_developer_role)
        if after.nick:
            owner_role = nextcord.utils.get(after.guild.roles, name="Owner")
            admin_role = nextcord.utils.get(after.guild.roles, name="Admin")
            roles = (owner_role, admin_role)
            admin_names = [
                [user.name, user.display_name]
                for user in after.guild.members
                if any(role in user.roles for role in roles)
            ]
            admin_names = tuple(sum(admin_names, []))
            admin_roles = (owner_role, admin_role)
            if (
                all(admin_role not in after.roles for admin_role in admin_roles)
                and after.nick in admin_names
            ):
                try:
                    user = self.bot.get_user(int(after.id))
                    if before.nick:
                        await after.edit(nick=before.nick)
                    else:
                        await after.edit(nick=before.name)
                    query = {"_id": after.id}
                    if USER_DATA.count_documents(query) == 0:
                        post = {"_id": after.id, "warns": 1}
                        USER_DATA.insert_one(post)
                    else:
                        user = USER_DATA.find_one(query)
                        warns = user["warns"] if "warns" in user else 0
                        warns = warns + 1
                        USER_DATA.update_one(
                            {"_id": after.id}, {"$set": {"warns": warns}}
                        )
                except nextcord.Forbidden:
                    bl.error("Couldn't change nickname", __file__)

    @commands.Cog.listener()
    async def on_member_remove(self, member: nextcord.Member):
        """Called when a member has been removed from the server"""
        try:
            embed = nextcord.Embed(
                color=0x0DD91A,
                title=f"Bye {member.display_name} :wave:\nIt was great having you!!",
            )
            if member.guild.system_channel:
                await member.guild.system_channel.send(embed=embed)
            dm = await member.create_dm()
            await dm.send(embed=embed)
        except nextcord.errors.HTTPException:
            pass

    @commands.Cog.listener()
    async def on_command_error(self, ctx: Context, error: commands.CommandError):
        """Called when a command error occurs"""
        if isinstance(error, commands.CommandNotFound):
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
        embed.add_field(name="An error occured!", value=error, inline=True)
        await ctx.send(embed=embed)
        bl.error(error, __file__)


def setup(bot: commands.Bot):
    bot.add_cog(event_handler(bot))
