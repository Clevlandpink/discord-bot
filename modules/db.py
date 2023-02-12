import discord
from discord.ext import commands
import asyncpg
import asyncio
import traceback
from modules import config

class Db:

    @classmethod
    async def create_pool(cls):
        """Initialize database connection."""
        cls.pool = await asyncpg.create_pool(user=config.DB_USER, password=config.DB_PASSWORD, host=config.DB_HOST, database=config.DB_DATABASE)
        print("Connection pool created.")

    @classmethod
    async def get_pool(cls):
        if cls.pool:
            return cls.pool
        else:
            return None


    @staticmethod
    async def init_db():
        pool = Db.pool
        file = open("modules/setup.sql", 'r')
        data = file.read()
        file.close()
        sql = data.split(";")
        async with pool.acquire() as conn:
            for command in sql:
                await conn.execute(command)
        print("Successfully initialized db.")

    @staticmethod
    async def is_guild_owner(member: discord.Member, guild: discord.Guild,conn):
        #return True if await conn.fetchrow("SELECT * FROM guilds WHERE guild_id=$1 AND owner_id=$2", guild.id, member.id) else False
        return True if member.id == guild.owner_id else False
    
    @staticmethod
    async def has_permission(ctx, *permissions):
        if is_owner := await ctx.bot.is_owner(ctx.author):
            return True
        
        author_roles = ctx.author.roles
        
        if (pool := Db.pool) is None:
            await ctx.send("Failed to connect to permissions server.")
            return False

        async with pool.acquire() as conn:
            if await Db.is_guild_owner(ctx.author, ctx.guild, conn):
                #return True
                pass
            try:
                for p in permissions:
                    row = await conn.fetch("SELECT * FROM permissions WHERE guild_id=$1 AND permission=$2", ctx.guild.id, p)
                    if row is not None:
                        for r in row:
                            for role in author_roles:
                                if r["role_id"] == role.id:
                                    return True
            except Exception as e:
                print(f"ERROR: {type(e).__name__} - {e}")
            await conn.close()
            return False
    
    @staticmethod
    async def db_permission(ctx, perm: str, roles, action):
        pool = Db.pool
        async with pool.acquire() as conn:
            try:
                for r in roles:
                    row = await conn.fetchrow("SELECT * FROM permissions WHERE guild_id=$1 AND role_id=$2 AND permission=$3", ctx.guild.id, r.id, perm)
                    if row is None and action == "grant":
                        await conn.execute("INSERT INTO permissions(guild_id, role_id, permission) VALUES($1, $2, $3)", ctx.guild.id, r.id, perm)
                        return True
                    elif row is not None and action == "revoke":
                        await conn.execute("DELETE FROM permissions WHERE guild_id=$1 AND role_id=$2 AND permission=$3", ctx.guild.id, r.id, perm)
                        return True
                    else:
                        return False
            except Exception as e:
                print(f"ERROR: {type(e).__name__} - {e}")
        return False

    @staticmethod
    async def init_guild(guild):
        pool = Db.pool
        async with pool.acquire() as conn:
            try:
                row = await conn.fetchrow("SELECT * FROM guilds WHERE guild_id =$1", guild.id)
            except Exception as e:
                    print(f"ERROR: {type(e).__name__} - {e}")
            if row is None:
                print("No results, creating new entry.")
                await conn.execute("INSERT INTO guilds(guild_id, owner_id) VALUES($1, $2)", guild.id, guild.owner_id)






