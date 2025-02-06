# Crea un nuevo archivo llamado populate_db.py en la raíz de tu proyecto

import os
import django
import random
from datetime import date, timedelta

# Configura el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai_recruitment.settings')
django.setup()

from recruitment.models import JobOffer

def create_job_offers():
    job_offers = [
        {
            "title": "Consultor SAP Analytics & Datasphere",
            "company": "Digital Enterprise Solutions",
            "location": "Madrid, España (Híbrido)",
            "job_type": "full_time",
            "salary_range": "45.000€ - 65.000€ anual",
            "description": """
            Digital Enterprise Solutions busca un Consultor SAP especializado en Analytics Cloud y Datasphere para unirse a nuestro equipo de consultoría. Como consultor, serás responsable de implementar y optimizar soluciones de análisis de datos y business intelligence utilizando las últimas tecnologías de SAP.

            Trabajarás en proyectos desafiantes para grandes empresas, ayudándoles a transformar sus datos en insights accionables y a tomar decisiones basadas en datos. Si te apasiona el análisis de datos y tienes experiencia con las soluciones SAP, ¡queremos conocerte!
            """,
            "responsibilities": """
            - Implementar y configurar soluciones de SAP Analytics Cloud y SAP Datasphere para clientes.
            - Desarrollar dashboards, informes y visualizaciones avanzadas utilizando SAP Analytics Cloud.
            - Diseñar y optimizar modelos de datos en SAP Datasphere.
            - Realizar integraciones con diferentes fuentes de datos y sistemas SAP/no SAP.
            - Proporcionar formación y soporte a usuarios finales.
            - Documentar procesos y crear guías de usuario.
            - Colaborar con equipos técnicos y de negocio para entender y satisfacer las necesidades de reporting.
            - Participar en la definición de arquitecturas de datos y estrategias de BI.
            """,
            "requirements": """
            - 3+ años de experiencia en consultoría SAP, específicamente con SAP Analytics Cloud.
            - Experiencia demostrable con SAP Datasphere (anteriormente SAP Data Warehouse Cloud).
            - Conocimientos sólidos en modelado de datos y diseño de dashboards.
            - Experiencia en la integración de diferentes fuentes de datos con SAP Analytics Cloud.
            - Familiaridad con otras soluciones SAP como BW/4HANA, S/4HANA o SAP BTP.
            - Conocimientos de SQL y experiencia en manipulación de datos.
            - Certificaciones SAP relevantes (valorable).
            - Excelentes habilidades de comunicación y presentación.
            - Capacidad para trabajar con equipos multidisciplinares.
            - Inglés nivel B2 o superior.
            """,
            "benefits": """
            - Salario competitivo con bonus anual por objetivos.
            - Modelo de trabajo híbrido (3 días presenciales).
            - 23 días de vacaciones anuales.
            - Plan de desarrollo profesional personalizado.
            - Formación continua y certificaciones SAP pagadas por la empresa.
            - Seguro médico privado extensible a familiares.
            - Plan de pensiones con aportación empresarial.
            - Ticket restaurante y transporte.
            - Horario flexible con jornada intensiva los viernes.
            - Eventos de empresa y actividades de team building.
            """,
        },
        {
            "title": "Desarrollador Full Stack Senior",
            "company": "TechInnovate Solutions",
            "location": "Madrid, España (Remoto)",
            "job_type": "full_time",
            "salary_range": "50.000€ - 70.000€ anual",
            "description": """
            TechInnovate Solutions busca un Desarrollador Full Stack Senior para unirse a nuestro equipo de innovación tecnológica. El candidato ideal tiene una sólida experiencia en desarrollo web tanto en front-end como en back-end, y está apasionado por crear soluciones tecnológicas escalables y de alto rendimiento.

            Nuestro equipo trabaja en proyectos desafiantes para clientes de diversos sectores, utilizando las últimas tecnologías y metodologías ágiles. Si te emociona la idea de trabajar en un entorno dinámico y en constante evolución, ¡queremos conocerte!
            """,
            "responsibilities": """
            - Diseñar, desarrollar y mantener aplicaciones web complejas utilizando tecnologías modernas.
            - Colaborar con equipos multidisciplinarios para definir, diseñar y enviar nuevas características.
            - Optimizar aplicaciones para máxima velocidad y escalabilidad.
            - Implementar seguridad y protección de datos.
            - Integrar interfaces de usuario con servicios y APIs del lado del servidor.
            - Ayudar a mantener la calidad del código, la organización y la automatización.
            - Mentorizar a desarrolladores junior y liderar proyectos técnicos.
            """,
            "requirements": """
            - 5+ años de experiencia en desarrollo web full stack.
            - Dominio de JavaScript, HTML5, CSS3 y frameworks modernos como React, Angular o Vue.js.
            - Experiencia sólida con lenguajes de back-end como Python, Ruby, Java o Node.js.
            - Conocimiento profundo de frameworks de back-end como Django, Ruby on Rails o Express.js.
            - Experiencia con bases de datos relacionales y NoSQL.
            - Familiaridad con sistemas de control de versiones (Git).
            - Conocimiento de principios de diseño de software y patrones arquitectónicos.
            - Excelentes habilidades de resolución de problemas y atención al detalle.
            - Capacidad para trabajar de forma independiente y en equipo.
            - Inglés fluido (hablado y escrito).
            """,
            "benefits": """
            - Salario competitivo y revisión anual.
            - Trabajo remoto con flexibilidad horaria.
            - 23 días de vacaciones anuales.
            - Presupuesto para formación y desarrollo profesional.
            - Seguro médico privado.
            - Plan de pensiones.
            - Eventos de team building y cultura de empresa innovadora.
            """,
        },
        {
            "title": "Data Scientist",
            "company": "AnalyticsPro",
            "location": "Barcelona, España",
            "job_type": "full_time",
            "salary_range": "45.000€ - 65.000€ anual",
            "description": """
            AnalyticsPro está buscando un Data Scientist talentoso y motivado para unirse a nuestro equipo de análisis avanzado. Como Data Scientist, jugarás un papel crucial en la extracción de insights valiosos de grandes conjuntos de datos, ayudando a nuestros clientes a tomar decisiones informadas basadas en datos.

            Trabajarás en proyectos desafiantes en diversos sectores, desde finanzas hasta salud, aplicando técnicas avanzadas de machine learning y estadística para resolver problemas complejos del mundo real.
            """,
            "responsibilities": """
            - Desarrollar modelos predictivos y algoritmos de machine learning.
            - Realizar análisis estadísticos y visualizaciones de datos complejas.
            - Colaborar con equipos de negocio para entender sus necesidades y proporcionar soluciones basadas en datos.
            - Procesar, limpiar y validar la integridad de los datos.
            - Desarrollar procesos y herramientas para monitorear y analizar el rendimiento y la precisión del modelo.
            - Presentar hallazgos a stakeholders no técnicos de manera clara y concisa.
            - Mantenerse actualizado con las últimas tendencias y técnicas en ciencia de datos y machine learning.
            """,
            "requirements": """
            - Grado en Estadística, Matemáticas, Informática o campo relacionado. Se valorará máster o doctorado.
            - 3+ años de experiencia en un rol de Data Scientist.
            - Sólidos conocimientos en Python o R, y SQL.
            - Experiencia con bibliotecas de machine learning como scikit-learn, TensorFlow o PyTorch.
            - Familiaridad con técnicas de big data y herramientas como Hadoop o Spark.
            - Excelentes habilidades analíticas y de resolución de problemas.
            - Fuertes habilidades de comunicación y capacidad para explicar conceptos técnicos a audiencias no técnicas.
            - Experiencia en visualización de datos con herramientas como Tableau o PowerBI.
            """,
            "benefits": """
            - Salario competitivo con bonificaciones basadas en rendimiento.
            - Horario flexible y opción de teletrabajo parcial.
            - 22 días de vacaciones anuales.
            - Presupuesto anual para conferencias y cursos de formación.
            - Seguro médico y dental.
            - Gimnasio en la oficina.
            - Ambiente de trabajo colaborativo y oportunidades de crecimiento profesional.
            """,
        },
        {
            "title": "UX/UI Designer",
            "company": "CreativeHub Digital",
            "location": "Valencia, España (Híbrido)",
            "job_type": "full_time",
            "salary_range": "35.000€ - 55.000€ anual",
            "description": """
            CreativeHub Digital está en busca de un UX/UI Designer apasionado y creativo para unirse a nuestro equipo de diseño. Como UX/UI Designer, serás responsable de crear experiencias de usuario excepcionales y visualmente atractivas para nuestros clientes en diversos proyectos digitales.

            Trabajarás en estrecha colaboración con nuestros equipos de desarrollo y marketing para crear interfaces intuitivas y atractivas que cumplan con los objetivos de negocio de nuestros clientes y deleiten a los usuarios finales.
            """,
            "responsibilities": """
            - Crear wireframes, prototipos y maquetas de alta fidelidad para sitios web y aplicaciones móviles.
            - Realizar investigación de usuarios y análisis de competencia para informar decisiones de diseño.
            - Desarrollar y mantener sistemas de diseño y guías de estilo.
            - Colaborar con desarrolladores para asegurar una implementación precisa de los diseños.
            - Realizar pruebas de usabilidad y utilizar los resultados para mejorar los diseños.
            - Mantenerse actualizado con las últimas tendencias y mejores prácticas en diseño UX/UI.
            - Presentar y justificar decisiones de diseño a clientes y stakeholders internos.
            """,
            "requirements": """
            - Grado en Diseño, Interacción Humano-Computadora o campo relacionado.
            - 3+ años de experiencia en diseño UX/UI para productos digitales.
            - Dominio de herramientas de diseño como Figma, Sketch o Adobe XD.
            - Sólida comprensión de principios de diseño, teoría del color y tipografía.
            - Experiencia en la creación de prototipos interactivos.
            - Conocimientos básicos de HTML, CSS y JavaScript.
            - Excelentes habilidades de comunicación y presentación.
            - Capacidad para trabajar en múltiples proyectos con plazos ajustados.
            - Portfolio que demuestre proyectos de UX/UI exitosos.
            """,
            "benefits": """
            - Salario competitivo con revisiones semestrales.
            - Modelo de trabajo híbrido con 2 días de teletrabajo a la semana.
            - 21 días de vacaciones anuales + tu cumpleaños libre.
            - Presupuesto para equipamiento y software de diseño.
            - Formación continua y asistencia a conferencias de diseño.
            - Seguro médico privado.
            - Descuentos en gimnasios y actividades culturales.
            - Ambiente de trabajo creativo y colaborativo.
            """,
        },
    ]

    for job_data in job_offers:
        job = JobOffer(
            title=job_data['title'],
            company=job_data['company'],
            location=job_data['location'],
            job_type=job_data['job_type'],
            salary_range=job_data['salary_range'],
            description=job_data['description'].strip(),
            responsibilities=job_data['responsibilities'].strip(),
            requirements=job_data['requirements'].strip(),
            benefits=job_data['benefits'].strip(),
            application_deadline=date.today() + timedelta(days=random.randint(14, 30))
        )
        job.save()
        print(f"Creada oferta de trabajo: {job.title}")

if __name__ == '__main__':
    print("Poblando la base de datos...")
    create_job_offers()
    print("¡Población completada!")