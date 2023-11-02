from django.shortcuts import redirect
from django.shortcuts import render
import smtplib
from django.conf import settings
from django.core.mail import EmailMultiAlternatives, send_mail

#models
from .models import Contact

def contact(request, state = 0):
    form_submitted = state

    if request.method == "POST":
        data = request.POST
        obj_contact = Contact()
        obj_contact.full_name = data["name"]
        obj_contact.email = data["email"]
        obj_contact.phone_number = data["phone"]
        obj_contact.message = data["message"]
        
        obj_contact.save()
        sendEmail(data)
        # Redirect to a confirmation page after a successful submission.
        return redirect('confirmation_page')  # Replace 'confirmation_page' with the actual URL name.

    return render(request, "contact.html", {'form_submitted': form_submitted})

def confirmation(request):
    return render(request, 'confirmation.html')


def sendEmail(data):
    hostPass = settings.EMAIL_HOST_PASSWORD
    host = settings.EMAIL_HOST
    port = settings.EMAIL_PORT
    hostUser = settings.EMAIL_HOST_USER 
    reciever_email = 'mon.andres02@gmail.com'

    text_message = f"Mensaje: {data['message']}, de: {data['name']} informacion de contacto: {data['phone'], data['email']}"
    text = f"Subject: Nuevo mensaje de: {data['name']}\n\n {text_message}"
    server = smtplib.SMTP(host, port)
    server.starttls()
    server.login(hostUser, hostPass)
    server.sendmail(hostUser, reciever_email, text)
    print("email sent and message:" + text)

# clave gmail 
# xsws zfwi molz jfuk