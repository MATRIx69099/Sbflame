import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import datetime
import random

# Load token from .env file
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

OWNER_ID = 1416823315460526150  # your ID here

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)
bot.remove_command("help")

# OWNER CHECK
def owner_only():
    async def predicate(ctx):
        return ctx.author.id == OWNER_ID
    return commands.check(predicate)

@bot.event
async def on_ready():
    print(f"\nLogged in as: {bot.user}\nBot running...\n")
    await bot.change_presence(activity=discord.Game("Online ✓"))

# PRESENCE COMMANDS
@bot.command()
@owner_only()
async def streaming(ctx, *, text):
    await bot.change_presence(activity=discord.Streaming(name=text, url="https://twitch.tv/discord"))
    await ctx.reply(f"🎥 Streaming: {text}")

@bot.command()
@owner_only()
async def playing(ctx, *, text):
    await bot.change_presence(activity=discord.Game(name=text))
    await ctx.reply(f"🎮 Playing: {text}")

@bot.command()
@owner_only()
async def listening(ctx, *, text):
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=text))
    await ctx.reply(f"🎧 Listening: {text}")

@bot.command()
@owner_only()
async def watching(ctx, *, text):
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=text))
    await ctx.reply(f"📺 Watching: {text}")

# AFK SYSTEM
afk_users = {}

@bot.command()
@owner_only()
async def afk(ctx, *, reason="AFK"):
    afk_users[ctx.author.id] = reason
    await ctx.reply(f"💤 AFK set: {reason}")

@bot.event
async def on_message(message):
    if message.author.id in afk_users:
        del afk_users[message.author.id]
    await bot.process_commands(message)

# USERINFO
@bot.command()
async def userinfo(ctx, member: discord.Member = None):
    member = member or ctx.author
    embed = discord.Embed(title="User Info", color=0x2f3136, timestamp=datetime.datetime.utcnow())
    embed.set_thumbnail(url=member.avatar.url if member.avatar else None)
    embed.add_field(name="Username", value=member.name)
    embed.add_field(name="ID", value=member.id)
    embed.add_field(name="Joined Server", value=member.joined_at.strftime("%d %b %Y"))
    embed.add_field(name="Account Created", value=member.created_at.strftime("%d %b %Y"))
    await ctx.reply(embed=embed)

# SERVERINFO
@bot.command()
async def serverinfo(ctx):
    guild = ctx.guild
    embed = discord.Embed(title=f"Server Info — {guild.name}", color=0x2f3136)
    embed.set_thumbnail(url=guild.icon.url if guild.icon else None)
    embed.add_field(name="Server ID", value=guild.id)
    embed.add_field(name="Owner", value=guild.owner)
    embed.add_field(name="Members", value=guild.member_count)
    embed.add_field(name="Created On", value=guild.created_at.strftime("%d %b %Y"))
    await ctx.reply(embed=embed)

# FUN COMMANDS
@bot.command()
async def coinflip(ctx):
    await ctx.reply(random.choice(["🪙 Heads!", "🪙 Tails!"]))

@bot.command()
async def joke(ctx):
    jokes = [
        "Why don’t skeletons fight? They have no guts.",
        "I'm reading a book on anti-gravity — it's impossible to put down!",
        "I tried to catch fog yesterday… Mist."
    ]
    await ctx.reply(random.choice(jokes))

# UTILITIES
@bot.command()
async def ping(ctx):
    await ctx.reply(f"Pong! `{round(bot.latency * 1000)} ms`")

@bot.command()
async def say(ctx, *, text):
    await ctx.message.delete()
    await ctx.send(text)

# CLEAR
@bot.command()
@owner_only()
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f"Cleared `{amount}` messages.", delete_after=2)

# RUN
bot.run(TOKEN)
