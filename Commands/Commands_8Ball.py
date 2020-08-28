'''
8Ball Commands for the bot
'''

# Main Functions
@client.command(name='8ball', pass_context=True, aliases=['is', 'does', 'will','what'])
async def eight_ball(context):
    # Imports
    import random

    print("Trigerred 8ball Reponse to", context)
    possible_responses=['As I see it, yes',
    'Ask again later',
    'Better not tell you now',
    'Cannot predict now',
    'Concentrate and ask again',
    'Don’t count on it',
    'It is certain',
    'It is decidedly so',
    'Most likely',
    'My reply is no',
    'My sources say no',
    'Outlook not so good',
    'Outlook good',
    'Reply hazy, try again',
    'Signs point to yes',
    'Very doubtful',
    'Without a doubt',
    'Yes',
    'Yes – definitely',
    "You may rely on it"]
    await context.channel.send(random.choice(possible_responses) + context.message.author.mention)
    return