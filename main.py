import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix='$', intents=intents)


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
    embed_var = discord.Embed(title=user.display_name + "'s Tasks")

    # Send the embedded message
    embedded_message = await ctx.channel.send(embed=embed_var)


bot.run(os.environ['TOKEN'])