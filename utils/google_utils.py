from dotenv import load_dotenv, find_dotenv
from typing import Optional
import os
from numpy import nan
import gspread
import gspread_dataframe as gd
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from oauth2client.service_account import ServiceAccountCredentials

_ = load_dotenv(find_dotenv())


DEFALUT_SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive',
]


DEFAULT_CREDENTIALS = {
  "type": "service_account",
  "project_id": os.getenv("PROJECT_NAME"),
  "private_key_id": os.getenv("PRIVATE_KEY_ID"),
  "private_key": os.getenv("PRIVATE_KEY"),
  "client_email": os.getenv("CLIENT_EMAIL"),
  "client_id": os.getenv("CLIENT_ID"),
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": os.getenv("CLIENT_CERT_URL"),
  "universe_domain": "googleapis.com"
}


def load_credentials(credentials_path: Optional[str] = None, scopes: list = DEFALUT_SCOPES) -> ServiceAccountCredentials:
    """
    Initialize credentials for the service account.
    :param scopes: scopes to request
    :return: credentials
    """
    if credentials_path is not None:
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            'credentials.json', scopes=scopes)
    else:
        credentials = ServiceAccountCredentials.from_json_keyfile_dict(DEFAULT_CREDENTIALS)
    return credentials


def initialize_sheet_service(credentials: ServiceAccountCredentials) -> gspread.service.GspreadService:
    """
    Initialize the sheet service.
    :param credentials: credentials
    :return: sheet service
    """
    return gspread.authorize(credentials)


def initialize_drive_service(credentials: ServiceAccountCredentials) -> gspread.service.GspreadService:
    """
    Initialize the drive service.
    :param credentials: credentials
    :return: drive service
    """
    return build('drive', 'v3', credentials=credentials)


def list_files_in_drive_folder(drive_service, folder_id):
    results = drive_service.files().list(
        q=f"'{folder_id}' in parents",
        pageSize=1000,
        fields="nextPageToken, files(id, name, mimeType)"
    ).execute()

    items = results.get('files', [])
    return items


def upload_image_and_get_image_formula(drive_service, folder_id, image, image_id=None):
    """
    Upload an image to Google Drive and return the direct link to the image file.
    The impage formula will be used to make the image visible to google sheet user.
    folder_id: The drive folder store the transformed temp image.
    """
    # Save the image to a temporary file and upload it to Google Drive
    if not image:
        return nan
    temp_filename = 'temp_image.jpg' if image_id is None else f'temp_image_{image_id}.jpg'
    image.save(temp_filename)

    file_metadata = {'name': temp_filename, 'parents': [folder_id]}
    media = MediaFileUpload(temp_filename, mimetype='image/jpeg')
    file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    
    # Change the permissions to allow anyone with the link to view the file
    permission = {'type': 'anyone','role': 'reader'}
    drive_service.permissions().create(fileId=file['id'], body=permission).execute()
    
    # Get the direct link to the image file
    file = drive_service.files().get(fileId=file['id'], fields='webContentLink').execute()
    image_url = file['webContentLink']
    
    # Get the IMAGE function string with the direct link to the uploaded image
    image_formula = f'=IMAGE("{image_url}")'

    return image_formula


def read_data_from_sheet(googe_service, spreadsheet_id, sheet_name, as_df=False):
    # Open google sheet given the spreadsheet id and sheet name
    spreadsheet = googe_service.open_by_key(spreadsheet_id)
    worksheet = spreadsheet.worksheet(sheet_name)

    # Read the data from the sheet
    if as_df:
        return gd.get_as_dataframe(worksheet)
    return worksheet.get_all_values()


def write_dataframe_to_sheet(googe_service, spreadsheet_id, sheet_name, df):
    # Open google sheet given the spreadsheet id and sheet name
    spreadsheet = googe_service.open_by_key(spreadsheet_id)
    worksheet = spreadsheet.worksheet(sheet_name)

    # Find the number of rows of existing data
    existing_rows = len(worksheet.get_all_values())
    include_column_header = existing_rows == 0

    # Append to the sheet if with existing data without header
    gd.set_with_dataframe(worksheet, df, row=existing_rows+1, include_column_header=include_column_header)
    return