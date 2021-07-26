# F20-54-D-ContractDrafter

Contract Drafter is an android native based application for the short meetings of property dealing. The android app provides a feature of conference call within a particular group of participants. The admin starts recording a video & saves it DropBox. The other end i.e. Python script with a trained model & a script which fetches a video stream from DropBox & pass it to an ASR. The ASR transcribes the video stream into an Urdu text. The text of whole meeting gets store into a text file. The other model which is a summarization model summarizes the text & generates a contract draft.

1- The Repository contains a trained model/script of on ASR.

2- Find Android Video Conference calling app on the link below.

https://github.com/Jahanzaib523/Contract-Drafter.git

3- The DropboxAPI.py file is a Dropbox API to upload, list & download files from/to the dropbox.

