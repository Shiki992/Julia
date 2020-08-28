#######################################################################################################################################

import asyncio
import functools
import itertools
import math
import random
import time

import discord
from async_timeout import timeout
from discord.ext import commands,tasks
from discord.ext.commands import has_permissions 
from itertools import cycle

#######################################################################################################################################


class Moderation_Commands(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

   ############################################-------Clear Messages by User------#######################################################

    @commands.command(aliases=['del','prune','delete','purge'])
    @has_permissions(manage_messages=True)
    async def clear(self, ctx, limit : int = 10, member:discord.Member=None):
        '''Clean a number of messages (optional by a user also)'''
        if member is None:
            await ctx.channel.purge(limit = limit+1)
        else:
            await ctx.channel.purge(limit = 1)
            async for message in ctx.channel.history(limit=limit+1):
                if message.author is member:
                    await message.delete()

  ##########################################-----Unban a member-----################################################################
    @commands.command(name = "unban" , pass_context = True)
    # @has_permissions(Administrator=True)
    async def unban(self , context , * , member ):
        '''Unban a user.
        Should be of the format membername#discriminator code Ex: unban Abc#XXXX
        '''
        banned_users = await context.guild.bans()
        member_name , member_discriminator = member.split('#')
        #Should be of the format membername#discriminator code Ex: unban Shiki Brekksten#7042
        for ban_entry in banned_users:
            user = ban_entry.user
            if( user.name , user.discriminator ) == ( member_name, member_discriminator ):
                await context.guild.unban(user)
                print(f"Unbanned {user.name}#{user.discriminator}")
                await context.send(f"Unbanned {user.name}#{user.discriminator}")
                return 

def setup(bot):
    bot.add_cog(Moderation_Commands(bot))