'''
Stack Overflow Commands for the bot
'''

@client.command(name='so', pass_context=True)
async def stackoverflow(context, query=None):
    print("Trigerred Stack Overflow Check:", query)
    json_resp = MiscLibrary.StackOverflow_SearchQuery(query)
    response = MiscLibrary.GetAnswerURLs(json_resp)
    responseText = ""
    for resp in response:
        responseText += str(resp) + "\n"
    embed = dc.Embed(title="StackOverflow", description=responseText)
    await context.send(embed=embed)
    # MiscLibrary.OpenURLs(response)