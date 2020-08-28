'''
Basic Commands for the bot
'''

# Main Functions
# Hello Command
@client.command(name='hello',pass_context=True)
async def on_hello(message):
    # Bot should not reply to itself
    if message.author == client.user:
        return

    print("Trigerred Hello Response to", message)
    msg = 'Hello {0.author.mention}'.format(message)
    await message.channel.send(msg)
    return