import requests
import json
from datetime import datetime
import os, glob


def writeToFile(data_path, case, certanity="LOW"):
    '''Write key - value pairs to file, 

        key TAB value

        Parameters:
        --------------------
        data_path (str) : The path to where case data files are being stored
        case (dict) : A json representation of case
        certanity (str) : determines certanity - based on condition tested before function call.

        Return: None
    '''    
    drugs = case['drugs']
    drugs_inline_string = ""
    for drug in drugs:
        drugs_inline_string += drug['name'] + ", "
    
    date_sync = datetime.utcnow().strftime("%Y-%m-%d %H-%M-%S")

    with open(f"{data_path}\CIVIC_EVIDENCE_{[case['id']]}.tsv", 'w') as f:
                f.write(f"Id\t{str(case['id'])}\n" + 
                        f"VARIANT_NAME\t{(case['variant'])['name']}\n" +
                        f"GENE_NAME\t{(case['gene'])['name']}\n" +
                        f"EVIDENCE_RATING\t{case['evidenceRating']}\n" +
                        f"EVIDENCE_LEVEL\t{case['evidenceLevel']}\n" +
                        f"CERTANITY\t{certanity}\n" +
                        f"DISEASE_NAME\t{(case['disease'])['name']}\n" +
                        f"DRUG_NAMES\t{drugs_inline_string}\n" +
                        f"SOURCE_SOURCE_TYPE\t{(case['source'])['sourceType']}\n" +
                        f"DATE_SYNCHRONIZED\t{date_sync}")
                        
def readJsonFromFile(path):
    '''
        Read data from example json file, provided with the test.

        Parameters:
        --------------------
        path (str) : The path to the json file.

        Return: Data (dict) : All cases found in file.
    '''
    with open(path, "r") as f:
        data = json.load(f)
        data = ( ( data['data'] )['evidenceItems'] )['nodes']
        return data

def readFromJsonPayload(path):
    '''
        Reads the required payload for query with CIViC API, as json.

        Parameters:
        --------------------
        path (str) : The path to payload.json
    '''
    with open(path, 'r') as f:
        return json.load(f)

def printFromTsvFile(path):
    '''Prints the contents from a case file to the console'''
    with open(path, "r") as f:
        print(os.path.join(path))
        print("- - - - - - - - - - - - - - - - - - - -\n")
        for line in f.readlines():
            print(line)
        print("- - - - - - - - - - - - - - - - - - - -\n\n")

def getDataFromApi(api_path, json_path):
    '''
        Make a post request to the CIViC API.

        Parameters:
        --------------------
        api_path (str) : The path to the API endpoint
        json_path (str) : The path to the payload for the post request

        Return: data (dict) : All found cases represented as a dictionary.

    '''
    jsonPayload = readFromJsonPayload(json_path)
    data = requests.post(api_path, json=jsonPayload)
    data = data.json()
    data = ( ( data['data'] )['evidenceItems'] )['nodes']
    return data



# Run this code if this file is run directly.
if __name__ == "__main__":
    # path to directories and neccessary json files.
    current_directory_path = os.getcwd()
    data_path = rf"{current_directory_path}\data"
    json_path = rf"{current_directory_path}\json"
    json_data_sample_path = rf"{json_path}\data.json"
    json_payload_path = rf"{json_path}\payload.json"

    # Data read from test data provided in the assignment.
    data = readJsonFromFile(json_data_sample_path)

    # Writing test data to file.
    for case in data:
        if (case['evidenceRating'] >= 4 and case['evidenceLevel'] == 'A'):
          writeToFile(data_path, case, "HIGH")
        else:
            writeToFile(data_path, case)

    # Printing data from the files created from earlier to console
    os.chdir(data_path)
    for file in glob.glob("*.tsv"):
        printFromTsvFile(file)
    
    # Getting data from API endpoint.
    api_path = r"https://civicdb.org/api/graphql"
    api_data = getDataFromApi(api_path, json_payload_path)
    
    # Writing to file the data returned from the API call.
    for case in api_data:
        if (case['evidenceRating'] >= 4 and case['evidenceLevel'] == 'A'):
          writeToFile(data_path, case, "HIGH")
        else:
            writeToFile(data_path, case)
