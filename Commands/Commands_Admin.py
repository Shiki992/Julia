'''
Admin Commands for the bot
'''

# Imports
# import discord as dc
from discord import Member
from discord.ext.commands import has_permissions

# Main Functions
# Ban User
@client.command(name='ban',pass_context=True)
@has_permissions(ban_members=True)
async def ban(context,user:dc.Member,*,reasons=None):
    if reasons==None:
        reasons= "no reason :person_shrugging:"
    await user.ban(reason=reasons)
    embed=dc.Embed(title="User banned!", description=("**"+user.mention+"** was banned by **"+str(context.message.author.mention)+"** because "+reasons).format(user, context.message.author), color=0xff00f6)
    await context.send(embed=embed)
    async for message in context.channel.history():
        if message.author is user:
            await message.delete()
    await user.send(embed=embed)

# Kick User
@client.command(name='kick',pass_context=True)
@has_permissions(kick_members=True)
async def kick(context,user:dc.Member,*,reasons=None):
    try:
        if reasons==None:
            reasons= "no reason :person_shrugging:"
        
        await user.kick(reason=reasons)
        embed=dc.Embed(title="User Kicked!", description=("**"+user.mention+"** was kicked by **"+str(context.message.author.mention)+"** because "+reasons).format(user, context.message.author), color=0xff00f6)
        await context.send(embed=embed)
        await user.send(embed=embed)
    except dc.Forbidden:
        await context.send("Nice try but you do not have permission qt :stuck_out_tongue_winking_eye:"+context.message.author.mention)
    
    return

# Mute User
# DOESNT WORK
@client.command(name='mute',pass_context = True)
async def mute(ctx, member: dc.Member):
     if ctx.message.author.guild_permissions.administrator:
        role = dc.utils.get(member.guild.roles, name='Muted')
        print(str(role)+"\n")
        if str(role) == "None":
            author = ctx.message.author
            # split the string to get the rolename to create
            # role_name = ctx.message.content.lower().split("!rolecreate ", maxsplit=1)[1]
            perms = dc.Permissions(send_messages=False, read_messages=True)
            role = await Guild.create_role(name="Muted", colour=dc.Colour(0x000000),permissions=perms)
            await member.add_roles(member, role)
            embed=dc.Embed(title="User Muted!", description=("**"+member+"** was muted by **"+str(ctx.message.author)+"**!").format(member, ctx.message.author), color=0xff00f6)
            await ctx.send(embed=embed)
        else:
            await member.add_roles(member, role)
            embed=dc.Embed(title="User Muted!", description=("**"+member+"** was muted by **"+str(ctx.message.author)+"**!").format(member, ctx.message.author), color=0xff00f6)
            await ctx.send(embed=embed)
     else:
         embed=dc.Embed(title="Permission Denied.", description="You don't have permission to use this command.", color=0xff00f6)
         await ctx.say(embed=embed)

