import os
import sys
import discord
from discord.ext import commands
import configparser

# Set CWD to script directory
os.chdir(os.path.dirname(__file__))

# Get Config
config = configparser.ConfigParser()
config.read('../config/config.ini')

# Settings
INVITELINK = 'https://discordapp.com/oauth2/authorize?&client_id=' + str(config['DEFAULT']['CLIENTID']) + '&scope=bot&permissions=0'
description = """Theme Wars Bot is a Discord bot created by Byte#0017."""

def get_prefix(bot, msg):
    """A callable Prefix for our bot. This could be edited to allow per server prefixes."""
    
    prefixes = [config['DEFAULT']['PREFIX']]
    
    # Check to see if we are outside of a guild. e.g DM's etc.
    if msg.guild is None:
        # Only allow ? to be used in DMs
        return '?'

    # Allow bot mention as prefix.
    return commands.when_mentioned_or(*prefixes)(bot, msg)

# Inital Cog's to load.
initial_extensions = (
    'cogs.themewars',
)

bot = commands.Bot(command_prefix=get_prefix, description=description)

@bot.event
async def on_ready():
    """http://discordpy.readthedocs.io/en/rewrite/api.html#discord.on_ready"""
	
    print(f'\n\nLogged in as: {bot.user.name} - {bot.user.id}\nVersion: {discord.__version__}\n')
    
    # Inital Extention Loading.
    if __name__ == '__main__':
        for extension in initial_extensions:
            try:
                bot.load_extension(extension)
            except Exception as e:
                print(f'Failed to load extension {extension}. ', file=sys.stderr)
                traceback.print_exc() # Uncomment for bug reports.
    print(f'Successfully logged in and connected!')
    
bot.run(config['DEFAULT']['TOKEN'], bot=True, reconnect=True)