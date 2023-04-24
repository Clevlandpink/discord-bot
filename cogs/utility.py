import random

import discord
from discord.ext import commands
from discord import app_commands

class Utility(commands.Cog):
    """Commands providing simple utility."""

    def __init__(self, bot):
        self.bot = bot
    
    @commands.hybrid_command(name="choose", aliases=["pick"], hidden=False)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def choose(self, ctx, *, message):
        """Picks a random item from given list Arguments should be seperated by commas.

        **Args:**
            ``list`` : List of items to pick from.
        
        **Example:**
            ```!pick One, Two, Three```
        """

        args = message.split(",")
        if len(args) <= 1:
            await ctx.send("List items should be seperated by commas.", delete_after=10)
            return
        else:
            await ctx.send(random.choice(args))
    
    @commands.hybrid_command(name="roll", aliases=["dice"], hidden=False)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def roll(self, ctx, number: int = 10):
        """Outputs a random number between 1 and the given number. Default 10.

        **Args:**
            ``number (int, optional)`` : Max possible number. Defaults to 10. Max: 10,000

        **Example:**
            ```!roll 12```
        """
        if number > 10000:
            number = 10000
        elif number <= 1:
            number = 2

        await ctx.send(random.randint(1, number))

    @commands.hybrid_command(name="flip", aliases=["coinflip", "coin"], hidden=False)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def flip(self, ctx):
        """Flips a coin.

        **Example:**
            ```!flip```
        """
        coin = random.randint(1, 2)
        if coin == 1:
            await ctx.send("Heads")
        else:
            await ctx.send("Tails")

    @commands.hybrid_command(name="prune", aliases=["purge", "delete"])
    @commands.guild_only()
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.has_permissions(manage_messages=True)
    #@commands.is_owner()
    async def prune(self, ctx, number: int):
        """Bulk deletes given number of __recent__ messages.

        **Requires:**
            ```Manage Messages```

        **Args:**
            number : Number of messages to delete. Max 10 to prevent abuse.

        **Example:**
            ```!prune 10```
        """
        if number > 10:
            number = 10
        elif number < 1:
            pass
        messages = []
        async for x in ctx.message.channel.history(limit=number + 1):
            messages.append(x)
        await ctx.message.channel.delete_messages(messages)
        await ctx.send(str(number) + " messages deleted.", delete_after=True)

    
    @commands.hybrid_command(name="move", hidden=False)
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.has_any_role(156929098583638017, 845512204403867678) # Temporary workaround
    #@commands.has_permissions(move_members=True) # Seems to be broken right now.
    async def move(self, ctx, *, channel: discord.VoiceChannel):
        """Moves all members of your current channel to the given channel.

        **Requires:**
            ```Move Members```

        **Args:**
            channel : The channel to move members to. Case sensitive.

        **Example:**
            ```!move Lobby```
        """
        try:
            r = ctx.author.voice.channel.members
        except Exception:
            await ctx.send("You must be in a voice channel to use this command.")
            return
        overwrites = channel.overwrites_for(ctx.author.top_role)
        if overwrites.connect is False or overwrites.move_members is False:
            await ctx.send("You do not have permission to move to this channel.")
            return
        for m in r:
            await m.move_to(channel)
        await ctx.send("Success!", delete_after=1)
    
async def setup(bot):
    await bot.add_cog(Utility(bot))
