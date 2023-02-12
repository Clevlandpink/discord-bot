import discord
from discord.ext import commands

class HelpCommand(commands.MinimalHelpCommand):
    help_thumbnail = "https://media.discordapp.net/attachments/454498602073587725/1041135107047702538/ruined.png"
    def get_command_signature(self, command):
        return self.context.clean_prefix+ '{1.qualified_name} {1.signature}'.format(self, command)

    def get_help_desc(self):
        return 'Use {0}{1} [command] for more info on a command.'.format(self.context.clean_prefix, self.invoked_with)

    async def send_bot_help(self, mapping):
        embed = discord.Embed(title="Commands")
        embed.description = self.get_help_desc()
        embed.set_thumbnail(url=HelpCommand.help_thumbnail)

        for cog, commands, in mapping.items():
            name = "No Category" if cog is None else cog.qualified_name
            filtered = await self.filter_commands(commands, sort=False)
            if filtered:
                value = ' | '.join(f"``{c.name}``" for c in filtered)
                #if cog and cog.description:
                    #value = '{0}\n{1}'.format(cog.description, value)
                embed.add_field(name=name, value=value, inline=False)
        embed.set_footer(text="Names are case sensitive.")
        await self.get_destination().send(embed=embed)
    
    async def send_cog_help(self, cog):
        embed = discord.Embed(title="{0.qualified_name} Commands".format(cog))
        embed.set_thumbnail(url=HelpCommand.help_thumbnail)
        if cog.description:
           embed.description = cog.description
        filtered = await self.filter_commands(cog.get_commands(), sort=True)
        for command in filtered:
            print(command)
            embed.add_field(name=command.qualified_name, value=command.short_doc or '...', inline=False)
        embed.set_footer(text=self.get_help_desc())
        await self.get_destination().send(embed=embed)
    
    async def send_group_help(self, group):
        embed = discord.Embed(title=group.qualified_name)
        embed.set_thumbnail(url=HelpCommand.help_thumbnail)
        if group.help:
            embed.description = group.help

        if isinstance(group, commands.Group):
            filtered = await self.filter_commands(group.commands, sort=True)
            for command in filtered:
                embed.add_field(name=command.qualified_name, value=command.short_doc or '...', inline=True)

        embed.set_footer(text=self.get_help_desc())
        await self.get_destination().send(embed=embed)
        
    async def send_command_help(self, command):
        embed = discord.Embed(title=command.qualified_name)
        embed.set_thumbnail(url=HelpCommand.help_thumbnail)
        if command.help:
            embed.description = command.help
        embed.add_field(name="Syntax", value=f"```{self.get_command_signature(command)}```")
        if command.aliases:
            embed.add_field(name="Aliases", value=' | '.join(f"``{c}``" for c in command.aliases), inline=False)
        await self.get_destination().send(embed=embed)

    @staticmethod
    async def error_help(ctx, command):
        
        embed = discord.Embed(title=command.qualified_name)
        #embed.add_field(name="Syntax", value=f"```{HelpCommand.get_command_signature(HelpCommand, command)}```")
        if command.help:
            if example := command.help.split("**Example:**"): 
                embed.add_field(name="Example", value=example[1], inline=False)
                embed.set_footer(text=f"For more details use !help [{command}].")
        else:
            await ctx.send(f"{command.qualified_name} is missing docs.")

        await ctx.send(embed=embed, delete_after=20)

class Help(commands.Cog):
    """Commands for getting help with other commands."""
    def __init__(self, bot):
        self.bot = bot
        self._original_help_command = bot.help_command
        bot.help_command = HelpCommand()
        bot.help_command.cog = self

    def cog_unload(self):
        self.bot.help_command = self._original_help_command
        



async def setup(bot):
    await bot.add_cog(Help(bot))