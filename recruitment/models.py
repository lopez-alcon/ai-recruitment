from django.db import models
from django.utils.text import slugify
from django.utils import timezone
import uuid
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from storages.backends.s3boto3 import S3Boto3Storage

def validate_file_size(value):
    filesize = value.size
    if filesize > 10 * 1024 * 1024:  # 10MB límite
        raise ValidationError("El archivo no puede ser mayor a 10MB")

class JobOffer(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    company = models.CharField(max_length=100, default="López Alcón")
    location = models.CharField(max_length=100, default="Utrera")
    job_type = models.CharField(max_length=50, default="Tiempo Completo", choices=[
        ('full_time', 'Tiempo completo'),
        ('part_time', 'Tiempo parcial'),
        ('contract', 'Contrato'),
        ('internship', 'Prácticas'),
    ])
    salary_range = models.CharField(max_length=100, blank=True)
    description = models.TextField(default="TBD")
    responsibilities = models.TextField(default="TBD")
    requirements = models.TextField(default="TBD")
    benefits = models.TextField(blank=True)
    application_deadline = models.DateField(null=True, blank=True)
    posted_date = models.DateField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Candidate(models.Model):
    CONTACT_CHOICES = [
        ('phone', 'Llamada telefónica'),
        ('email', 'Correo electrónico'),
        ('whatsapp', 'WhatsApp')
    ]

    def cv_upload_path(instance, filename):
        # Genera un nombre único para el archivo usando UUID
        ext = filename.split('.')[-1]
        filename = f"{uuid.uuid4()}.{ext}"
        # Organiza por fecha
        return f'cvs/{timezone.now().strftime("%Y/%m/%d")}/{filename}'

    name = models.CharField(max_length=100, default="")
    last_name = models.CharField(max_length=100, default="")
    email = models.EmailField()
    phone = models.CharField(max_length=20, null=False, blank=False)
    preferred_contact = models.CharField(max_length=10, choices=CONTACT_CHOICES, default='email')
    cv = models.FileField(
        upload_to=cv_upload_path,
        storage=S3Boto3Storage(),
        max_length=255,
        validators=[
            FileExtensionValidator(allowed_extensions=['pdf']),
            validate_file_size
        ]
    )
    job_offer = models.ForeignKey(JobOffer, on_delete=models.CASCADE)
    score = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} {self.last_name}"

    def get_cv_url(self):
        if self.cv:
            return self.cv.url
        return None

class JobApplication(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('accepted', 'Aceptada'),
        ('rejected', 'Rechazada')
    ]
    candidate = models.ForeignKey('Candidate', on_delete=models.CASCADE)
    job_offer = models.ForeignKey('JobOffer', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    score = models.FloatField(null=True, blank=True)
    application_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.candidate.name} - {self.job_offer.title}"

class AIQuestion(models.Model):
    job_application = models.ForeignKey('JobApplication', on_delete=models.CASCADE, related_name='questions')
    question = models.TextField()
    answer = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Question for {self.job_application.candidate.name}"