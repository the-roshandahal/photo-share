from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.db.models import Count
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_str
import base64
import qrcode
from io import BytesIO
from django.http import HttpResponse
from .models import *

def home (request):
    return render(request,'index.html')





def dashboard(request):
    if request.user.is_authenticated:
        events = Event.objects.annotate(num_photos=Count('gallery__photo')).all()

        current_site = get_current_site(request)

        event_qrcodes = []
        for event_instance in events:
            event_url = f"{request.scheme}://{current_site.domain}{reverse('event', args=[event_instance.event_credentials, event_instance.secret_token])}"

            # Encode the event credentials and secret token for use in the URL
            event_credentials_b64 = urlsafe_base64_encode(force_str(event_instance.event_credentials).encode())
            secret_token_b64 = urlsafe_base64_encode(force_str(event_instance.secret_token).encode())

            # Generate a single QR code for each event
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(event_url)
            qr.make(fit=True)

            buffer = BytesIO()
            qr_img = qr.make_image(fill_color="black", back_color="white")
            qr_img.save(buffer, format="PNG")
            qr_img_data = base64.b64encode(buffer.getvalue()).decode("utf-8")

            event_qrcodes.append({
                'event_instance': event_instance,
                'qr_img_data': qr_img_data,
                'event_url': event_url,
                'event_credentials_b64': event_credentials_b64,
                'secret_token_b64': secret_token_b64,
            })

        context = {
            'event_qrcodes': event_qrcodes,
        }

        return render(request, 'dashboard.html', context)
    else:
        return redirect('home')
# views.py

from django.http import HttpResponse
from django.utils.http import urlsafe_base64_decode

def download_qr_code(request, event_credentials, secret_token):
    event = get_object_or_404(Event, event_credentials=urlsafe_base64_decode(event_credentials).decode(),
                               secret_token=urlsafe_base64_decode(secret_token).decode())
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    event_url = f"{request.scheme}://{request.get_host()}{reverse('event', args=[event.event_credentials, event.secret_token])}"

    qr.add_data(event_url)
    qr.make(fit=True)

    buffer = BytesIO()
    qr_img = qr.make_image(fill_color="black", back_color="white")
    qr_img.save(buffer, format="PNG")
    image_data = buffer.getvalue()

    response = HttpResponse(image_data, content_type='image/png')
    response['Content-Disposition'] = f'attachment; filename="{event.event_name}_qr_code.png"'

    return response


def upload_photo_guest(request, event_credentials):
    event = Event.objects.get(event_credentials=event_credentials)
    if request.method == 'POST':
        name = request.POST.get('name')
        images = request.FILES.getlist('images')
        
        event_obj = Event.objects.get(event_credentials=event_credentials)
        gallery, created = Gallery.objects.get_or_create(event = event_obj, gallery_name=name)
        print(gallery)
        for image in images:
            Photo.objects.create(
                gallery=gallery,
                guest_name=name,
                image=image,
            )
        return redirect('gallery_detail', gallery_id=gallery.id)
    else:
        context = {
            'event': event,
        }
        return render(request, 'upload_photo_guest.html', context)



def create_gallery(request):
    if request.method == 'POST':
        gallery_name = request.POST['gallery_name']
        gallery_obj = Gallery.objects.create(gallery_name = gallery_name)
        gallery_obj.save()
        return redirect('home')
    else:
        return render(request,'create_gallery.html')



def gallery_detail(request, gallery_id):
    gallery = get_object_or_404(Gallery, id=gallery_id)
    photos = Photo.objects.filter(gallery=gallery)
    return render(request, 'gallery_detail.html', {'gallery': gallery, 'photos': photos})


def create_event(request):
    return render(request, 'create_event.html')


# event detail page
def event(request, event_credentials, secret_token):
    event = get_object_or_404(Event, event_credentials=event_credentials, secret_token=secret_token)
    gallerys = Gallery.objects.filter(event=event).annotate(num_photos=Count('photo'))
    context = {
        'gallerys':gallerys,
        'event':event,
    }
    return render(request, 'event.html', context)


def create_photographer(request):
    pass

def create_folder(request):
    pass

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        print(user)

        if user is not None:
            login(request, user)
            messages.success(request, 'Successfully logged in.')
            return redirect('home')  # Redirect to the home page after successful login
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html')

# def upload_photo_user(request):
#     if request.method == 'POST':
#         name = request.POST.get('name')
#         images = request.FILES.getlist('images')

#         gallery, created = Gallery.objects.get_or_create(gallery_name=name)
#         print(gallery)
#         for image in images:
#             Photo.objects.create(
#                 gallery=gallery,
#                 guest_name=name,
#                 image=image,
#             )
#         return redirect('gallery_detail', gallery_id=gallery.id)

#     return render(request, 'upload_photo_guest.html')