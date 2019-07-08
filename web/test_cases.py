import unittest

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
import main



SCOPES = 'https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE = 'client_secret.json'

authInst = auth.auth(SCOPES,CLIENT_SECRET_FILE)
service = authInst.getAuth()

cwd = os.getcwd()
filepath=os.path.join(cwd,'sample','sample.jpg')
downLoadPath = cwd+'/downloads'
# mimetype = 'image/jpeg'

class TestServices(unittest.TestCase):

    def test_getContent_str_negative(self):
        with self.assertRaises(ValueError):
            # case 1 - test_getContent takes a str, 0 or negativeinput for pagesize and it should raise a value error

            main.getContent('sdad', service)
            main.getContent(0, service)



            # Case 2 - MIMETYPE value Error
    def test_upLoadFile_MIME(self):
        with self.assertRaises(ValueError):
            main.uploadFile("",filepath,'image.jpeg',service)
            main.uploadFile("",filepath,'image/jpeg',service)











if __name__ == '__main__':
    unittest.main()
