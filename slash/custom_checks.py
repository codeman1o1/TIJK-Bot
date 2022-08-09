# type: ignore[arg-type]

from nextcord import ApplicationError, Guild, Interaction, Member
from nextcord.ext.application_checks import check
from nextcord.utils import get


class CustomCheckError(ApplicationError):
    def __init__(self, message: str):
        self.message = message


async def check_bot_owner(interaction: Interaction) -> bool:
    app_info = await interaction.client.application_info()
    return app_info.owner == interaction.user


def check_server_owner(interaction: Interaction) -> bool:
    return interaction.guild.owner == interaction.user


def has_role(interaction: Interaction, role: str) -> bool:
    return (
        get(interaction.guild.roles, name=role) in interaction.user.roles
        if get(interaction.guild.roles, name=role)
        else False
    )


def has_role_or_above(user: Member, guild: Guild, role: str) -> bool:
    role = get(guild.roles, name=role)
    if role is None:
        return False

    guild_roles = guild.roles
    guild_roles.reverse()
    for guild_role in guild_roles:
        if guild_role.position < role.position:
            break
        if guild_role in user.roles:
            return True
    return False


def is_bot_owner():
    async def predicate(interaction: Interaction) -> bool:
        if await check_bot_owner(interaction):
            return True

        raise CustomCheckError(
            f"You are not the owner of {interaction.client.user.name}!"
        )

    return check(predicate)


def is_server_owner():
    async def predicate(interaction: Interaction) -> bool:
        app_info = await interaction.client.application_info()
        if app_info.owner == interaction.user or check_server_owner(interaction):
            return True

        raise CustomCheckError("You are not the owner of this server!")

    return check(predicate)


def is_owner():
    async def predicate(interaction: Interaction) -> bool:
        if (
            await check_bot_owner(interaction)
            or check_server_owner(interaction)
            or has_role_or_above(interaction.user, interaction.guild, "Owner")
        ):
            return True

        raise CustomCheckError("You are not an owner!")

    return check(predicate)


def is_admin():
    async def predicate(interaction: Interaction) -> bool:
        if (
            await check_bot_owner(interaction)
            or check_server_owner(interaction)
            or has_role_or_above(interaction.user, interaction.guild, "Admin")
        ):
            return True

        raise CustomCheckError("You are not an admin!")

    return check(predicate)


def is_mod():
    async def predicate(interaction: Interaction) -> bool:
        if (
            await check_bot_owner(interaction)
            or check_server_owner(interaction)
            or has_role_or_above(interaction.user, interaction.guild, "Moderator")
        ):
            return True

        raise CustomCheckError("You are not a moderator!")

    return check(predicate)
