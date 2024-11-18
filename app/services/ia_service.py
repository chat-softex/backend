# app/service/ia_service.py:
import openai
import os
import time
import logging
from app.services.projeto_service import ProjectService
from app.utils.text_extractor import TextExtractor
from app.erros.custom_errors import NotFoundError, ValidationError, InternalServerError

openai.api_key = os.environ.get('OPENAI_KEY')
logger = logging.getLogger(__name__)

class IaService:
    PONTOS_ANALISE = [
        "Viabilidade técnica",
        "Potencial de inovação",
        "Impacto no mercado",
        "Sustentabilidade do projeto",
        "Escalabilidade"
    ]
    MAX_RETRIES = 3

    def __init__(self, projeto_service=ProjectService()):
        self.projeto_service = projeto_service

    def obter_texto_projeto(self, project_id):
        """Obtém e extrai o texto do arquivo do projeto para análise."""
        projeto = self.projeto_service.get_by_id(project_id)
        if not projeto:
            logger.warning(f"Projeto com ID {project_id} não encontrado.")
            raise NotFoundError("Projeto", "Projeto não encontrado")
        
        # extrai o texto com base no tipo de arquivo (PDF, DOC ou DOCX)
        file_content = projeto.arquivo.read()  
        if projeto.arquivo.name.endswith('.pdf'):
            texto = TextExtractor.extract_text_pdf(file_content)
        elif projeto.arquivo.name.endswith(('.doc', '.docx')):
            texto = TextExtractor.extract_text_docx(file_content)
        else:
            raise ValidationError("arquivo", "Tipo de arquivo não suportado para análise.")
        
        if not texto:
            raise ValidationError("arquivo", "O arquivo do projeto não contém texto válido para análise.")
        
        return texto

    def enviar_para_analise(self, projeto_texto):
        """Envia o texto do projeto para a API do ChatGPT para avaliação."""
        for attempt in range(self.MAX_RETRIES):
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-4",  
                    messages=[
                        {"role": "system", "content": "Você é um assistente especializado em avaliar projetos de inovação tecnológica."},
                        {"role": "user", "content": f"Texto do projeto para análise:\n\n{projeto_texto}\n\nPontos a serem analisados:\n- " + "\n- ".join(self.PONTOS_ANALISE)}
                    ],
                    max_tokens=4600
                )
                logger.info("Análise realizada com sucesso pela API da OpenAI.")
                return response.choices[0].message["content"]
            except openai.error.OpenAIError as e:
                logger.error(f"Erro ao acessar a API da OpenAI: {e}")
                if attempt < self.MAX_RETRIES - 1:
                    logger.info("Tentando novamente em 60 segundos...")
                    time.sleep(60)
                else:
                    logger.error("Número máximo de tentativas atingido. Não foi possível concluir a análise.")
                    raise InternalServerError("Erro ao acessar o serviço de IA para análise do projeto.")
            except Exception as e:
                logger.error(f"Erro inesperado ao acessar a API: {e}")
                raise InternalServerError("Erro inesperado ao acessar o serviço de IA.")

    # def avaliar_projeto(self, project_id):
    #     """Realiza a análise do projeto a partir de seu ID."""
    #     try:
    #         projeto_texto = self.obter_texto_projeto(project_id)
    #         logger.info(f"Iniciando análise para o projeto ID {project_id}.")
    #         resultado_analise = self.enviar_para_analise(projeto_texto)
    #         return resultado_analise
    #     except NotFoundError as e:
    #         raise e
    #     except ValidationError as e:
    #         raise e
    #     except Exception as e:
    #         logger.error(f"Erro ao avaliar projeto {project_id}: {e}")
    #         raise InternalServerError("Erro ao avaliar o projeto.")
