

import csv
import json
from datetime import datetime
import requests

class Sdk:
    '''ReMAP SDK for RUL Algorithms'''

    DIR_BASE = '/app/'
    DATASET_FILE = 'dataset.csv'
    METADATA_FILE = 'metadata.json'
    METADATA='metadata'
    KC_TOKEN_URL='http://local-remap:8080/auth/realms/remapnode/protocol/openid-connect/token'
    CLIENT_ID= 'rulSDK'
    OUTPUT_URL= 'http://localhost:3200/mngTools/api/models/RulEstimation'

    start_date = None
    end_date = None
    tailNumber = None
    metadata = None
    dataset = None
    rulRunner= ""
    

    def __init__(self): 
        '''SDK constructor'''
        print("Initializing ReMAP SDK")
        pass

    def getStartTime(self):
        '''get the start time of the csv file'''
        if self.start_date is None:
            results = []
            with open(self.DIR_BASE+self.DATASET_FILE) as File:
                reader = csv.DictReader(File)
                start_date = None
                for row in reader:
                    thedatestr = row['timestamp']

                    thedate = datetime.strptime(thedatestr, '%Y-%m-%dT%H:%M:%S.%fZ')
                    #thedate = datetime.strptime(thedatestr, '%d/%m/%Y %H:%M')
                    if start_date is None:
                        start_date = thedate
                    else:
                        if start_date > thedate:
                            start_date = thedate
                    results.append(row)
                self.start_date = start_date
        return self.start_date

    def getEndTime(self):
        if self.end_date is None:
            print('buscando end time..')
            results = []
            with open(self.DIR_BASE+self.DATASET_FILE) as File:
                reader = csv.DictReader(File)
                end_date = None
                for row in reader:
                    thedatestr = row['timestamp']
                    thedate = datetime.strptime(thedatestr, '%Y-%m-%dT%H:%M:%S.%fZ')
                    #thedate = datetime.strptime(thedatestr, '%d/%m/%Y %H:%M')
                    if end_date is None:
                        end_date = thedate
                    else:
                        if end_date < thedate:
                            end_date = thedate
                    results.append(row)
                self.end_date = end_date
        return self.end_date

    def getTailNumber(self):
        if self.tailNumber is None:
            if self.metadata is None:
                with open(self.DIR_BASE+self.METADATA_FILE) as file:
                    self.metadata = json.load(file)

            self.tailNumber = self.metadata['tailNumber']
        else:
            pass
        return self.tailNumber

    def getMetadata(self):
        with open(self.DIR_BASE+self.METADATA_FILE) as file:
            self.metadata = json.load(file)
            print(self.metadata) 
        return self.metadata['metadata']

    def getReplacements (self):
        if self.metadata is None:
            with open(self.DIR_BASE+self.METADATA_FILE) as file:
                self.metadata = json.load(file)      
                 
        return self.metadata['replacements']

    def getDataset (self):
        return self.DIR_BASE+self.DATASET_FILE
    # return the component PartNo of the parameter passed as param
    
    def getParamPartNumber(self, param):
        PartNo="P/N Not Found"
        if self.metadata is None:
            with open(self.DIR_BASE+self.METADATA_FILE) as file:
                self.metadata = json.load(file)
        self.metadata=self.metadata[self.METADATA]
        for x in self.metadata:
            if x.__contains__('parameter'):
                    parameter =x['parameter']
                    if parameter is not None:
                        name=parameter['name']
                        if name == param:
                            component=parameter['component']
                            PartNo=component['partNo']
        return PartNo

    def sendOutput(self, rulUnit, rulValue, probabilityOfFailure, ConfidenceInterval):
        secret=self.__getClientSecret()
        runnerId=self.__getRulRunnerId()
        payload = {
            "serial": "Serial_NO" , #TODO config file to generate in rulRunner
            "dataset": "DatasetID" , #TODO config file to generate in rulRunner
            "model":"modelId", #TODO to implement when its implemented in rulRunner / config file to generate in rulRunner
            "status":"FINISHED",
            "probabilityOfFailure": probabilityOfFailure,
            "RULUnit": rulUnit,
            "RULValue": rulValue,
            "ConfidenceInterval": ConfidenceInterval,
            "runnerId":runnerId #TODO config file to generate in rulRunner
            }

        token=self.__getKCToken(secret)
        print(token)

        json_dump = json.dumps(payload)

        headers={"Content-Type":"application/json","Authorization":"Bearer "+token}

        r=requests.post(self.OUTPUT_URL,headers=headers,data=json_dump)
        #TODO Esta fallando esta llamada pq la api de mngtools está boqueada hasta que termine el script

        return (r.text)

    def __getKCToken(self,secret):
       
        url = self.KC_TOKEN_URL
        payload = {
            "client_id": self.CLIENT_ID ,
            "grant_type": "client_credentials" ,
            "client_secret":secret}

        r=requests.post(url,data=payload)
        res=json.loads(r.text)   
        return (res['access_token'])
    

        
    def __getClientSecret(self):
       
        secret="Secret Not Found"        
       
        with open(self.DIR_BASE+'secret') as file:
            secret=file.read() 
        return secret

    def __getRulRunnerId(self):
        with open(self.DIR_BASE+self.METADATA_FILE) as file:
            self.metadata = json.load(file)
            self.rulRunner=self.metadata['rulRunner']       
        return self.rulRunner