from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.signing import TimestampSigner
from django.http import HttpResponse, HttpResponseForbidden
from django.urls import reverse
import mimetypes
import logging
from django.http import JsonResponse

from .models import JobOffer, Candidate, AIQuestion, JobApplication
from .forms import CandidateForm, JobOfferForm
from .ai_utils import evaluate_cv, generate_questions

logger = logging.getLogger(__name__)

def job_list(request):
    jobs = JobOffer.objects.all().order_by('-posted_date')
    return render(request, 'recruitment/job_list.html', {'jobs': jobs})

def job_detail(request, job_id):
    job = get_object_or_404(JobOffer, id=job_id)
    if request.method == 'POST':
        form = CandidateForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                # Guardar candidato
                candidate = form.save(commit=False)
                candidate.job_offer = job
                candidate.save()
                
                # Crear aplicación
                job_application = JobApplication.objects.create(
                    candidate=candidate,
                    job_offer=job,
                    status='pending'
                )
                
                # Evaluar CV
                try:
                    score = evaluate_cv(candidate.cv, job.description)
                    job_application.score = score
                    job_application.save()
                except Exception as e:
                    logger.error(f"Error evaluating CV: {str(e)}")
                    messages.warning(request, "Hubo un problema al procesar tu CV, pero tu aplicación ha sido recibida.")
                    return redirect('job_list')
                
                messages.success(request, "Tu aplicación ha sido enviada con éxito. ¡Gracias por aplicar!")
                
                # Generar preguntas si el score es suficiente
                if score > 0.5:
                    try:
                        questions = generate_questions(job.description)
                        for i, q in enumerate(questions, 1):
                            AIQuestion.objects.create(
                                job_application=job_application,
                                question=f"{i}. {q}"
                            )
                        return redirect('answer_questions', application_id=job_application.id)
                    except Exception as e:
                        logger.error(f"Error generating questions: {str(e)}")
                        return redirect('job_list')
                else:
                    return redirect('job_list')
            except Exception as e:
                logger.error(f"Error in job application process: {str(e)}")
                messages.error(request, "Ha ocurrido un error al procesar tu aplicación. Por favor, intenta nuevamente.")
                return redirect('job_list')
    else:
        form = CandidateForm()
    return render(request, 'recruitment/job_detail.html', {'job': job, 'form': form})

def answer_questions(request, application_id):
    job_application = get_object_or_404(JobApplication, id=application_id)
    
    # Verificar que la aplicación esté pendiente
    if job_application.status != 'pending':
        messages.error(request, "Esta aplicación ya no está disponible para responder preguntas.")
        return redirect('job_list')
    
    if request.method == 'POST':
        try:
            for question in job_application.questions.all():
                answer = request.POST.get(f'answer_{question.id}')
                if answer:
                    question.answer = answer
                    question.save()
            job_application.status = 'completed'
            job_application.save()
            messages.success(request, "Gracias por responder las preguntas. Su aplicación ha sido completada.")
            return redirect('job_list')
        except Exception as e:
            logger.error(f"Error saving answers: {str(e)}")
            messages.error(request, "Ha ocurrido un error al guardar tus respuestas. Por favor, intenta nuevamente.")
    
    return render(request, 'recruitment/answer_questions.html', {'application': job_application})

@login_required
def download_cv(request, application_id):
    """Vista segura para descargar CVs con URLs firmadas"""
    signer = TimestampSigner()
    try:
        # Verificar firma y tiempo de expiración (30 minutos)
        unsigned_id = signer.unsign(application_id, max_age=1800)
        application = get_object_or_404(JobApplication, id=unsigned_id)
        
        if not application.candidate.cv:
            return HttpResponseForbidden("CV no encontrado")
        
        # Obtener el tipo MIME correcto
        content_type, _ = mimetypes.guess_type(application.candidate.cv.name)
        if not content_type:
            content_type = 'application/octet-stream'
        
        # Preparar respuesta
        response = HttpResponse(application.candidate.cv.read(), content_type=content_type)
        response['Content-Disposition'] = f'attachment; filename="{application.candidate.cv.name}"'
        return response
    except Exception as e:
        logger.error(f"Error downloading CV: {str(e)}")
        return HttpResponseForbidden("Link expirado o inválido")

def get_secure_cv_url(application):
    """Genera una URL firmada para descarga segura del CV"""
    signer = TimestampSigner()
    signed_id = signer.sign(str(application.id))
    return reverse('download_cv', kwargs={'application_id': signed_id})

def about_us(request):
    return render(request, 'recruitment/about_us.html')

def contact(request):
    return render(request, 'recruitment/contact.html')

@login_required
def admin_dashboard(request):
    job_offers = JobOffer.objects.all().order_by('-posted_date')
    return render(request, 'recruitment/admin_dashboard.html', {'job_offers': job_offers})

@login_required
def job_applications(request, job_id):
    job = get_object_or_404(JobOffer, id=job_id)
    applications = JobApplication.objects.filter(job_offer=job).order_by('-score')

    # Aplicar filtros
    status_filter = request.GET.get('status')
    min_score = request.GET.get('min_score')
    max_score = request.GET.get('max_score')

    if status_filter and status_filter != 'all':
        applications = applications.filter(status=status_filter)
    if min_score:
        applications = applications.filter(score__gte=float(min_score))
    if max_score:
        applications = applications.filter(score__lte=float(max_score))

    # Generar URLs seguras para los CVs
    for application in applications:
        if application.candidate.cv:
            application.secure_cv_url = get_secure_cv_url(application)

    context = {
        'job': job,
        'applications': applications,
        'status_choices': JobApplication.STATUS_CHOICES,
        'current_status': status_filter,
        'current_min_score': min_score,
        'current_max_score': max_score,
    }
    return render(request, 'recruitment/job_applications.html', context)

@login_required
def application_detail(request, application_id):
    application = get_object_or_404(JobApplication, id=application_id)
    # Generar URL segura para el CV
    if application.candidate.cv:
        application.secure_cv_url = get_secure_cv_url(application)
    return render(request, 'recruitment/application_detail.html', {'application': application})

@login_required
def delete_application(request, application_id):
   application = get_object_or_404(JobApplication, id=application_id)
   if request.method == 'POST':
       application.delete()
       return JsonResponse({'success': True})
   return JsonResponse({'success': False})


@login_required
def create_job_offer(request):
    if request.method == 'POST':
        form = JobOfferForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Oferta de trabajo creada exitosamente.")
            return redirect('admin_dashboard')
    else:
        form = JobOfferForm()
    return render(request, 'recruitment/job_offer_form.html', {'form': form})

@login_required
def edit_job_offer(request, job_id):
    job = get_object_or_404(JobOffer, id=job_id)
    if request.method == 'POST':
        form = JobOfferForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, "Oferta de trabajo actualizada exitosamente.")
            return redirect('admin_dashboard')
    else:
        form = JobOfferForm(instance=job)
    return render(request, 'recruitment/job_offer_form.html', {'form': form, 'job': job})

@login_required
def delete_job_offer(request, job_id):
    job = get_object_or_404(JobOffer, id=job_id)
    if request.method == 'POST':
        job.delete()
        messages.success(request, "Oferta de trabajo eliminada exitosamente.")
        return redirect('admin_dashboard')
    return render(request, 'recruitment/delete_job_offer.html', {'job': job})

def logout_view(request):
    logout(request)
    messages.success(request, "Has cerrado sesión exitosamente.")
    return redirect('job_list')