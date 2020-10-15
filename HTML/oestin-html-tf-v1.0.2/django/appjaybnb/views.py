from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.shortcuts import redirect
from django.contrib import messages
from django.db.models import Q
from datetime import datetime
from django.core.mail import send_mail, BadHeaderError

# Create your views here.
class ContactForm(object):
    from_email = ""
    subject = ""
    message = ""


def home(request):
    return render(request, 'core/home.html')

def team(request):
    return render(request, 'info/team.html')

def roomGrid(request):
    return render(request, 'propiedades/room-grid.html')

def contacto(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        request.method == 'POST'
        form = ContactForm()
        subject = request.POST['name']
        from_email = request.POST['email']
        message = request.POST['message']
        try:
            send_mail(subject, message, from_email, ['admin@example.com'])
            return redirect('contacto')
        except BadHeaderError:
            return HttpResponse('Invalid header found.')
        return redirect('success')
    return render(request, "contacto/contact.html")

def successView(request):
    return HttpResponse('Success! Thank you for your message.')
