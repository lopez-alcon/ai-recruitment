from django import forms
from .models import Candidate, JobOffer
from django.core.exceptions import ValidationError

class CandidateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Clases base para los campos
        input_classes = "w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
        select_classes = "w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors appearance-none bg-white"
        
        # Aplicar clases a los campos
        text_fields = ['name', 'last_name', 'email', 'phone']
        for field in text_fields:
            self.fields[field].widget.attrs.update({
                'class': input_classes,
                'placeholder': self.fields[field].label
            })
        
        # Aplicar clases al selector
        self.fields['preferred_contact'].widget.attrs.update({
            'class': select_classes
        })
        
        # Campo de CV
        self.fields['cv'].widget.attrs.update({
            'class': 'hidden',
            'accept': 'application/pdf'
        })

    def clean_cv(self):
        cv = self.cleaned_data.get('cv')
        if cv:
            if not cv.name.lower().endswith('.pdf'):
                raise ValidationError('Solo se permiten archivos PDF')
            if cv.size > 10 * 1024 * 1024:  # 10MB
                raise ValidationError('El archivo no puede ser mayor a 10MB')
        return cv

    class Meta:
        model = Candidate
        fields = ['name', 'last_name', 'email', 'phone', 'preferred_contact', 'cv']
        labels = {
            'name': 'Nombre',
            'last_name': 'Apellidos',
            'email': 'Correo electrónico',
            'phone': 'Teléfono de contacto',
            'preferred_contact': 'Vía preferida de contacto',
            'cv': 'Curriculum Vitae (PDF)'
        }

class JobOfferForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Clases base para todos los campos
        input_classes = "w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
        textarea_classes = "w-full p-4 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors h-32"
        
        # Aplicar clases a los campos de texto
        text_fields = ['title', 'company', 'location', 'job_type', 'salary_range']
        for field in text_fields:
            self.fields[field].widget.attrs.update({
                'class': input_classes
            })
        
        # Aplicar clases a los campos de área de texto
        textarea_fields = ['description', 'requirements', 'responsibilities', 'benefits']
        for field in textarea_fields:
            self.fields[field].widget.attrs.update({
                'class': textarea_classes
            })
        
        # Campo de fecha
        self.fields['application_deadline'].widget.attrs.update({
            'class': input_classes,
            'type': 'date'
        })

    class Meta:
        model = JobOffer
        fields = ['title', 'company', 'location', 'job_type', 'salary_range',
                 'application_deadline', 'description', 'requirements',
                 'responsibilities', 'benefits']