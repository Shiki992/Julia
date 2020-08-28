'''
Add Trigger-Response Commands for the bot
'''

# Main Functions
# Add Response
@client.command(name='addresp', pass_context=True)
async def on_addresp(context, *, message=None):
    # Imports
    import pandas as pd
    global BotLibrary
    global FirebaseLibrary

    if message == None:
        await context.channel.send("Give in format: TriggerWord - ResponseText " + context.message.author.mention)
        return

    print("Trigerred Add Reponse ", message)
    # Parse to get triggerWord and ResponseText
    MessageSplitUp = message.strip().split(' - ')
    if len(MessageSplitUp) == 1 or MessageSplitUp[0] == '':
        await context.channel.send("Give in format: TriggerWord - ResponseText " + context.message.author.mention)
        return
    triggerWord = MessageSplitUp[0]
    ResponseText = ' - '.join(MessageSplitUp[1:])
    print("TriggerWord - ", triggerWord)
    print("ResponseText - ", ResponseText)

    # Add to Response
    BotLibrary.AddResponseCommand(triggerWord, ResponseText)

    ## DEPRECIATED - SHIFTED TO CLOUD
    # Add to AddedResponses.csv
    #data = pd.read_csv(configData['added_responses_path'])
    #data = data.append({"trigger": triggerWord, "response": ResponseText}, ignore_index=True)
    #data.to_csv(configData['added_responses_path'], index=False)
    ## DEPRECIATED - SHIFTED TO CLOUD

    FirebaseLibrary.AddTriggerResponse2Cloud(triggerWord, ResponseText)

    await context.channel.send("Added Response " + context.message.author.mention)
    return