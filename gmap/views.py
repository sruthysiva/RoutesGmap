from django.shortcuts import render, redirect,HttpResponse
from django.http import JsonResponse
from .forms import *
import pandas as pd
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import uploadedData
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.hashers import make_password
import googlemaps
from django.conf import settings


gmaps = googlemaps.Client(key=settings.GOOGLE_API_KEY)

@login_required
def upload_file(request):

    if request.method == 'POST':

        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            
            uploaded_file = form.save(commit=False)
            uploaded_file.save()
            
            handle_uploaded_file(request.FILES['file'])
            
            return redirect('home')
            
    else:
        form = FileUploadForm()
    return render(request, 'gmap/upload.html', {'form': form})


@csrf_exempt
def handle_uploaded_file(file):
    
    if file.name.endswith('.csv'):
        df = pd.read_csv(file)
        
    elif file.name.endswith(('.xls', '.xlsx')):
        
        df = pd.read_excel(file)
        
    instances = []

        
    for index, row in df.iterrows():
        
        full_address = f"{row['address']},{row['city']},{row['state']},{row['country']} {row['zipcode']}"
         
        result = gmaps.geocode(full_address)
        
     
        if result:
            
            location = result[0]['geometry']['location']
            latitude = location['lat']
            longitude = location['lng']
            place_id = result[0]['place_id']
            
        else:
           
            latitude = None
            longitude = None
            place_id = None

        instance = uploadedData(
            
            column1_name=row['name'],
            column2_address=row['address'],           
            column3_latitude=latitude,
            column4_longitude=longitude,
            column5_city=row['city'],
            column6_district=row['district'],
            column7_state=row['state'],
            column8_country=row['country'],
            column9_zipcode=row['zipcode'],
            column10_email=row['email'], 
            column11_phone=row['phone'],
            column12_category=row['category'],
            place_id = place_id         
        )

        instances.append(instance)
        

    uploadedData.objects.bulk_create(instances)
    
    
    
    
    


@csrf_protect
def signup(request):
    
    if request.method == 'POST':
        
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password = request.POST['password']
        password2 = request.POST['password2']
        email = request.POST['email']

        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username,first_name=first_name,last_name=last_name,password=password, email=email)
                user.save()
                user_login = authenticate(username=username, password=password)
                if user_login:
                    login(request, user_login)
                return render(request,'gmap/home.html',{'name': username})
        else:
            messages.info(request, 'Passwords do not match')
            return redirect('signup')
    else:
        return render(request, 'gmap/signup.html')

@csrf_protect
def signin(request):
    
    if request.method == 'POST':
        
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            
            login(request, user)
            return render(request,'gmap/home.html',{'name': username})
        
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login')
    else:
        return render(request, 'gmap/signup.html')
    

@login_required
@csrf_exempt
def show_location(request):
    
    try:
        
        uploaded_data = uploadedData.objects.all()
        
        cities = uploadedData.objects.values_list('column5_city', flat=True).distinct()
        districts = uploadedData.objects.values_list('column6_district', flat=True).distinct()
        states = uploadedData.objects.values_list('column7_state', flat=True).distinct()
        catval = uploadedData.objects.values_list('column12_category', flat=True).distinct
               
        context = {
        'uploaded_data': uploaded_data,
        'cities': cities,
        'districts': districts,
        'states': states,
        'catval':catval,
    }
        
        return render(request,'gmap/maps.html',context)
    
    except uploadedData.DoesNotExist:
        
        raise Http404("Location details do not exist")
    
  
@login_required
@csrf_exempt
def show_leads(request): 
    
    if request.method == 'POST':
        row_number = request.POST.get('row_number')
        is_checked = request.POST.get('is_checked') == 'true'

        
        lead = uploadedData.objects.get(pk=row_number)
        lead.visited = is_checked
        lead.save()

        return JsonResponse({'status': 'success'})
    
    leads_list = uploadedData.objects.all()
    paginator = Paginator(leads_list,20)  
    
    page = request.GET.get('page')
    try:
        leads = paginator.page(page)
    except PageNotAnInteger:        
        
        leads = paginator.page(1)
    except EmptyPage:   
        leads = paginator.page(paginator.num_pages)

    return render(request, 'gmap/leads.html', {'leads': leads})


def home(request):
    
    total_leads = uploadedData.objects.count()
    visited_leads = uploadedData.objects.filter(visited='1').count()
    
    return render(request, 'gmap/home.html', {'total_leads': total_leads,'visited_leads':visited_leads})



    
@login_required
def signout(request):
        logout(request)
        return redirect('login')
    

@login_required
def profile(request):
    
    if request.method == 'GET':
        user_data = {            
            'username': request.user.username,
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
        }
        context = {'user_data': user_data}
        return render(request, 'gmap/profile.html', context)
    
    elif request.method == 'POST':
        user = request.user
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        if new_password or confirm_password:
            if new_password == confirm_password:
                user.set_password(new_password)  
                user.save()
                return redirect('profile')
            else:
                return HttpResponse("Old password incorrect", status=400)
            
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.save()
        return redirect('profile')
    
    
    
def forgot(request):
    
    if request.method == 'POST':
        email = request.POST.get("email")
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password == password2:
            user = User.objects.get(email=email)
            user.password = make_password(password)
            user.save()
            update_session_auth_hash(request, user)  
            
            messages.success(request, 'Your password was successfully updated!')
            return redirect('login') 
        
        else:
            messages.error(request, 'Passwords do not match. Please try again.')
    
    return render(request, 'gmap/forgot.html')

    

    