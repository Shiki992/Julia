'''
Library for accessing the bot easily
'''

# Imports
import discord as dc
from discord.ext.commands import Bot
import pandas as pd
import os
from tqdm import tqdm

# Global Params
configData = {}
client = None

# Bot Main Functions
# Init
def CreateBot(TriggerPrefix):
    ''' Creates a Bot, DUH '''
    return Bot(command_prefix=TriggerPrefix)

# Run
def RunBot(client, TOKEN):
    ''' Runs the Bot, DUH '''
    client.run(TOKEN)

# Bot Command Functions
def AddCommandsFromFile(client, cmdpath, globals=None):
    ''' Adds Python Client Commands from a file to the client '''
    CommandsCode = open(cmdpath, 'r').read()
    if globals == None:
        exec(CommandsCode)
    else:
        exec(CommandsCode, globals)


def AddResponseCommand(triggerWord, ResponseText):
    ''' Adds Trigger-Response Client Commands to the client '''
    NewClientCommandCode = open(configData['trigger-response_code'], 'r').read()
    exec_code = NewClientCommandCode.replace('triggerWord', "'" + triggerWord + "'")
    exec_code = exec_code.replace('ResponseText', "'" + ResponseText + "'")
    exec(exec_code)

def AddCustomResponses_FromPath(path):
    ''' Adds Custom Trigger-Response from a file or files in a directory '''

    # Check if file or dir
    if os.path.isdir(path):
        print("Adding Custom Responses from directory", path)

        # Add all files as custom responses
        for fname in os.listdir(path):
            fpath = os.path.join(path, fname)
            if os.path.isfile(fpath):
                AddCustomResponses_FromPath(path=fpath)

    elif os.path.isfile(path):
        print("Adding Custom Responses from file", path)

        # Check Extension of file
        ext = os.path.splitext(path)[1]

        # If csv file
        if ext == '.csv':
            triggerKey = None
            responseKey = None
            n_cmds = 0
            data = pd.read_csv(path)
            for key in data.keys():
                key_check = key.strip().upper()
                if "TRIGGERWORD".startswith(key_check) and triggerKey == None:
                    triggerKey = key
                elif "RESPONSETEXT".startswith(key_check) and responseKey == None:
                    responseKey = key
                    
            if ((not triggerKey == None) and (not responseKey == None)):
                for i in tqdm(range(data.shape[0])):
                    print(str(n_cmds+1) + ':', data[triggerKey][i], '-', data[responseKey][i])
                    # Add to client
                    AddResponseCommand(data[triggerKey][i], data[responseKey][i])

                    n_cmds += 1

                

        # If txt file
        elif ext == '.txt':
            # Read file and add line by line
            n_cmds = 0
            for line in tqdm(open(path, 'r').readlines()):
                # Parse
                MessageSplitUp = line.strip().split(' - ')
                if len(MessageSplitUp) == 1 or MessageSplitUp[0] == '':
                    continue
                triggerWord = MessageSplitUp[0]
                ResponseText = ' - '.join(MessageSplitUp[1:])
                print(str(n_cmds+1) + ':', triggerWord, '-', ResponseText)

                # Add to client
                AddResponseCommand(triggerWord, ResponseText)

                n_cmds += 1

def AddCustomResponses_FromData(data):
    ''' Adds Custom Trigger-Response from array of dictionaries '''

    for tr in data:
        tr = tr.to_dict()
        if 'trigger' in tr.keys() and 'response' in tr.keys():
            AddResponseCommand(tr['trigger'], tr['response'])