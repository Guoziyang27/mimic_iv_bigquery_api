from google_auth_oauthlib import flow

from google.cloud import bigquery

BigQuery_client = []

def connect():
    global BigQuery_client
    launch_browser = False

    appflow = flow.InstalledAppFlow.from_client_secrets_file(
        "./client_secret.json", scopes=["https://www.googleapis.com/auth/bigquery"]
    )

    if launch_browser:
        appflow.run_local_server()
    else:
        appflow.run_console()

    credentials = appflow.credentials

    project = 'rebuilt-mimic-iv'

    BigQuery_client.append(bigquery.Client(project=project, credentials=credentials))
    print(BigQuery_client is None)