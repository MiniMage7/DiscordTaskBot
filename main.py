import discord
from discord.ext import commands
import os
import sqlite3
from sqlite3 import Error

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix='$', intents=intents)

###########
# Classes #
###########

class User:
    def __init__(self, user_id):
        self.user_id = user_id
        self.points = 0
        self.task_list = []

    def add_task(self, task):
        self.task_list.append(task)

    def remove_task(self, task_message_id):
        for task in self.task_list:
            if task.message_id == task_message_id:
                self.task_list.remove(task)
                return


class Task:
    def __init__(self, message_id, task_name, task_type, points_on_complete, points_on_fail):
        self.message_id = message_id
        self.task_name = task_name
        self.task_type = task_type
        self.points_on_complete = points_on_complete
        self.points_on_fail = points_on_fail


###################
# Other Functions #
###################

def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection


#################
# Bot Functions #
#################

@bot.check
async def is_admin(ctx):
    return ctx.author.guild_permissions.administrator or await bot.is_owner(ctx.author)


@bot.command()
@commands.check(is_admin)
async def create_new_task_list(ctx, *args):
    # Delete the message that called this function
    await ctx.message.delete()

    if len(args) != 1:
        await ctx.send("create_new_task_list requires only a user_id\nExample: $create_new_task_list 1234567890")
        return

    # Get the user from the user_id
    user = bot.get_user(int(args[0]))
    if user is None:
        await ctx.send("Invalid user_id")
        return

    # Create the embedded message
    embed_var = discord.Embed(title=user.display_name + "'s Tasks",
                              description="React with \U0001F6CF to end the day\n\n" +
                              "React with \U00002705 to add a new task")

    # Send the embedded message
    embedded_message = await ctx.channel.send(embed=embed_var)

    # Add the bed and check mark emojis
    await embedded_message.add_reaction('\U0001F6CF')
    await embedded_message.add_reaction('\U00002705')


@bot.event
async def on_raw_reaction_add(ctx):
    pass


@bot.event
async def on_ready():
    # Connect to database on bot start up
    db = create_connection("DTBPRD.db")
    # Make database tables if the dont exist yet
    db.execute('''CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, points INTEGER, task_list TEXT)''')
    db.execute('''CREATE TABLE IF NOT EXISTS tasks (message_id INTEGER PRIMARY KEY, task_name TEXT, task_type TEXT, points_on_complete INTEGER, points_on_fail INTEGER)''')


bot.run(os.environ['TOKEN'])