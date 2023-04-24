# Standard library imports
import traceback
import sys
import logging
import datetime
import asyncio

# Third Party Imports
import discord
from discord.ext import commands
import aiohttp

# Local Imports
from modules import config
from cogs.help import HelpCommand

logger = logging.getLogger(__name__)

command_prefixs = ["!", "."]

extensions = [
    "cogs.owner",
    "cogs.help",
    "cogs.utility",
    "cogs.runescape",
    #"cogs.name",
    #"cogs.strongpond",
    "cogs.twitch",
]

class PondBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()
        super().__init__(command_prefix=command_prefixs, pm_help=False, intents=intents)

        self.spam_control = commands.CooldownMapping.from_cooldown(10, 12.0, commands.BucketType.user)

    async def setup_hook(self):
        self.session = aiohttp.ClientSession(loop=self.loop)
        for extension in extensions:
            try:
                await self.load_extension(extension)
                print(extension + " loaded.")
            except Exception:
                print(f"Failed to load extension {extension}.", file=sys.stderr)
                traceback.print_exc()

    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.NoPrivateMessage):
            await ctx.author.send('This command cannot be used in private messages.', delete_after=5)
        elif isinstance(error, commands.MissingRequiredArgument):
            await HelpCommand.error_help(self, ctx)
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(f'You need the ``{error.missing_perms}`` permission to perform that action.', delete_after=5)
        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.send(f'I need the ``{error.missing_perms}`` permission to perform that action.', delete_after=5)
        elif isinstance(error, discord.Forbidden):
            await ctx.author.send(f'``{error.response}``', delete_after=5)
        elif isinstance(error, commands.DisabledCommand):
            await ctx.author.send('This command is disabled.', delete_after=5)
        elif isinstance(error, commands.PrivateMessageOnly):
            await ctx.message.delete()
            await ctx.send("This command can only be used in DM.", delete_after=5)
        elif isinstance(error, commands.CheckFailure):
            await ctx.send(error, delete_after=5)
        elif isinstance(error, commands.CommandNotFound):
            return
        elif isinstance(error, commands.MaxConcurrencyReached):
            await ctx.message.delete()
            await ctx.send("You already have an instance of this command running.", delete_after=5)
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"That command is on cooldown. Try again in ``{round(error.retry_after)}``s.", delete_after=error.retry_after)
        elif isinstance(error, commands.CommandInvokeError):
            original = error.original
            if not isinstance(original, discord.HTTPException):
                print(f'In {ctx.command.qualified_name}:', file=sys.stderr)
                traceback.print_tb(original.__traceback__)
                print(f'{original.__class__.__name__}: {original}', file=sys.stderr)
        elif isinstance(error, commands.ArgumentParsingError):
            await ctx.send(error)
        else:
            await ctx.send(error)
    
    async def on_ready(self):
        if not hasattr(self, 'uptime'):
            self.uptime = datetime.datetime.utcnow()
        print(f"\n{self.user.name} online - Discord Version: {discord.__version__}\n")
        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Cindr.org"))

    async def on_message(self, message):
        if message.author.bot:
            return
        await self.process_commands(message)
    
    async def close(self) -> None:
        await super().close()
        await self.session.close()

    async def get_session(self, *arg, **kwargs):
        async with self.session.get(*arg, **kwargs) as resp:
            return await resp.json()
     
    async def post_session(self, *arg, **kwargs):
        async with self.session.post(*arg, **kwargs) as resp:
            return await resp.json()    
    
    async def text_session(self, *arg, **kwargs):
        async with self.session.request(*arg, **kwargs) as resp:
            return await resp.text()

bot = PondBot()

async def main():
    async with bot:
        await bot.start(config.DEV_TOKEN, reconnect=True)


asyncio.run(main())

