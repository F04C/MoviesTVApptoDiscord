import discord
from discord.ext import commands
import psutil
import os
from config import token
# Set your Discord bot token here


# Initialize the Discord bot with intents
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

# Function to get the currently playing file name
def get_currently_playing():
    # Get the process ID of the "Movies & TV" app
    for process in psutil.process_iter(['pid', 'name']):
        if "Movies & TV" in process.info['name']:
            process_id = process.info['pid']
            # Get the list of open files by the process
            open_files = psutil.Process(process_id).open_files()
            print(open_files)
            # Assuming the first open file is the currently playing video
            if open_files:
                file_path = open_files[0].path
                # Extract the file name from the path
                file_name = os.path.basename(file_path)
                return file_name

# Command to display the currently playing file on Discord
@bot.command(name='playing')
async def display_currently_playing(ctx):
    file_name = get_currently_playing()
    if file_name:
        message = f"Currently playing: {file_name}"
        await ctx.send(message)
    else:
        await ctx.send("No file currently playing.")

# Command suggestion feature
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Check for the command prefix
    if message.content.startswith('!'):
        available_commands = [command.name for command in bot.commands]
        suggestions = ', '.join(available_commands)
        await message.channel.send(f"Available commands: {suggestions}")

    await bot.process_commands(message)

# Run the bot
bot.run(token)
