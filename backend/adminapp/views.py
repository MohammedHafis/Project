from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib import messages
from rest_framework.response import Response
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view,permission_classes
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from .models import User
from django.contrib.auth import authenticate,login
from rest_framework.permissions import IsAuthenticated
from adminapp.models import Movie,Watch_later,View_history
from .serializers import MovieSerializer,ViewHistorySerializer
from .serializers import WatchSerializer
from django.contrib.auth import logout as django_logout

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages

def Login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password') 
        
        user = authenticate(request, email=email, password=password)
        
        if user is not None and user.is_admin: 
            login(request, user)
            return redirect('movielist')
        else:
            print("Login failed - invalid credentials")
            messages.error(request, 'Invalid email or password')
    
    return render(request, 'login.html')



@login_required(login_url='/')
def movielist(request):
    movies = Movie.objects.all()
    paginator = Paginator(movies, 10) 
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'movielist.html', {'page_obj': page_obj})

@login_required(login_url='/')
def addmovie(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        thumbnail = request.FILES.get('thumbnail')
        video = request.FILES.get('video')

        if title and description and thumbnail and video:
            Movie.objects.create(
                title=title,
                description=description,
                thumbnail=thumbnail,
                video=video
            )
            return redirect('movielist') 
        else:
            error = "All fields are required."
            return render(request, 'addmovie.html', {'error': error})

    return render(request, 'addmovie.html')

@login_required(login_url='/')
def editmovie(request, pk):
    movie = get_object_or_404(Movie, pk=pk)

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')

        thumbnail = request.FILES.get('thumbnail')
        video = request.FILES.get('video')

        # Update fields
        movie.title = title
        movie.description = description
        
        if thumbnail:
            movie.thumbnail = thumbnail
        
        if video:
            movie.video = video
        
        movie.save()
        return redirect('movielist')  
    return render(request, 'editmovie.html', {'movie': movie})

@login_required(login_url='/')
def movie_delete(request,pk):
    movie=Movie.objects.get(pk=pk)  
    if request.method == 'POST':
        movie.delete()
        return redirect('movielist')
    
    return render(request,'delete.html',{'movie':movie})

@login_required(login_url='/')
def viewmovie(request,pk):
    movie = Movie.objects.get(pk=pk)
    return render(request, 'viewmovie.html', {'movie': movie})

@login_required(login_url='/')
def userlist(request):
    search_query = request.GET.get('search', '')
    
    if search_query:
        users = User.objects.filter(
            Q(name__icontains=search_query) | 
            Q(email__icontains=search_query)
        ).order_by('name')
    else:
        users = User.objects.all().order_by('name')
    
    return render(request, 'userlist.html', {
        'users': users,
        'search_query': search_query
    })

@login_required(login_url='/')
def userhistory(request, pk):
    user = User.objects.get(pk=pk)
    history = View_history.objects.filter(user=user)
    return render(request, 'userhistory.html', {'history': history,'user': user})

@login_required(login_url='/')
def reports(request):
    movies = Movie.objects.all().order_by('-views')
    paginator = Paginator(movies, 10) 
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'reports.html', {'page_obj': page_obj})

def logout(request):
    django_logout(request)
    return redirect('/')

@login_required(login_url='/')
def blockuser(request, pk):
    user_obj = User.objects.get(pk=pk) 
    user_obj.is_active = False
    user_obj.save()
    return redirect('userlist') 

@login_required(login_url='/')
def unblockuser(request, pk):
    user_obj = User.objects.get(pk=pk)
    user_obj.is_active = True
    user_obj.save()
    return redirect('userlist')

@login_required(login_url='/')
def changepassword(request):
     if request.method == 'POST':
        user = request.user
        old_password = request.POST.get('oldPassword')
        new_password = request.POST.get('password')
        new_password_confirm = request.POST.get('passnew1')
    
        if new_password != new_password_confirm:
            messages.error(request, 'New passwords do not match.')
            return redirect('change_password')

        if not old_password or not new_password:
            messages.error(request, 'Both old and new passwords are required.')
            return redirect('change_password')

        if not user.check_password(old_password):
            messages.error(request, 'Old password is incorrect.')
            return redirect('change_password')

        user.set_password(new_password)
        user.save()

        messages.success(request, 'Password changed successfully.')
        return redirect('change_password')

     return render(request, 'changepass.html')
   




@api_view(['POST'])
@permission_classes((AllowAny,))
def signup(request):
        email = request.data.get('email')
        name = request.data.get('name')
        password = request.data.get('password')

        if not email or not password:
            return Response({'error': 'Email and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            return Response({'error': 'User already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(email=email, password=password)
        user.name = name
        user.save()

        return Response({'message': 'Signup successful'}, status=status.HTTP_201_CREATED)
    
@api_view(['POST'])
@permission_classes((AllowAny,))
def loginup(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
        return Response(
            {'error': 'Email and password are required.'}, 
            status=status.HTTP_400_BAD_REQUEST
        )

    user = authenticate(username=email, password=password)

    if not user:
        return Response(
            {'error': 'Invalid email or password'}, 
            status=status.HTTP_401_UNAUTHORIZED
        )

    if not user.is_active:
        return Response(
            {'error': 'Your ID is temporarily deactivated'}, 
            status=status.HTTP_403_FORBIDDEN  # 403 is better than 401 here
        )

    token, _ = Token.objects.get_or_create(user=user)
    return Response({
        'token': token.key,
        'user_id': user.id,
        'email': user.email
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def movie_list(request):
    movies =  Movie.objects.all()
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_watchlater(request):
    movie_id = request.data.get('movie_id')

    if not movie_id:
        return Response({'error': 'Movie ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        movie = Movie.objects.get(id=movie_id)
    except Movie.DoesNotExist:
        return Response({'error': 'Movie not found.'}, status=status.HTTP_404_NOT_FOUND)

    user = request.user

    if Watch_later.objects.filter(user=user, movie=movie).exists():
        return Response({'message': 'Movie is already in your watch later list.'}, status=status.HTTP_200_OK)

    Watch_later.objects.create(user=user, movie=movie)

    return Response({'message': 'Movie added to watch later list.'}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def watchlater_list(request):
    user = request.user
    watch_later_movies = Watch_later.objects.filter(user=user).select_related('movie')
    movies = [entry.movie for entry in watch_later_movies]
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_watchlater(request, movie_id):
    user = request.user
    try:
        watch_entry = Watch_later.objects.get(user=user, movie_id=movie_id)
        watch_entry.delete()
        return Response({'message': 'Movie removed from watch later list.'}, status=status.HTTP_200_OK)
    except Watch_later.DoesNotExist:
        return Response({'error': 'Movie not found in your watch later list.'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def watch_history(request):
    movie_id = request.data.get('movie_id')

    if not movie_id:
        return Response({'error': 'Movie ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        movie = Movie.objects.get(id=movie_id)
        movie.views+=1
        movie.save()
    except Movie.DoesNotExist:
        return Response({'error': 'Movie not found.'}, status=status.HTTP_404_NOT_FOUND)

    user = request.user

    if View_history.objects.filter(user=user, movie=movie).exists():
        return Response({'message': 'Movie is already in your History.'}, status=status.HTTP_200_OK)

    View_history.objects.create(user=user, movie=movie)

    return Response({'message': 'Movie added to watch History.'}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def watch_history_list(request):
    user = request.user
    watch_history_movies = View_history.objects.filter(user=user).select_related('movie')
    # movies = [entry.movie for entry in watch_history_movies]
    serializer = ViewHistorySerializer(watch_history_movies, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def movie_detail(request, movie_id):
    try:
        movie = Movie.objects.get(id=movie_id)
    except Movie.DoesNotExist:
        return Response({"error": "Movie not found"}, status=404)

    serializer = MovieSerializer(movie)
    return Response(serializer.data)

from rest_framework.authtoken.models import Token

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    user = request.user
    old_password = request.data.get('oldpassword')
    new_password = request.data.get('password')

    if not old_password or not new_password:
        return Response({'error': 'Both old and new passwords are required.'}, status=status.HTTP_400_BAD_REQUEST)

    if not user.check_password(old_password):
        return Response({'error': 'Old password is incorrect.'}, status=status.HTTP_400_BAD_REQUEST)

    user.set_password(new_password)
    user.save()

    # Delete old token to force re-login
    Token.objects.filter(user=user).delete()

    return Response({'message': 'Password changed successfully. Please login again.'}, status=status.HTTP_200_OK)
