'''
Library to custom access firebase from bot
'''

# Imports
import firebase_admin
import firestore
import google.cloud
from firebase_admin import credentials, firestore

import pandas as pd
import numpy as np
import os
from tqdm import tqdm

# Global Params
configData = {}

cred = None
app = None
db = None

# Init
def DBInit():
    global cred
    global app
    global db

    cred = credentials.Certificate(configData['firebase_credentials_path'])
    app = firebase_admin.initialize_app(cred)

    db = firestore.client()

# Generic Functions
def ReadCollection(CollectionName):
    ''' Returns a array of dictionaries of the data in the collection '''
    doc_ref = db.collection(CollectionName)

    try:
        docs = doc_ref.stream()
        return docs
        
    except google.cloud.exceptions.NotFound:
        return None

def WriteDocumentToCollection(CollectionName, DocumentID, DocumentData, merge=True):
    ''' Writes {DocumentData} to cloud {DocumentID} in {CollectionName} '''
    db.collection(CollectionName).document(DocumentID).set(DocumentData, merge=merge)

def PrintCollection(CollectionName):
    ''' Prints all Documents in {CollectionName}'''
    docs = ReadCollection(CollectionName)
    if docs == None:
        print(u'Missing data')
    else:
        for doc in docs:
            print(u'Doc Data:{}'.format(doc.to_dict()))

# Specific Functions
def GetTriggerResponseDict(Data):
    return {
        'trigger': Data.trigger, 
        'response': Data.response, 
        'tag': Data.tag, 
    }

def GetTriggerResponse(trigger, response, tag):
    return {
        'trigger': trigger, 
        'response': response, 
        'tag': tag, 
    }

def GetAllTriggerResponses():
    ''' Returns all Trigger Responses from Cloud '''
    return ReadCollection(configData['firebase_collection_name_trigger-response_data'])

def AddTriggerResponse2Cloud(trigger, response):
    ''' Writes Trigger Response to cloud '''
    tr = GetTriggerResponse(trigger, response, '')
    WriteDocumentToCollection(configData['firebase_collection_name_trigger-response_data'], trigger + " - " + response, tr, merge=True)


def AddTriggerResponsesFromFile2Cloud(filepath):
    ''' Writes all Custom Trigger Responses in a file to cloud '''

    # Read file
    data = np.array([])
    ext = os.path.splitext(filepath)[1]
    if ext == '.csv':
        data = pd.read_csv(filepath)
        # Add all trigger-responses
        for i in tqdm(data.shape[0]):
            tr = GetTriggerResponse(data['trigger'][i], data['response'][i], ' ')
            WriteDocumentToCollection(configData['firebase_collection_name_trigger-response_data'], data['trigger'][i] + " - " +  data['response'][i], tr, merge=True)

    elif ext == '.txt':
        n = 0
        for line in tqdm(open(filepath, 'r').readlines()):
            # Parse
            MessageSplitUp = line.strip().split(' - ')
            if len(MessageSplitUp) == 1 or MessageSplitUp[0] == '':
                continue
            triggerWord = MessageSplitUp[0]
            ResponseText = ' - '.join(MessageSplitUp[1:])
            tr = GetTriggerResponse(triggerWord, ResponseText, ' ')
            WriteDocumentToCollection(configData['firebase_collection_name_trigger-response_data'], triggerWord + " - " + ResponseText, tr, merge=True)
            n += 1

# Specific Classes
class TriggerResponse:
    ''' Stores Details of a Custom Response '''
    def __init__(self, trigger, response, tag):
        self.trigger = trigger
        self.response = response
        self.tag = tag