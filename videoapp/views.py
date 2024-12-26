from django.shortcuts import render, redirect

# Create your views here.

from .api import *
from django.shortcuts import render
from gtts import gTTS
import os, io, json
from io import BytesIO
import requests
from openai import AzureOpenAI
from PIL import Image
#import langdetect
import shutil
from .api import *
from django.http import  JsonResponse
import time
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .agora.RtcTokenBuilder import RtcTokenBuilder, Role_Attendee
from django.core.validators import validate_email
from django.contrib.auth.password_validation import validate_password
from django.db.models import Q
from django.core.mail import EmailMessage
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from .models import VerificationCode

def upload_file(request):
    if request.method == 'POST' and request.FILES['file']:
        file = request.FILES['file']
        fs = FileSystemStorage()
        filename = fs.save(file.name, file)
        file_url = fs.url(filename)
        
        # Notifier via WebSocket
        # Vous pouvez appeler un consumer ici ou utiliser un autre moyen pour envoyer une notification WebSocket

        return JsonResponse({'file_url': file_url})
    return render(request, 'chat/upload.html')




@csrf_exempt
def generate_agora_token(request):
    app_id = 'f2891190d713482dbed4c3fd804ec233'
    app_certificate = 'ec7803663ae640658b2a5afe5dc0894e'
    channel_name = 'channel1'
    uid = 0  # Utilisez 0 pour des utilisateurs anonymes ou un UID spécifique
    #role = RtcTokenBuilder.Role_Attendee  # Utilisateur participant à la réunion
    expiration_time_in_seconds = 3600  # Durée de validité du token en secondes

    current_timestamp = int(time.time())
    privilege_expired_ts = current_timestamp + expiration_time_in_seconds

    token = RtcTokenBuilder.buildTokenWithUid(app_id, app_certificate, channel_name, uid, Role_Attendee, privilege_expired_ts)
    print("="*10, "token", "="*10)
    print(token)
    print("="*10, "token", "="*10)
    return JsonResponse({'token': token})

@login_required
def index(request):
    return render(request, "index.html")

def chat_view(request):
    return render(request, "chat.html")

def chat_ai(request):
    if request.method == "POST":
        print(request.body)
        data = json.loads(request.body)
        text = data.get("user_input")
        print(text)
        
        try:
            text = chat(text)
            print(text)
            return JsonResponse({ 'success': True,  'text':f'{text}'})
        except Exception as e:
            text = chat(text)
            return JsonResponse({ 'success': False,'text':f'{e}'})
    return render(request, "chat.html")



def forgotpassword(request):
    return render(request, "index.html")


def register(request):
    mess = ""
    if request.method == "POST":
        
        print("="*5, "NEW REGISTRATION", "="*5)
        username = request.POST.get("username", None)
        email = request.POST.get("email", None)
        pass1 = request.POST.get("password1", None)
        pass2 = request.POST.get("password2", None)
        print(username, email, pass1, pass2)
        try:
            validate_email(email)
        except:
            mess = "Invalid Email"
        if pass1 != pass2 :
            mess += " Password not match"
        if User.objects.filter(Q(email= email)| Q(username=username)).first():
            mess += f" Exist user with email {email}"
        print("Message: ", mess)
        if mess=="":
            try:
                    validate_password(pass1)
                    user = User(username= username, email = email)
                    user.save()
                    user.password = pass1
                    user.set_password(user.password)
                    user.save()
                   

                    subject = "Bienvenue sur videoCall !"

                    email_message = f"""
                    Cher(e) {username},

                    Nous sommes ravis de t’accueillir sur videoCall ! 🎉

                    Ton compte a été créé avec succès, et tu es maintenant prêt(e) à explorer l'univers passionnant des appels vidéo multilingues. Grâce à notre plateforme, tu peux te connecter avec des personnes du monde entier et profiter de la traduction vocale en temps réel lors de tes appels vidéo.

                    Voici quelques fonctionnalités incroyables que tu peux découvrir dès maintenant :

                    - Communique avec des utilisateurs parlant différentes langues, avec ta voix instantanément traduite dans la langue de ton interlocuteur.
                    - Brise les barrières linguistiques et échange facilement avec des personnes parlant français, anglais, espagnol, et bien d’autres !
                    - Profite d’une traduction fluide et en temps réel grâce à notre technologie IA avancée.
                    - Explore une large sélection de langues pour une expérience de communication véritablement mondiale.

                    Nous sommes impatients de t’aider à connecter avec le monde entier de manière inédite. Si tu as des questions ou besoin d’assistance, n’hésite pas à nous contacter à [ton adresse e-mail] ou à visiter notre page de support.

                    Encore une fois, bienvenue sur videoCall ! Nous sommes ravis de t’avoir parmi nous.

                    Cordialement,  
                    L’équipe videoCall
                    """

                    email = EmailMessage(subject,
                             email_message,
                             f"Youtube VideoTrans <{settings.EMAIL_HOST}>",
                             [user.email])

                    email.send()
                    mess = f"Welcome {user.username}, Your account is create successfully, to active your account, get you verification code in your email boss at {user.email}"
                        
                    messages.info(request, mess)

                    verification_code, created = VerificationCode.objects.get_or_create(user=user)
                    verification_code.generate_code()
                    print(verification_code.code)
                    
                    code = EmailMessage(
                        'Votre code de vérification ',
                        f'Bonjour,\n\nVotre code de vérification pour activer votre compte sur videoCall est : {verification_code.code}\n\nMerci de l\'utiliser pour valider votre inscription.',
                        f"videoCall <{settings.EMAIL_HOST}>",
                        [user.email]
                    )


                    code.send()
                    return redirect("code")
            except Exception as e:
                    print("error: ", e)
                    #err = " ".join(e)
                    messages.error(request, e)
                    return render(request, template_name="register.html")
            
        #messages.info(request, "Bonjour")

    return render(request, template_name="register.html")



def connection1(request):
    mess = ""

    '''if request.user.is_authenticated:
         return redirect("dashboard")'''
    if request.method == "POST":
        
        print("="*5, "NEW CONECTION", "="*5)
        email = request.POST.get("email")
        password = request.POST.get("password")
        
        try:
            validate_email(email)
        except:
            mess = "Invalid Email !!!"
        #authen = User.lo
        if mess=="":
            user = User.objects.filter(email= email).first()
            if user:
                auth_user= authenticate(username= user.username, password= password)
                if auth_user:
                    print("Utilisateur infos: ", auth_user.username, auth_user.email)
                    login(request, auth_user)
                    
                    return redirect("index")
                else :
                    mess = "Incorrect password"
            else:
                mess = "user does not exist"
            
        messages.info(request, mess)

    return render(request, template_name="login.html")


from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.contrib import messages
from django.conf import settings
from django.shortcuts import render, redirect

def connection(request):
    mess = ""

    if request.method == "POST":
        print("="*5, "NEW CONNECTION", "="*5)
        email = request.POST.get("email")
        password = request.POST.get("password")
        remember_me = request.POST.get("remember_me")  # Récupération de l'option "Se souvenir de moi"
        
        try:
            validate_email(email)
        except:
            mess = "Invalid Email !!!"

        if mess == "":
            user = User.objects.filter(email=email).first()
            if user:
                auth_user = authenticate(username=user.username, password=password)
                if auth_user:
                    print("Utilisateur infos: ", auth_user.username, auth_user.email)
                    
                    # Authentification et gestion de session
                    login(request, auth_user)
                    
                    # Gérer la durée de la session
                    if remember_me:  # Si "Se souvenir de moi" est coché
                        request.session.set_expiry(settings.SESSION_COOKIE_AGE)  # 30 jours
                    else:
                        request.session.set_expiry(0)  # Expire à la fermeture du navigateur
                    
                    return redirect("index")
                else:
                    mess = "Incorrect password"
            else:
                mess = "User does not exist"
            
        messages.info(request, mess)

    return render(request, template_name="login.html")


def code(request):
    mess = ""

   
    if request.method == "POST":
        
        print("="*5, "NEW CONECTION", "="*5)
        email = request.POST.get("email")
        code_v = request.POST.get("code")
        user = User.objects.filter(email= email).first()
        verification_code, created = VerificationCode.objects.get_or_create(user=user)
        
        print(verification_code.code)
        if str(code_v) == str(verification_code.code) :
            messages.info(request, "Code valide")
            return redirect("login")
        else:
            mess = "Invalid code !!!"
      
        messages.info(request, mess)

    return render(request, template_name="code.html")



def deconnexion(request):
         print("Deconnexion")
         logout(request)
         return redirect("index")
    


'''from openai import AzureOpenAI

# may change in the future
# https://learn.microsoft.com/en-us/azure/ai-services/openai/reference#rest-api-versioning
api_version = "2023-07-01-preview"

# gets the API Key from environment variable AZURE_OPENAI_API_KEY
client = AzureOpenAI(
    api_version=api_version,
    # https://learn.microsoft.com/en-us/azure/cognitive-services/openai/how-to/create-resource?pivots=web-portal#create-a-resource
    azure_endpoint="https://example-endpoint.openai.azure.com",
)

completion = client.chat.completions.create(
    model="gpt-35-turbo",  # e.g. gpt-35-instant
    messages=[
        {
            "role": "user",
            "content": "How do I output all files in a directory using Python?",
        },
    ],
)
print(completion.to_json())


deployment_client = AzureOpenAI(
    api_version=api_version,
    # https://learn.microsoft.com/en-us/azure/cognitive-services/openai/how-to/create-resource?pivots=web-portal#create-a-resource
    azure_endpoint="https://example-resource.azure.openai.com/",
    # Navigate to the Azure OpenAI Studio to deploy a model.
    azure_deployment="gpt-35-turbo",  # e.g. gpt-35-instant
)

completion = deployment_client.chat.completions.create(
    model="<ignored>",
    messages=[
        {
            "role": "user",
            "content": "How do I output all files in a directory using Python?",
        },
    ],
)
print(completion.to_json())'''
