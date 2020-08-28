'''
Main Script to Run Juliana Bot
'''

########################################## - Imports - ################################################
import discord as dc
from discord.ext.commands import Bot
import json

import BotLibrary
from Utils import FirebaseLibrary
from Utils import MiscLibrary
import google
from googlesearch import search
import os
import random
from discord import Member
from discord.ext.commands import has_permissions

if __name__ == '__main__':
    ########################################## - Init - ###################################################

    print("Init Bot...\n")

    # Load Bot Data
    configData = json.load(open('config.json'))
    BotName = configData['bot_name']
    TOKEN = configData['bot_token']
    # TOKEN = 'Njc4Mjg2MTMxMDcwMjM4NzQw.XkgnJw.e_jqfJbM6acEt33Y_YiOqnfdpAM'
    trigger = configData['bot_trigger']

    # Create Bot
    client = Bot(command_prefix=trigger)
    # channel = client.get_channel(678286131070238740)

    # Init Script Data
    # BotLibrary
    BotLibrary.configData = configData
    BotLibrary.client = client
    # FirebaseLibrary
    FirebaseLibrary.configData = configData
    FirebaseLibrary.DBInit()


    # Load Custom Response Commands from directory
    BotLibrary.AddCustomResponses_FromPath(path=configData['trigger-response_path'])
    # Load Custom Response Commands from Cloud
    print("Adding Custom Responses from Cloud")
    BotLibrary.AddCustomResponses_FromData(FirebaseLibrary.GetAllTriggerResponses())

    print("\nAll Custom Responses Loaded\n")

    print("\n\n")

    ########################################## - Bot Events - #############################################
    # Bot Started Event
    @client.event
    async def on_ready():
        print('Logged in as')
        print(client.user.name)
        print(client.user.id)
        print(str(client.user))
        print('------')
        print("\n\n")
        return

    ########################################## - Basic Ping Commands - ####################################
    # Basic Commands
    BotLibrary.AddCommandsFromFile(client, 'Commands/Commands_Basic.py', globals())

    ########################################## - Admin Commands - ########################################
    BotLibrary.AddCommandsFromFile(client, 'Commands/Commands_Admin.py', globals())

    ########################################## - Further Commands - ########################################
    # 8 Ball Random Reponse
    BotLibrary.AddCommandsFromFile(client, 'Commands/Commands_8Ball.py', globals())

    # Trigger-Response Commands
    BotLibrary.AddCommandsFromFile(client, 'Commands/Commands_Trigger-Response.py', globals())

    # Stack Overflow Commands
    BotLibrary.AddCommandsFromFile(client, 'Commands/Commands_StackOverflow.py', globals())

    #Google Commands
    BotLibrary.AddCommandsFromFile(client, 'Commands/Commands_google.py', globals())

    ########################################## - LOAD COGS - #####################################################

    for cog in os.listdir(os.path.abspath("Cogs")):
        if cog.endswith(".py"):
            try:
                cog = f"Cogs.{cog.replace('.py', '')}"
                client.load_extension(cog)
                print("Loaded ", cog)

            except Exception as e:
                print(f"{cog} cannot be loaded")
                raise e

    ########################################## - RUN - #####################################################
    # Run the Client
    client.run(TOKEN)
