import discord
from discord.ext import commands
import os
import json

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

DATA_FILE = "channels.json"

def load_channels():
    try:
        with open(DATA_FILE, "r") as f:
            return set(json.load(f))
    except:
        return set()

def save_channels(channels):
    with open(DATA_FILE, "w") as f:
        json.dump(list(channels), f)

CHANNEL_IDS = load_channels()

@bot.event
async def on_ready():
    print(f"Bot đã online: {bot.user}")

@bot.command()
@commands.has_permissions(manage_channels=True)
async def addchannel(ctx):
    CHANNEL_IDS.add(ctx.channel.id)
    save_channels(CHANNEL_IDS)
    await ctx.send("✅ Đã bật auto-xóa cho kênh này.")

@bot.command()
@commands.has_permissions(manage_channels=True)
async def removechannel(ctx):
    CHANNEL_IDS.discard(ctx.channel.id)
    save_channels(CHANNEL_IDS)
    await ctx.send("✅ Đã tắt auto-xóa cho kênh này.")

@bot.command()
@commands.has_permissions(manage_channels=True)
async def listchannels(ctx):
    if not CHANNEL_IDS:
        await ctx.send("📋 Chưa có kênh nào được quản lý.")
        return

    channels = []
    for channel_id in CHANNEL_IDS:
        channel = bot.get_channel(channel_id)
        if channel:
            channels.append(channel.mention)

    await ctx.send("📋 Kênh đang auto-xóa:\n" + "\n".join(channels))

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if message.channel.id in CHANNEL_IDS:
        has_link = (
            "http://" in message.content
            or "https://" in message.content
        )

        has_attachment = len(message.attachments) > 0

        if not has_link and not has_attachment:
            await message.delete()
            return

    await bot.process_commands(message)

token = os.getenv("DISCORD_TOKEN")

if not token:
    raise ValueError("Chưa có DISCORD_TOKEN")

bot.run(token)
