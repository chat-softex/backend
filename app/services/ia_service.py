import openai
import requests
from io import BytesIO
import os
import time
import logging
from app.repositories.projeto_repository import ProjectRepository
from app.utils.text_extractor import TextExtractor
from app.erros.custom_errors import NotFoundError, ValidationError, InternalServerError, ExternalAPIError

openai.api_key = os.environ.get('OPENAI_KEY')
logger = logging.getLogger(__name__)

class IaService:
    PONTOS_ANALISE = [
        "Mérito da Inovação",
        "Originalidade",
        "Relevância",
        "Aplicabilidade",
        "Viabilidade técnica",
        "Potencial de inovação",
        "Impacto no mercado",
        "Sustentabilidade do projeto",
        "Escalabilidade",
        "Barreiras de Risco",
        "Engajamento da Empresa",
        "Enquadramento em atividades de PD&I: Pesquisa Básica (PB), Pesquisa Aplicada (PA) ou Desenvolvimento Experimental (DE), ou não se enquadra em nenhuma atividade de PD&I",
        "Natureza das Atividades de PD&I (Produto, Processo ou Serviço) do projeto",
        "É destacado os elementos tecnologicamente novo ou inovador da atividade?"
        "São explicitados os objetivos do projeto?",
        "Descreve explicitamente Resultado Econômico e Resultado de Inovação esperados?",
        "Existe outros projetos de inovação tecnológica semelhantes?",
        "O projeto se enquadra na Lei do Bem (Lei federal nº 11.196 de 21 de novembro de 2005)? E por que?",
        "Recomendações de melhoria"
    ]
    MAX_RETRIES = 3

    def __init__(self, projeto_repository=ProjectRepository()):
        self.projeto_repository = projeto_repository

    def obter_texto_projeto(self, project_id):
        """Obtém e extrai o texto do arquivo do projeto para análise."""
        projeto = self.projeto_repository.get_by_id(project_id)
        if not projeto:
            logger.warning(f"Projeto com ID {project_id} não encontrado.")
            raise NotFoundError("Projeto", "Projeto não encontrado")
        
        if not projeto.arquivo or not isinstance(projeto.arquivo, str):
            logger.error(f"O caminho do arquivo é inválido para o projeto {project_id}.")
            raise ValidationError("arquivo", "Caminho do arquivo inválido.")
        
        try:
            response = requests.get(projeto.arquivo)
            if response.status_code != 200:
                logger.error(f"Erro ao baixar o arquivo: {response.status_code}")
                raise ValidationError("arquivo", "Não foi possível baixar o arquivo do projeto.")

            file_content = BytesIO(response.content)  

            if projeto.arquivo.endswith('.pdf'):
                file_type = "pdf"
            elif projeto.arquivo.endswith(('.doc', '.docx')):
                file_type = "docx"
            else:
                logger.error(f"Tipo de arquivo não suportado: {projeto.arquivo}")
                raise ValidationError("arquivo", "Tipo de arquivo não suportado para análise.")
            
            texto = TextExtractor.extract_text(file_content.read(), file_type)

            if not texto.strip():
                logger.error(f"O arquivo do projeto {project_id} não contém texto válido.")
                raise ValidationError("arquivo", "O arquivo do projeto não contém texto válido para análise.")
            
            logger.info(f"Texto extraído com sucesso para o projeto ID {project_id}.")
            return texto

        except requests.exceptions.RequestException as e:
            logger.error(f"Erro ao acessar o arquivo do projeto: {e}")
            raise ValidationError("arquivo", "Erro ao acessar o arquivo do projeto.")
        except ValidationError:
            raise  
        except Exception as e:
            logger.error(f"Erro ao processar o arquivo do projeto {project_id}: {e}")
            raise InternalServerError("Erro ao processar o arquivo do projeto.")

    def enviar_para_analise(self, projeto_texto):
        """Envia o texto do projeto para a API do ChatGPT para avaliação."""
        for attempt in range(self.MAX_RETRIES):
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",  
                    messages=[
                        {"role": "system", "content": "Você é um assistente especializado em avaliar projetos de inovação tecnológica."},
                        {"role": "user", "content": f"Texto do projeto para análise:\n\n{projeto_texto}\n\nPontos a serem analisados:\n- " + "\n- ".join(self.PONTOS_ANALISE)}
                    ],
                    max_tokens=4000
                )
                logger.info("Análise realizada com sucesso pela API da OpenAI.")
                return response.choices[0].message["content"]
            except openai.error.OpenAIError as e:
                logger.error(f"Erro ao acessar a API da OpenAI: {e}")
                if attempt < self.MAX_RETRIES - 1:
                    logger.info("Tentando novamente em 60 segundos...")
                    time.sleep(30)
                else:
                    logger.error("Número máximo de tentativas atingido. Não foi possível concluir a análise.")
                    raise ExternalAPIError(service="OpenAI", message=str(e))
            except Exception as e:
                logger.error(f"Erro inesperado ao acessar a API: {e}")
                raise InternalServerError("Erro inesperado ao acessar o serviço de IA.")
