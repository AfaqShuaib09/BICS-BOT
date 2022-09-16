import os
from dotenv import load_dotenv
import nextcord
from nextcord.ext import commands, application_checks
import log_setup as log
from server_ids import *

# - Embeds
from embeds.welcome_embed import Welcome_embed
from embeds.help_embed import Help_embed

load_dotenv()
log.setup_nextcord_logging()

LOGGER = log.get_bot_logger()


def get_intents():
    # - Loading intents
    intents = nextcord.Intents.default()
    intents.members = True
    intents.message_content = True
    return intents


bot_description = """This is the BOT built to work with the BICS student server.\n 
                     It's purpose is to automate the server in someways such as
                     let a user make a selection of the courses he/she attends, welcoming new members and much more.\n 
                     Currently the bot is under development and it is only serving as a wecoming user."""

bot = commands.Bot(
    command_prefix="!", description=bot_description, intents=get_intents()
)


# - Events


@bot.event
async def on_ready():
    LOGGER.info("The BOT is now active!")
    print("The BOT is now active!")


@bot.event
async def on_member_join(member: nextcord.Member):
    server_name = await bot.fetch_guild(member.guild.id)
    server_name = server_name.name
    LOGGER.info(f"{member} has joined the {server_name} server!")
    LOGGER.info(f"Sending welcoming message to {member}")

    await member.send(embed=Welcome_embed(member.display_name, server_name))


# - Commands
@bot.slash_command(
    guild_ids=[BICS_GUILD_ID, BICS_CLONE_GUILD_ID], description="Show bot commands"
)
async def help(interaction: nextcord.Interaction):
    await interaction.response.send_message(embed=Help_embed(), ephemeral=True)


@bot.slash_command(
    guild_ids=[BICS_GUILD_ID, BICS_CLONE_GUILD_ID], description="Introduce yourself"
)
async def intro(
    interaction: nextcord.Interaction,
    name: str = nextcord.SlashOption(description="Name", required=True),
    surname: str = nextcord.SlashOption(description="Surname", required=True),
    year: str = nextcord.SlashOption(
        description="The year you will be/are in (in case of erasmus/global exchange choose **abroad**)",
        choices=["year-1", "year-2", "year-3", "abroad"],
    ),
):
    if interaction.channel_id == INTRO_CHANNEL_ID:
        user = interaction.user
        user_roles = user.roles

        if len(user_roles) > 1:
            # - Means the user already has at least one role
            await interaction.response.send_message(
                f"You have already introduced yourself!", ephemeral=True
            )
        else:
            # - Getting the roles
            year1_role = interaction.guild.get_role(YEAR1_ROLE_ID)
            year2_role = interaction.guild.get_role(YEAR2_ROLE_ID)
            year3_role = interaction.guild.get_role(YEAR3_ROLE_ID)
            abroad_role = interaction.guild.get_role(ABROAD_ROLE_ID)

            if year == "year-1":
                await user.add_roles(year1_role)
            elif year == "year-2":
                await user.add_roles(year2_role)
            elif year == "year-3":
                await user.add_roles(year3_role)
            else:
                await user.add_roles(abroad_role)

            # - Changing the nickname to Name + Surname initial
            await user.edit(nick=f"{name.capitalize()} {surname[0].upper()}")

            await interaction.response.send_message(
                f"Welcome on board {name} {surname}. Your role has been updated and you are all set 😉. In case of any question, or your name has not correctly been changed, feel free to ping an <@&{ADMIN_ROLE_ID}>",
                ephemeral=True,
            )
    else:
        # - Trying to type the command outside the right channel
        await interaction.response.send_message(
            f"Oops something went wrong! Make sure you are on <#{INTRO_CHANNEL_ID}> to send the **/intro** command",
            ephemeral=True,
        )


bot.run(os.getenv("BOT_TESTER_TOKEN"))
