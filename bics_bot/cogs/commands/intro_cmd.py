import nextcord
import sys

from nextcord.ext import commands
from nextcord import application_command

sys.path.append("../../../")
from server_ids import *


class IntroCmd(commands.Cog):
    def __init__(self, client):
        self.client = client

    @application_command.slash_command(
        guild_ids=[BICS_GUILD_ID, BICS_CLONE_GUILD_ID], description="Introduce yourself"
    )
    async def intro(
        self,
        interaction: nextcord.Interaction,
        name: str = nextcord.SlashOption(description="Name", required=True),
        surname: str = nextcord.SlashOption(description="Surname", required=True),
        year: str = nextcord.SlashOption(
            description="The year you will be in. In case you plan on comming to the uni, choose **incoming**",
            choices=["year-1", "year-2", "year-3", "alumni", "erasmus", "incoming"],
        ),
    ):
        if interaction.channel_id == INTRO_CHANNEL_ID:
            user = interaction.user
            user_roles = user.roles

            if len(user_roles) > 1:
                # - Means the user already has at least one role
                await interaction.response.send_message(
                    f"You have already introduced yourself! In case you have a role that you think should be changed feel free to ping an <@&{ADMIN_ROLE_ID}>",
                    ephemeral=True,
                )
            else:
                # - Getting the roles
                year1_role = nextcord.utils.get(interaction.guild.roles, name="Year 1")
                year2_role = nextcord.utils.get(interaction.guild.roles, name="Year 2")
                year3_role = nextcord.utils.get(interaction.guild.roles, name="Year 3")
                erasmus_role = nextcord.utils.get(
                    interaction.guild.roles, name="Erasmus"
                )
                alumni_role = nextcord.utils.get(interaction.guild.roles, name="Alumni")
                incoming_role = nextcord.utils.get(
                    interaction.guild.roles, name="Incoming"
                )

                if year == "year-1":
                    await user.add_roles(year1_role)
                elif year == "year-2":
                    await user.add_roles(year2_role)
                elif year == "year-3":
                    await user.add_roles(year3_role)
                elif year == "alumni":
                    await user.add_roles(alumni_role)
                elif year == "incomming":
                    await user.add_roles(incoming_role)
                else:
                    await user.add_roles(erasmus_role)

                # - Changing the nickname to Name + Surname initial
                await user.edit(nick=f"{name.capitalize()} {surname[0].upper()}")
                await user.send(
                    f"`Welcome on board {name.capitalize()} {surname.capitalize()}! Your role has been updated and you are all set 😉. In case of any question, feel free to ping an @Admin`"
                )
        else:
            # - Trying to type the command outside the right channel
            await interaction.response.send_message(
                f"Oops something went wrong! Make sure you are on <#{INTRO_CHANNEL_ID}> to send the **/intro** command",
                ephemeral=True,
            )


def setup(client):
    client.add_cog(IntroCmd(client))