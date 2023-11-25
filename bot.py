import discord
import os
import logging
import subprocess
import uuid
import re
import glob
import shutil
from RedDownloader import RedDownloader
from helper import simple_embed
from discord.ext import commands
from discord import app_commands

logger = logging.getLogger('discord')
logger.name = 'application'


bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.event
async def on_ready():
    logger.info("Bot is Online")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Social Media"))
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

def download_with_args(args: str):
    id = str(uuid.uuid4()) + ".mp4"
    process = subprocess.Popen(f"youtube-dl -o {id} {args}", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    process.wait()
    return id

async def change_msg(ctx, text: str):
    await ctx.edit_original_response(embed=simple_embed(text))

@bot.tree.command(name="youtube")
async def youtube(ctx, url: str):
    await ctx.response.send_message(embed=simple_embed('Downloading ...'))
    file_id = download_with_args(f"-f 'best[ext=mp4]' {url}")
    await change_msg(ctx, "Sending ...")
    file = discord.File(file_id)
    channel = bot.get_channel(ctx.channel.id)
    await channel.send(file=file)
    await change_msg(ctx, "Done")
    os.remove(file_id)

def datei_existiert(name):
    erweiterungen = ['.mp4', '.jpeg', '.mpeg', '.jpg', '.png', '.gif', '.webm', '.mp3', '.wav']

    for erweiterung in erweiterungen:
        dateipfad = f"{name}{erweiterung}"
        if os.path.exists(dateipfad):
            return f"{name}{erweiterung}"  

@bot.tree.command(name="reddit")
async def reddit(ctx, url: str):
    await ctx.response.send_message(embed=simple_embed('Downloading ...'))
    id = str(uuid.uuid4())
    RedDownloader.Download(url=url, output=id)
    file_id = datei_existiert(id)
    await change_msg(ctx, "Sending ...")
    file = discord.File(file_id)
    channel = bot.get_channel(ctx.channel.id)
    await channel.send(file=file)
    await change_msg(ctx, "Done")
    os.remove(file_id)

def extract_shortcode(url):
    instagram_url_pattern = re.compile(r'(https?://www\.instagram\.com/(?:reel|p)/([^/?]+))')
    match = instagram_url_pattern.match(url)
    if match:
        shortcode = match.group(2)
        return shortcode
    else:
        return None
    
def find_media_files(directory):
    media_files = []
    extensions = ['.mp4', '.jpeg', '.mpeg', '.jpg', '.png', '.gif', '.webm', '.mp3', '.wav']
    for extension in extensions:
        files_with_extension = glob.glob(os.path.join(directory, f"*{extension}"))
        if extension == '.mp4':
            media_files.extend(files_with_extension)
        else:
            if any(file.endswith('.mp4') for file in files_with_extension):
                media_files.extend(files_with_extension)
    return media_files
    
@bot.tree.command(name="instagram")
async def instagram(ctx, url: str):
    await ctx.response.send_message(embed=simple_embed('Downloading ...'))
    shortcode = extract_shortcode(url)
    if shortcode == None:
        await change_msg(ctx, "URL Invalid")
        return

    process = subprocess.Popen(f"instaloader -- -{shortcode}", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    process.wait()

    await change_msg(ctx, "Sending ...")
    files = find_media_files(f"./-{shortcode}")
    for file_id in files:
        file = discord.File(file_id)
        channel = bot.get_channel(ctx.channel.id)
        await channel.send(file=file)
    await change_msg(ctx, "Done")
    shutil.rmtree(f"-{shortcode}")


@bot.tree.command(name="info")
async def info(ctx):
    await ctx.response.send_message("https://github.com/Katze719/Youtube-dlBot")

bot.run(str(os.getenv('Token')))
