from nextcord import ApplicationError, Interaction
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


def has_role_or_above(interaction: Interaction, role: str) -> bool:
    if not (ROLE := get(interaction.guild.roles, name=role)):
        return False

    guild_roles = interaction.guild.roles.reverse()
    for guild_role in guild_roles:
        if guild_role.position < ROLE.position:
            break
        if guild_role in interaction.user.roles:
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
            or has_role_or_above(interaction, "Owner")
        ):
            return True

        raise CustomCheckError("You are not an owner!")

    return check(predicate)


def is_admin():
    async def predicate(interaction: Interaction) -> bool:
        if (
            await check_bot_owner(interaction)
            or check_server_owner(interaction)
            or has_role_or_above(interaction, "Admin")
        ):
            return True

        raise CustomCheckError("You are not an admin!")

    return check(predicate)


def is_mod():
    async def predicate(interaction: Interaction) -> bool:
        if (
            await check_bot_owner(interaction)
            or check_server_owner(interaction)
            or has_role_or_above(interaction, "Moderator")
        ):
            return True

        raise CustomCheckError("You are not a moderator!")

    return check(predicate)
