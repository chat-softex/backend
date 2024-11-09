# app/service/firebase_service.py:
import firebase_admin
from firebase_admin import credentials, storage
import os

# Inicializa o aplicativo Firebase com as credenciais e o bucket configurados no .env
cred = credentials.Certificate(os.getenv('FIREBASE_CONFIG'))
firebase_admin.initialize_app(cred, {'storageBucket': os.getenv('STORAGE_BUCKET')})

class FirebaseService:
    @staticmethod
    def upload_file(file_path, file_name):
        bucket = storage.bucket()
        blob = bucket.blob(file_name)
        blob.upload_from_filename(file_path)
        # blob.make_public()  # Torna o arquivo público
        return blob.public_url

    @staticmethod
    def download_file(file_name, destination):
        bucket = storage.bucket()
        blob = bucket.blob(file_name)
        blob.download_to_filename(destination)
