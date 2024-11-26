# app/service/firebase_service.py:
import firebase_admin
from firebase_admin import credentials, storage, exceptions
import os
import logging
from app.erros.custom_errors import InternalServerError, ExternalAPIError

# Configuração de logging
logger = logging.getLogger(__name__)

# Inicializa o aplicativo Firebase com as credenciais e o bucket configurados no .env
cred = credentials.Certificate(os.getenv('FIREBASE_CONFIG'))
firebase_admin.initialize_app(cred, {'storageBucket': os.getenv('STORAGE_BUCKET')})

class FirebaseService:
    
    @staticmethod
    def upload_file(file_path, file_name):
        try:
            bucket = storage.bucket()
            if not bucket.exists():
                raise exceptions.NotFoundError("O bucket especificado não existe.")

            blob = bucket.blob(file_name)
            blob.upload_from_filename(file_path)
            blob.make_public()  # Torna o arquivo público
            logger.info(f"Arquivo '{file_name}' enviado com sucesso. URL: {blob.public_url}")
            return blob.public_url

        except exceptions.NotFoundError as e:
            logger.error(f"Bucket não encontrado para o arquivo '{file_name}'. Detalhes: {e}")
            raise ExternalAPIError(service="Firebase", message="Bucket não encontrado.") from e

        except exceptions.PermissionDeniedError as e:
            logger.error(f"Permissão negada para acessar o bucket ao enviar '{file_name}'. Detalhes: {e}")
            raise ExternalAPIError(service="Firebase", message="Permissão negada.") from e

        except exceptions.FirebaseError as e:
            logger.error(f"Erro geral do Firebase ao enviar '{file_name}'. Detalhes: {e}")
            raise ExternalAPIError(service="Firebase", message=f"Erro do Firebase: {e}") from e

        except Exception as e:
            logger.error(f"Erro inesperado ao fazer upload do arquivo '{file_name}'. Detalhes: {e}")
            raise InternalServerError("Erro inesperado ao fazer upload do arquivo.") from e


    @staticmethod
    def download_file(file_name, destination):
        try:
            bucket = storage.bucket()
            if not bucket.exists():
                raise exceptions.NotFoundError("O bucket especificado não existe.")

            blob = bucket.blob(file_name)
            blob.download_to_filename(destination)

        except exceptions.NotFoundError as e:
            logger.error(f"Bucket não encontrado para o arquivo '{file_name}'. Detalhes: {e}")
            raise ExternalAPIError(service="Firebase", message="Bucket não encontrado.") from e

        except exceptions.PermissionDeniedError as e:
            logger.error(f"Permissão negada para acessar o bucket ao enviar '{file_name}'. Detalhes: {e}")
            raise ExternalAPIError(service="Firebase", message="Permissão negada.") from e

        except exceptions.FirebaseError as e:
            logger.error(f"Erro geral do Firebase ao enviar '{file_name}'. Detalhes: {e}")
            raise ExternalAPIError(service="Firebase", message=f"Erro do Firebase: {e}") from e

        except Exception as e:
            logger.error(f"Erro inesperado ao fazer upload do arquivo '{file_name}'. Detalhes: {e}")
            raise InternalServerError("Erro inesperado ao fazer upload do arquivo.") from e    
