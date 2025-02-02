import unittest
from os import path, getenv
from google.cloud import bigquery
import googleapiclient.discovery
from google.oauth2 import service_account
from gfluent import Sheet
from gfluent import BQ

_GOOGLESERVICE = googleapiclient.discovery.Resource

SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
]

# use the standard Google key file variable
SA_PATH = getenv("GOOGLE_APPLICATION_CREDENTIALS")
SHEET_ID = "a-look-like-sheet-id-string"
SHEET_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/"
googleSheetType = googleapiclient.http.HttpRequest


class TestSheet(unittest.TestCase):
    def test_init_with_sa_path(self):
        sheet = Sheet(SA_PATH)
        self.assertEqual(_GOOGLESERVICE, sheet._service.__class__)

    def test_init_with_cred(self):
        cred = service_account.Credentials.from_service_account_file(
            SA_PATH, scopes=SCOPES)
        sheet = Sheet(cred)
        self.assertEqual(_GOOGLESERVICE, sheet._service.__class__)

    def test_sheet_id_keyword(self):
        sheet = Sheet(SA_PATH).sheet_id(SHEET_ID)
        self.assertEqual(sheet._sheet_id, SHEET_ID)

    def test_sheet_url(self):
        sheet = Sheet(SA_PATH).url(SHEET_URL)
        self.assertEqual(sheet._sheet_id, SHEET_ID)

    def test_worksheet_keyword(self):

        sheet = Sheet(SA_PATH).sheet_id(SHEET_ID).worksheet("Sheet1")
        self.assertEqual(sheet._worksheet, "Sheet1")

    def test_range_keyword(self):

        sheet = Sheet(SA_PATH).sheet_id(
            SHEET_ID).worksheet("Sheet1").range("A:C")
        self.assertEqual(sheet._range, "A:C")

    def test_with_kwargs(self):
        bq_project = 'here-is-project-id'
        table = "dataset.table"
        bq = BQ(bq_project, table=table)
        sheet = Sheet(SA_PATH,
                      sheet_id=SHEET_ID,
                      worksheet="Sheet1",
                      range="A:C",
                      bq=bq
                      )
        self.assertEqual(sheet._sheet_id, SHEET_ID)
        self.assertEqual(sheet._worksheet, "Sheet1")
        self.assertEqual(sheet._range, "A:C")
        self.assertEqual(bq._table, table)

    def test_call_range_first_exception(self):
        sheet = Sheet(SA_PATH).sheet_id(SHEET_ID)
        with self.assertRaises(ValueError):
            sheet.range("B3:B8")

    def test_twice_range_exception(self):
        sheet = Sheet(SA_PATH).sheet_id(SHEET_ID).worksheet("Sheet1!A2:C6")
        with self.assertRaises(ValueError):
            sheet.range("B3:B8")


    def test_invalid_sheet_id(self):
        with self.assertRaises(TypeError):
            _ = Sheet(SA_PATH).sheet_id(123)

        with self.assertRaises(ValueError):
            _ = Sheet(SA_PATH).worksheet("132")

        with self.assertRaises(ValueError):
            _ = Sheet(SA_PATH).sheet_id(SHEET_ID).range("A:C")

        with self.assertRaises(TypeError):
            _ = Sheet(SA_PATH,
                      sheet_id=SHEET_ID,
                      worksheet="Sheet1",
                      bq="bq"
                      )
