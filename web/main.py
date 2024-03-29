from __future__ import print_function
import pickle
import os.path
import io
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from apiclient.http import MediaFileUpload, MediaIoBaseDownload
from pyfiglet import Figlet
from io import BytesIO



import auth


SCOPES = 'https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE = 'client_secret.json'

authInst = auth.auth(SCOPES,CLIENT_SECRET_FILE)
service = authInst.getAuth()
f = Figlet(font='starwars')


cwd = os.getcwd()
filepath = os.path.join(cwd,'sample','sample.jpg')
downLoadPath = os.path.join(cwd,'downloads')
mimetype = 'image/jpeg'

mime_types= {
        "xls" :"application/vnd.ms-excel",
        "xlsx" :"application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "xml" :"text/xml",
        "ods":"application/vnd.oasis.opendocument.spreadsheet",
        "csv":"text/plain",
        "tmpl":"text/plain",
        "pdf": "application/pdf",
        "php":"application/x-httpd-php",
        "jpg":"image/jpeg",
        "png":"image/png",
        "gif":"image/gif",
        "bmp":"image/bmp",
        "txt":"text/plain",
        "doc":"applicat# ion/msword",
        "js":"text/js",
        "swf":"application/x-shockwave-flash",
        "mp3":"audio/mpeg",
        "zip":"application/zip",
        "rar":"application/rar",
        "tar":"application/tar",
        "arj":"application/arj",
        "cab":"application/cab",
        "html":"text/html",
        "htm":"text/html",
        "default":"application/octet-stream",
        "folder":"application/vnd.google-apps.folder"
        }


def getFileList(pagesize,service=service):
    try:
        if pagesize >= 1:
            results = service.files().list(
                            pageSize=pagesize, fields="nextPageToken, files(id, name)").execute()
            items = results.get('files', [])
            if not items:
                print('No files found.')
            else:
                print('Files:')
                for item in items:
                    print(u'{0}--------({1})'.format(item['id'], item['name']))
        elif pagesize <= 0:
            raise ValueError('Please select a non-zero value greater than 1')
    except ValueError:
        print("Invalid value. Values must be within the range: [1, 1000]")



def getContent(pagesize,service=service):

    try:
        if pagesize >= 1:
            results = service.files().list(
                            pageSize=pagesize, fields="nextPageToken, files(id, name)").execute()
            items = results.get('files', [])
            if not items:
                print('No files found.')
            else:
                print('Files:')
                for item in items:
                    print(u'{0}--------({1})'.format(item['id'], item['name']))
        elif pagesize <= 0:
            raise ValueError('Please select a non-zero value greater than 1')
    except ValueError:
        print("ValueError Raised:Values must be within the range: [1, 1000]")

    anyKey = input("Press any key to continue!")
    os.system('clear')
    menuCLI()

def uploadFile(filename,filepath,mimetype,service=service):
    try:
        if mimetype and (mimetype in mime_types.values()):
            file_metadata = {'name': filename}
            media = MediaFileUpload(filepath,
                                    mimetype=mimetype)
            file = service.files().create(body=file_metadata,
                                                media_body=media,
                                                fields='id').execute()
            print('File ID: %s' % file.get('id'))
        else:
            raise TypeError('Invalid or Missing MIMETYPE')
    except TypeError:
        print("Invalid or Missing MIMETYPE")

    anyKey = input("Press any key to continue!")
    os.system('clear')
    menuCLI()

def downLoadFile(id,filepath,service=service):
    file_id = id
    request = service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download %d%%." % int(status.progress() * 100))
    with io.open(filepath,'wb') as f:
        fh.seek(0)
        f.write(fh.read())

    anyKey = input("Press any key to continue!")
    os.system('clear')
    menuCLI()

def downLoadAllFiles(service=service):
    results = service.files().list(
                    pageSize=100, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])

    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print(u'{0}--------({1})'.format(item['id'], item['name']))
            request = service.files().get_media(fileId=item['id'])
            fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                print("Download %d%%." % int(status.progress() * 100))
            with io.open(os.path.join(downLoadPath,item['name']),'wb') as f:
                fh.seek(0)
                f.write(fh.read())

    anyKey = input("Press any key to continue!")
    os.system('clear')
    menuCLI()



def menuCLI():
    # print(header)
    print(f.renderText('Google Drive'))
    print("1. List all files in the drive")
    print("2. Upload a file to the drive")
    print("3. Download a file from the drive")
    print("4. Downlaod all files from the drive")
    print("5. Quit")

    while True:
        try:
            choice=int(input("Enter your choice : "))

            if choice == 1:
                pagesize = int(input("Enter the number of files you want to view. (1 - 100) : "))
                getContent(pagesize,service)
                break

            elif choice == 2:
                filename = input("Enter the name you want to give your file : ")
                print("\nWe need to know the type of document you are uploading\n")


                """
                    Display the list of MIMETYPES supported by Google Drive ,
                    uploadFile() needs the mimetype argument to upload the file
                    into the google drive
                """

                print("Generating the list of mimetype,\n\n Please select the relevant one ")
                for k, v in mime_types.items():
                    print(k, '>', v)
                print("\n\n")
                mimetype = input("We need the know the type of document you are uploading : ")


                uploadFile(filename,filepath,mimetype,service)
                break

            elif choice == 3:
                print("We need the file Id to upload to drive ")
                pagesize = int(input("Enter the number of files you want to view. (1 - 100) : "))
                getFileList(pagesize,service)

                fileid = input("Enter the file id that you want to download : ")
                filename = input("Enter the name that you want the file to be saved as with extension (.jpeg,.doc,.pdf)")
                downLoadFile(fileid,os.path.join(downLoadPath,filename),service)
                break

            elif choice == 4:
                downLoadAllFiles(service)
                break

            elif choice == 5:
                break
            else:
                print("Invalid Choice. Enter 1-5 : ")
                menuCLI()
        except ValueError:
            print("Incorrect input, Please try again\n ")
        except EOFError:
            print("EOF Error in Menu")

    exit

if __name__ == '__main__':
    menuCLI()
