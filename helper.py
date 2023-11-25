import discord

EMBED_COLOR=0xE8652D

def simple_embed(title, text=''):
    embed = discord.Embed(title=title,description=text, color=EMBED_COLOR)
    return embed
