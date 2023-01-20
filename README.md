# Speech Recognition with Azure Cognitive Services
----------
![alt](./image.png)

## Project description
This project is a simple speech recognition application that uses Azure Cognitive Services to convert speech to text and save the text to a Notion Databse. The application is built using the Python, the Azure Speech SDK and NOTION API. 

## You'll need
- Python 3.8
- Azure Cognitive Services
- Notion API
- Streamlit

## How to use
1. Clone the repository
2. Create a Notion Database and get the database ID
3. Create a Notion API key and get the API key
4. Create an Azure Cognitive Services resource and get the API key
5. Create a .env file and add the following variables
    - NOTION_DATABASE_ID
    - NOTION_API_KEY
    - AZURE_SPEECH_KEY
    - AZURE_SPEECH_REGION
6. Run the application
## Screenshots
The application is built using Streamlit. The application has a simple UI that allows you to record your speech and save it to a Notion Database. The application also allows you to view the text that has been saved to the Notion Database.
![alt](./screenshot.png)