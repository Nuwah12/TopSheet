Keep a log of important jobs on your Linux/Unix server in a convenient Google Sheet. 

#### Google OAuth Setup:
First, make sure you have navigated to The [Google Cloud Console Homepage](https://console.cloud.google.com/) and created a project with a unique name. 

1. Click "APIs and Servces" > "Enabled APIs and Services" > "+ Enable APIs and services"
2. Search for and enable both "Google Drive API" and "Google Sheets API"
3. Click on "Oauth concent screen" on the left sidebar and fill out the required information, then click "Create OAuth Screen"
4. Once you click "create" **make sure to download the Client and Secret ID to your local machine** via the `Download JSON` button in the lower left.
5. Rename this file to `credentials.json` and place it in `~/.config/gspread/` on the machine yo want to monitor

#### Application Setup
TBA
