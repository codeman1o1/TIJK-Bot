import datetime
import nextcord
from nextcord.ext import commands
from dotenv import load_dotenv
from pymongo import MongoClient
import json
import basic_logger as bl
import os

load_dotenv(os.path.join(os.getcwd() + "\.env"))

MongoPassword = os.environ["MongoPassword"]
MongoUsername = os.environ["MongoUsername"]
MongoWebsite = os.environ["MongoWebsite"]
cluster = MongoClient(f"mongodb+srv://{MongoUsername}:{MongoPassword}@{MongoWebsite}")
Data = cluster["Data"]
UserData = Data["UserData"]
BotData = Data["BotData"]


class event_handler(
    commands.Cog,
    name="Event Handler",
    description="A seperate cog for handling events",
):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def warn_system(event, user, amount: int = 1):
        query = {"_id": user.id}
        if UserData.count_documents(query) == 0:
            post = {"_id": user.id, "warns": amount}
            UserData.insert_one(post)
            total_warns = amount
        else:
            user2 = UserData.find(query)
            try:
                for result in user2:
                    warns = result["warns"]
            except KeyError:
                pass
            total_warns = warns + amount
            UserData.update_one({"_id": user.id}, {"$set": {"warns": total_warns}})
        embed = nextcord.Embed(color=0x0DD91A)
        if total_warns <= 9:
            embed.add_field(
                name=f"{user.display_name} has been warned by Warn System",
                value=f"{user.display_name} has {10 - total_warns} warns left!",
                inline=False,
            )
            await event.channel.send(embed=embed)
        if total_warns >= 10:
            UserData.update_one({"_id": user.id}, {"$set": {"warns": 0}})
            embed.add_field(
                name=f"{user.display_name} exceeded the warn limit!",
                value=f"He shall be punished with a 10 minute mute!",
                inline=False,
            )
            await event.channel.send(embed=embed)
            await user.edit(
                timeout=nextcord.utils.utcnow() + datetime.timedelta(seconds=600)
            )
            logs_channel = nextcord.utils.get(user.guild.channels, name="logs")
            embed = nextcord.Embed(color=0x0DD91A)
            embed.add_field(
                name=f"User muted!",
                value=f"{user.display_name} was muted for 10 minutes by Warn System",
                inline=False,
            )
            await logs_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        user = message.author

        for k in BotData.find():
            reaction_messages = dict(json.loads(k["reactionmessages"]))
        reaction_messages_keys = list(reaction_messages.keys())
        reaction_messages_values = list(reaction_messages.values())

        if any(
            key.lower() == message.content.lower() for key in reaction_messages_keys
        ):
            index = reaction_messages_keys.index(message.content.lower())
            corresponding_message = reaction_messages_values[index]
            if "{user}" in corresponding_message:
                corresponding_message = corresponding_message.replace(
                    "{user}", user.display_name
                )
            await message.channel.send(corresponding_message)

        if not user.bot:
            with open("spam_detect.txt", "r+") as file:
                file.writelines(f"{user.id}\n")
                counter = sum(lines.strip("\n") == str(user.id) for lines in file)
            if counter > 3:
                owner_role = nextcord.utils.get(user.guild.roles, name="Owner")
                admin_role = nextcord.utils.get(user.guild.roles, name="Admin")
                tijk_bot_developer_role = nextcord.utils.get(
                    user.guild.roles, name="TIJK-Bot developer"
                )
                anti_mute = (owner_role, admin_role, tijk_bot_developer_role)
                if all(role not in user.roles for role in anti_mute):
                    await user.edit(
                        timeout=nextcord.utils.utcnow()
                        + datetime.timedelta(seconds=600)
                    )
                    embed = nextcord.Embed(color=0x0DD91A)
                    embed.add_field(
                        name=f"You ({user.display_name}) have been muted",
                        value=f"You have been muted for 10 minutes.\nIf you think this was a mistake, please contact an owner or admin\nBecause of this action, you received 1 warn",
                        inline=True,
                    )
                    await message.channel.send(embed=embed)
                    await event_handler.warn_system(message, user)

        if user is not None:
            query = {"_id": user.id}
            if UserData.count_documents(query) == 0:
                post = {"_id": user.id, "messages": 1}
                UserData.insert_one(post)
            else:
                for result in UserData.find(query):
                    messages = result["messages"]
                messages = messages + 1
                UserData.update_one(
                    {"_id": message.author.id}, {"$set": {"messages": messages}}
                )

    @commands.Cog.listener()
    async def on_member_join(self, member):
        try:
            user = self.bot.get_user(member.id)
            embed = nextcord.Embed(
                color=0x0DD91A,
                title=f"Hey {member.display_name} :wave:\nWelcome to {member.guild.name}!\nWe hope you enjoy your stay!",
            )
            if member.guild.system_channel:
                await member.guild.system_channel.send(embed=embed)
            dm = await user.create_dm()
            await dm.send(embed=embed)
        except nextcord.errors.HTTPException:
            pass
        if not member.bot:
            member_role = nextcord.utils.get(member.guild.roles, name="Member")
            await member.add_roles(member_role)
        else:
            bot_role = nextcord.utils.get(member.guild.roles, name="Bot")
            await member.add_roles(bot_role)

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        tijk_bot_developer_role = nextcord.utils.get(
            after.guild.roles, name="TIJK-Bot developer"
        )
        if tijk_bot_developer_role in after.roles:
            info = await self.bot.application_info()
            owner = await commands.converter.UserConverter().convert(
                after, str(info.owner)
            )
            if after.id != owner.id:
                await after.remove_roles(tijk_bot_developer_role)
        if after.nick:
            owner_role = nextcord.utils.get(after.guild.roles, name="Owner")
            admin_role = nextcord.utils.get(after.guild.roles, name="Admin")
            roles = (owner_role, admin_role)
            admin_names = [
                [str(user.name), str(user.display_name)]
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
                    if UserData.count_documents(query) == 0:
                        post = {"_id": after.id, "warns": 1}
                        UserData.insert_one(post)
                    else:
                        user = UserData.find(query)
                        warns = 0
                        try:
                            for result in user:
                                warns = result["warns"]
                        except KeyError:
                            pass
                        warns = warns + 1
                        UserData.update_one(
                            {"_id": after.id}, {"$set": {"warns": warns}}
                        )
                except nextcord.Forbidden:
                    bl.error(f"Couldn't change nickname", __file__)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        try:
            user = self.bot.get_user(member.id)
            embed = nextcord.Embed(
                color=0x0DD91A,
                title=f"Bye {member.display_name} :wave:\nIt was great having you!!",
            )
            if member.guild.system_channel:
                await member.guild.system_channel.send(embed=embed)
            dm = await user.create_dm()
            await dm.send(embed=embed)
        except nextcord.errors.HTTPException:
            pass

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        embed = nextcord.Embed(color=0xFF0000)
        embed.add_field(
            name=f"An error occured!",
            value=f"{error}",
            inline=True,
        )
        await ctx.send(embed=embed)
        bl.error(error, __file__)


def setup(bot: commands.Bot):
    bot.add_cog(event_handler(bot))
