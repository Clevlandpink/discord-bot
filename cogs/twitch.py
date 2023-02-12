# Standard library imports

# Third Party Imports
from discord.ext import commands, tasks


# Local Imports
from modules import config

class Twitch(commands.Cog):
    """Commands related to Twitch."""

    def __init__(self, bot):
        self.bot = bot
        self.session = self.bot.session

        self.headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': '',
            'Client-Id': config.TWITCH_ID
        }

        self.data = {
            'client_id': config.TWITCH_ID,
            'client_secret': config.TWITCH_SECRET,
            'grant_type': 'client_credentials'
        }

        self.authorize.start()
        
    def cog_unload(self):
        self.authorize.cancel()

    @tasks.loop(hours=24)
    async def authorize(self):
        response = await self.bot.post_session("https://id.twitch.tv/oauth2/token", json=self.data)
        self.headers["Authorization"] = f"Bearer {response['access_token']}"

    async def get_user(self, login):
        response = await self.bot.get_session(f"https://api.twitch.tv/helix/users?login={login}", headers=self.headers)
        return response
    
    async def is_live(self, login):
        response = await self.bot.get_session(f"https://api.twitch.tv/helix/streams?user_login={login}", headers=self.headers)
        if len(response["data"]) == 0:
            return False
        return True

    @commands.command(name="info")
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.is_owner()
    async def info(self, ctx, login):
        response = await self.get_user(login)
        await ctx.send(response)

    @commands.command(name="live")
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.is_owner()
    async def live(self, ctx, login):
        response = await self.is_live(login)
        await ctx.send(response)


async def setup(bot):
    await bot.add_cog(Twitch(bot))
