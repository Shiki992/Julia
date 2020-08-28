import random
import discord
from discord.ext import commands


class Levels (commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._cd = commands.CooldownMapping.from_cooldown(1, 10.0, commands.BucketType.user)
    

    async def lvl_up(self, user):
        cur_xp = user['xp']
        cur_lvl = user['lvl']

        if cur_lvl < int(cur_xp ** (1/3)):
            await self.bot.pg_con.execute("UPDATE users SET lvl = $1 WHERE user_id = $2 AND guild_id = $3", cur_lvl + 1, user['user_id'], user['guild_id'])
            return True
        else: 
            return False
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot :
            return

        async def __local_check(self, ctx):
            bucket = self._cd.get_bucket(ctx.message)
            retry_after = bucket.update_rate_limit()
            if retry_after:
            # you're rate limited
            # helpful message here
                pass
            # you're not rate limited

        author_id = str(message.author.id)
        guild_id = str(message.guild.id)

        user = await self.bot.pg_con.fetch("SELECT * FROM users WHERE user_id = $1 AND guild_id = $2", author_id, guild_id)     

        if not user:
            await self.bot.pg_con.execute("INSERT INTO users (user_id, guild_id, lvl, xp) VALUES ($1, $2, 1, 0)", author_id, guild_id,)

        user = await self.bot.pg_con.fetchrow("SELECT * FROM users WHERE user_id = $1 AND guild_id = $2", author_id, guild_id)
        await self.bot.pg_con.execute("UPDATE users SET xp = $1 WHERE user_id = $2 AND guild_id = $3", user['xp'] + random.randint(1, 3) , author_id, guild_id)

        if await self.lvl_up(user):
            #await message.channel.send(f"{message.author.mention} is now level {user['lvl'] + 1}")
            embed=discord.Embed(title="Level UP! ", description=(message.author.name+" reached Level "+str(user['lvl'] + 1) + ". Keep Going"), color=0xff00f6)
            await message.channel.send( embed = embed )
            
    @commands.command()
    async def level(self, ctx, member: discord.Member = None):
        '''To get the level of a user'''
        member = ctx.author if not member else member
        member_id = str(member.id)
        guild_id = str(ctx.guild.id)

        user = await self.bot.pg_con.fetch("SELECT * FROM users WHERE user_id = $1 AND guild_id = $2", member_id, guild_id)

        if not user:
            await ctx.send("Member doesn't have a level.")
        else:
            embed = discord.Embed(
                color = discord.Color.green(),
                timestamp = ctx.message.created_at
            )
            embed.set_author(name = f"Level - {member}", icon_url = "https://cdn.discordapp.com/attachments/554887009693335563/554887093126692865/2416585_0.jpg")
            embed.add_field(name = "Level", value = user[0]['lvl'])
            embed.add_field(name = "XP", value = user[0]['xp'])
            embed.set_footer(text = f"Requested by {ctx.author}")


            await ctx.send(embed = embed)



# await ctx.send(self.users[member_id]["level"], self.users[member_id]["exp"])
def setup(bot):
    bot.add_cog(Levels(bot))