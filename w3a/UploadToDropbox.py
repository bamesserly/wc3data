#!/usr/bin/env python
# -*- coding: utf-8 -*-

from transferdata import TransferData
from Utils        import top
from time import sleep 

def UploadToDropbox(spreadsheet_file):
  print "Entering UploadToDropbox()"
  access_token = 'BJfeECR3F-AAAAAAAAAACfdM5D9QFy0fITmIYyAn_hC7qTWfEBH-rJ_1RrTN5gaL'	# get your access token from Dropbox Developers
  transferData = TransferData(access_token)

  file_from = top + spreadsheet_file
  file_to   = spreadsheet_file	# The full path to upload the file to, including the file name
  
  # API v1
  transferData.upload_file_v1(file_from=file_from, file_to=file_to)

  print "Exiting UploadToDropbox()"

if __name__ == '__main__':
  UploadToDropbox()
