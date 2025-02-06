from openai import OpenAI
import logging
import chardet
import PyPDF2
import io
import os
from django.conf import settings
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

logger = logging.getLogger(__name__)

# Inicializar el cliente de OpenAI usando la variable de entorno
client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))

def evaluate_cv(cv_file, job_description):
    """
    Evalúa un CV para una oferta de trabajo específica usando OpenAI.
    """
    try:
        # Leer el PDF
        cv_content = ""
        try:
            # Crear un lector de PDF
            pdf_reader = PyPDF2.PdfReader(cv_file)
            
            # Extraer texto de todas las páginas
            for page in pdf_reader.pages:
                cv_content += page.extract_text() + "\n"
                
            logger.debug(f"Contenido extraído del CV: {cv_content[:200]}...")  # Primeros 200 caracteres
            
        except Exception as e:
            logger.error(f"Error al leer el PDF: {str(e)}")
            return 0.5

        # Extraer información relevante del CV (primeros 2000 caracteres)
        cv_summary = cv_content[:2000]

        # Preparar el prompt
        prompt = f"""Evalúa la idoneidad del siguiente CV para el trabajo descrito.
        
        Trabajo: {job_description[:1000]}

        CV: {cv_summary}
        
        Evalúa la coincidencia en una escala de 0 a 1, donde 1 es una coincidencia perfecta.
        Responde solo con el número."""

        # Realizar la llamada a la API de OpenAI
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Eres un evaluador experto de CVs."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            temperature=0.3
        )

        # Extraer la puntuación de la respuesta
        score_text = response.choices[0].message.content.strip()
        try:
            score = float(score_text)
            score = max(0.0, min(1.0, score))  # Asegurar que el score esté entre 0 y 1
            return score
        except ValueError:
            logger.error(f"No se pudo convertir la respuesta a float: {score_text}")
            return 0.5

    except Exception as e:
        logger.error(f"Error al evaluar CV: {str(e)}")
        logger.exception(e)
        return 0.5  # Valor por defecto en caso de error

def generate_questions(job_description):
    """
    Genera preguntas relacionadas con la oferta de trabajo usando OpenAI.
    """
    try:
        prompt = f"""Basándote en esta descripción de trabajo, genera 3 preguntas técnicas específicas para evaluar a los candidatos:

        Descripción del trabajo: {job_description}

        Genera exactamente 3 preguntas numeradas, relevantes y específicas para este puesto."""

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Eres un experto en recursos humanos."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=300
        )

        questions_text = response.choices[0].message.content.strip()
        questions = [q.strip() for q in questions_text.split('\n') if q.strip()]

        # Asegurar que tengamos exactamente 3 preguntas
        while len(questions) < 3:
            questions.append("¿Podrías describir tu experiencia relevante para este puesto?")
        
        return questions[:3]  # Devolver solo las primeras 3 preguntas

    except Exception as e:
        logger.error(f"Error al generar preguntas: {str(e)}")
        logger.exception(e)
        # Preguntas genéricas en caso de error
        return [
            "¿Podrías describir tu experiencia relevante para este puesto?",
            "¿Cuáles son tus principales fortalezas técnicas?",
            "¿Por qué te interesa este puesto?"
        ]