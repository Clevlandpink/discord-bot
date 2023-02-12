# Third Party Imports
import discord
from discord.ext import commands

skills = [
            "<:Hiscores:571158948187734022>",
            "<:Attack:571158948544249856>",
            "<:Defence:571158948506501131>",
            "<:Strength:571158948678205441>",
            "<:Hitpoints:571158948552638534>",
            "<:Ranged:571158948539924497>",
            "<:Prayer:571158948434935826>",
            "<:Magic:571158948388929566>",
            "<:Cooking:571158948569284655>",
            "<:Woodcutting:571158948758159360>",
            "<:Fletching:571158948225220660>",
            "<:Fishing:571158948569284636>",
            "<:Firemaking:571158948548313108>",
            "<:Crafting:571158948208705558>",
            "<:Smithing:571158948686594098>",
            "<:Mining:571158948602839040>",
            "<:Herblore:571158948326146075>",
            "<:Agility:571158948774674432>",
            "<:Thieving:571158948657233941>",
            "<:Slayer:571158948376346654>",
            "<:Farming:571158948334403665>",
            "<:Runecraft:571158948732862494>",
            "<:Hunter:571158948380409882>",
            "<:Construction:571158948632330250>",
        ]

class Runescape(commands.Cog):
    """Commands related to runescape."""

    def __init__(self, bot):
        self.bot = bot
        self.session = self.bot.session


    async def get_stats(self, username):
        response = await self.bot.text_session('GET', f"http://services.runescape.com/m=hiscore_oldschool/index_lite.ws?player={username}")
        return response

    def create_stats_embed(self, stats):
        levels = []
        fields = stats.split(",")
        for f in fields:
            levels.append(f)

        embed = discord.Embed(colour=discord.Colour(0x4A90E2))
        embed.add_field(name="⠀", value=skills[0] + " " + levels[1], inline=True)
        embed.add_field(name="⠀", value=skills[1] + " " + levels[3], inline=True)
        embed.add_field(name="⠀", value=skills[2] + " " + levels[5], inline=True)
        embed.add_field(name="⠀", value=skills[3] + " " + levels[7], inline=True)
        embed.add_field(name="⠀", value=skills[4] + " " + levels[9], inline=True)
        embed.add_field(name="⠀", value=skills[5] + " " + levels[11], inline=True)
        embed.add_field(name="⠀", value=skills[6] + " " + levels[13], inline=True)
        embed.add_field(name="⠀", value=skills[7] + " " + levels[15], inline=True)
        embed.add_field(name="⠀", value=skills[8] + " " + levels[17], inline=True)
        embed.add_field(name="⠀", value=skills[9] + " " + levels[19], inline=True)
        embed.add_field(name="⠀", value=skills[10] + " " + levels[21], inline=True)
        embed.add_field(name="⠀", value=skills[11] + " " + levels[23], inline=True)
        embed.add_field(name="⠀", value=skills[12] + " " + levels[25], inline=True)
        embed.add_field(name="⠀", value=skills[13] + " " + levels[27], inline=True)
        embed.add_field(name="⠀", value=skills[14] + " " + levels[29], inline=True)
        embed.add_field(name="⠀", value=skills[15] + " " + levels[31], inline=True)
        embed.add_field(name="⠀", value=skills[16] + " " + levels[33], inline=True)
        embed.add_field(name="⠀", value=skills[17] + " " + levels[35], inline=True)
        embed.add_field(name="⠀", value=skills[18] + " " + levels[37], inline=True)
        embed.add_field(name="⠀", value=skills[19] + " " + levels[39], inline=True)
        embed.add_field(name="⠀", value=skills[20] + " " + levels[41], inline=True)
        embed.add_field(name="⠀", value=skills[21] + " " + levels[43], inline=True)
        embed.add_field(name="⠀", value=skills[22] + " " + levels[45], inline=True)
        embed.add_field(name="⠀", value=skills[23] + " " + levels[47], inline=True)

        return embed

    @commands.hybrid_command(name="lookup", aliases=["skills", "stats"], hidden=False)
    #@commands.command(name="lookup", aliases=["skills", "stats"], pass_context=True)
    async def lookup(self, ctx, user: str):
        """Looks up a user's runescape stats."""
        
        stats = await self.get_stats(user)
        embed = await self.bot.loop.run_in_executor(None, self.create_stats_embed, stats)
        await ctx.send(content=user, embed=embed)

    #@commands.command(name="rs", pass_context=True)
    @commands.hybrid_command(name="rs", hidden=False)
    @commands.cooldown(1, 10, commands.BucketType.default)
    async def rs(self, ctx, *, search: str):
        """Search osrs wiki."""
        url = await self.bot.get_session("https://oldschool.runescape.wiki/api.php?action=opensearch&search=" + search + "&format=json&limit=1")
        await ctx.send(url[3][0].strip('"'))

async def setup(bot):
    await bot.add_cog(Runescape(bot))
