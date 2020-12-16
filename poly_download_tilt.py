import requests
import os, sys
import json
import wget

API_KEY = os.environ.get('POLY_API_KEY')

def main():
    if len(sys.argv) <= 2:
        sys.exit("Usage: python poly_download_tilt.py <assetID> <download_filename>")
    
    assetID = sys.argv[1]
    filename = sys.argv[2]
    
    response = requests.get("https://poly.googleapis.com/v1/assets/" + assetID + "/?key=" + API_KEY)
    
    if (response.ok != True):
        print("Unsuccessful! Response code " + str(response.status_code) + ".")
        exit()
    
    response = response.json()
    
    for format in response['formats']:
        if (format['formatType']=="TILT"):
            url = format['root']['url']
            print("Downloading " + url + "...")
            filename = wget.download(url, out=os.path.join("./models/", filename + "_" + assetID + ".tilt"))
            exit()
    
    print("Unsuccessful! No TILT file found.")

    
if __name__ == '__main__':
    main()