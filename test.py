import unittest

from ftplib import FTP

class TestFtp(unittest.TestCase):
    """
    A class with test cases for ftp-server
    """
    def setUp(self):
        self.ftp = FTP('speedtest.tele2.net')
    
    def tearDown(self):
        self.ftp.quit()

    def test_authorisation(self):
        """
        Tests authorization on the server.
        Test case ID: 1
        """
        connect_answer = self.ftp.connect()
        self.assertEqual(connect_answer, '220 (vsFTPd 3.0.3)')

        login_answer = self.ftp.login('anonymous', 'anonymous')

        self.assertEqual(login_answer, '230 Login successful.')

    def test_fixed_list(self):
        """
        Tests a fixed list of contents.
        Test case ID: 2
        """
        self.ftp.connect()
        self.ftp.login('anonymous', 'anonymous')

        expected_list = ['1000GB.zip', '100GB.zip', '100KB.zip', 
                     '100MB.zip', '10GB.zip', '10MB.zip', '1GB.zip', 
                     '1KB.zip', '1MB.zip', '200MB.zip', '20MB.zip', 
                     '2MB.zip', '3MB.zip', '500MB.zip', '50GB.zip', 
                     '50MB.zip', '512KB.zip', '5MB.zip', 'upload' ]

        actual_list = self.ftp.nlst()

        self.assertEqual(expected_list.sort(), actual_list.sort())

    def test__download(self):
        """
        Tests a file download from server.
        Test case ID: 3
        """

        self.ftp.connect()
        self.ftp.login('anonymous', 'anonymous')

        out = '5MB.zip'
        with open(out, 'wb') as f:
            download_answer = self.ftp.retrbinary('RETR ' + '5MB.zip', f.write)

        self.assertEqual(download_answer, '226 Transfer complete.')

    def test_upload(self):
        """
        Tests a file upload to server.
        Test case ID: 4
        """
        self.ftp.connect()
        self.ftp.login('anonymous', 'anonymous')

        cd_answer = self.ftp.cwd('upload')
        self.assertEqual(cd_answer, '250 Directory successfully changed.')

        with open('5MB.zip', 'rb') as f:
            send_answer = self.ftp.storbinary('STOR 5MB.zip', f)
        self.assertEqual(send_answer, '226 Transfer complete.')

        actual_list = self.ftp.nlst()
        self.assertNotIn('5MB.zip', actual_list)

    def test_root_upload(self):
        """
        Tests a file upload to root folder server.
        Test case ID: 5
        """
        self.ftp.connect()
        self.ftp.login('anonymous', 'anonymous')

        with open('5MB.zip', 'rb') as f:
            try:
                self.ftp.storbinary('STOR 5MB.zip', f)
            except Exception as ex:
                self.assertEqual(str(ex), '553 Could not create file.')

    def test_download_upload_folder(self):
        """
        Tests a download 'upload' folder from server.
        Test case ID: 6
        """

        self.ftp.connect()
        self.ftp.login('anonymous', 'anonymous')

        out = 'upload'
        with open(out, 'wb') as f:
            try:
                self.ftp.retrbinary('RETR ' + 'upload', f.write)
            except Exception as ex:
                self.assertEqual(str(ex), '550 Failed to open file.')

if __name__ == '__main__':
    unittest.main(warnings='ignore')