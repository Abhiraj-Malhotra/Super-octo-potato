import asyncio
import subprocess

import discord
import yt_dlp
from discord.ext import commands


def check_ffmpeg():
    try:
        subprocess.run(['ffmpeg', '-version'], 
                       check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except FileNotFoundError:
        return False

if not check_ffmpeg():
    raise RuntimeError("FFmpeg is not installed or not found in the PATH.")

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

FFMPEG_OPTIONS = {'executable': '/path/to/ffmpeg', 'options': '-vn'}
YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': True}

class MusicCog(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.queue = []

    @commands.command()
    async def play(self, ctx, *, search):
        voice_channel = ctx.author.voice.channel if ctx.author.voice.channel else None

        if not voice_channel:
            return await ctx.send("You are not in a voice channel.")

        if not ctx.voice_client:
            await voice_channel.connect()

        async with ctx.typing():
            with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
                info = ydl.extract_info(f'ytsearch:{search}', download=False)
                if isinstance(info, dict) and 'entries' in info:
                    info = info['entries'][0]
                    if info:
                        url = info['url']
                        title = info['title']
                        self.queue.append((url, title))
                        await ctx.send(f'Added {title} to the queue')
                    else:
                        await ctx.send("Could not find a matching video.")
                else:
                    await ctx.send("No results found.")

        if not ctx.voice_client.is_playing():
            await self.play_next(ctx)

    async def play_next(self, ctx):
        if self.queue:
            url, title = self.queue.pop(0)
            try:
                source = discord.FFmpegPCMAudio(url, **FFMPEG_OPTIONS)
                ctx.voice_client.play(
                    source,
                    after=lambda _: self.client.loop.create_task(self.play_next(ctx))
                )
                await ctx.send(f'Now playing **{title}**')
            except Exception as e:
                await ctx.send(f"An error occurred: {e}")
        else:
            await ctx.send("Queue is empty.")

    @commands.command()
    async def skip(self, ctx):
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.stop()
            await ctx.send("Skipped")
        else:
            await ctx.send("No audio is playing to skip.")

client = commands.Bot(command_prefix="!", intents=intents)

async def main():
    token = 'YOUR BOT TOKEN'
    await client.add_cog(MusicCog(client))
    await client.start(token)

asyncio.run(main())
