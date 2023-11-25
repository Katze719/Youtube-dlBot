import discord
import os
import logging
from helper import simple_embed
from discord.ext import commands
from discord import app_commands

logger = logging.getLogger('discord')
logger.name = 'application'


bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.event
async def on_ready():
    logger.info("Bot is Online")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="getting DRUNK!!!"))
    try:
        synced = await bot.tree.sync()
        logger.info(f"Synced {len(synced)} command(s)")
    except Exception as e:
        logger.exception(e)

@bot.tree.command(name="ping")
async def ping(ctx):
    """
    Pings the bot and send a response with the time needed in ms

    Usage:
    !ping
    """
    await ctx.response.send_message(embed=simple_embed(f"Pong! {round(bot.latency * 1000)}ms"))


@bot.tree.command(name="info")
async def info(ctx):
    await ctx.response.send_message("https://github.com/Katze719/CaptainDrunk")

bot.run(str(os.getenv('Token')))




import subprocess

def download_from_yt(url: str):
    process = subprocess.Popen(f"youtube-dl -f 'best[ext=mp4]' {url}", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    process.wait()

download_from_yt("https://www.youtube.com/watch?v=yHgx0DyzFcE")
