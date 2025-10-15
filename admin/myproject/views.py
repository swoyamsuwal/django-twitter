from django.contrib.auth.models import User
from django.contrib.auth import login
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from .models import Tweet
from .forms import UserRegisterForm
from .serializers import TweetSerializer, UserSerializer  # Create UserSerializer for API


# ================================
# 🌐 API Views (Serializer-based)
# ================================

@api_view(['GET'])
def tweet_api_list(request):
    """Return all tweets as JSON"""
    tweets = Tweet.objects.all().order_by('-created_at')
    serializer = TweetSerializer(tweets, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def tweet_api_detail(request, tweet_id):
    """Return a single tweet detail"""
    tweet = get_object_or_404(Tweet, id=tweet_id)
    serializer = TweetSerializer(tweet)
    return Response(serializer.data)


@api_view(['POST'])
def tweet_api_create(request):
    """Create a new tweet and assign the logged-in user automatically"""
    if not request.user.is_authenticated:
        return Response({"error": "Authentication required."}, status=status.HTTP_401_UNAUTHORIZED)

    serializer = TweetSerializer(data=request.data)
    if serializer.is_valid():
        # Assign the logged-in user automatically
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['PUT'])
def tweet_api_update(request, tweet_id):
    """Update an existing tweet"""
    tweet = get_object_or_404(Tweet, id=tweet_id)
    serializer = TweetSerializer(tweet, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def tweet_api_delete(request, tweet_id):
    """Delete a tweet"""
    tweet = get_object_or_404(Tweet, id=tweet_id)
    tweet.delete()
    return Response({"message": "Tweet deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


# -----------------------------
# 👤 User Registration (API)
# -----------------------------
@api_view(['POST'])
def register_api(request):
    """Register a new user"""
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        user.set_password(serializer.validated_data['password'])
        user.save()
        login(request, user)
        return Response({"message": "User registered successfully."}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# -----------------------------
# 🔍 Search Tweets (API)
# -----------------------------
@api_view(['GET'])
def search_api(request):
    """Search tweets by text"""
    query = request.GET.get('search', '')
    tweets = Tweet.objects.filter(text__icontains=query) if query else Tweet.objects.none()
    serializer = TweetSerializer(tweets, many=True)
    return Response(serializer.data)


# ================================
# ❌ Normal Django Views (Commented)
# ================================

"""
def tweet_list(request):
    tweets = Tweet.objects.all().order_by('-created_at')
    return render(request, 'tweet_list.html', {'tweets': tweets})

@login_required
def tweet_create(request):
    if request.method == 'POST':
        form = TweetForm(request.POST, request.FILES)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            return redirect('tweet_list')
    else:
        form = TweetForm()
    return render(request, 'tweet_form.html', {'form': form})

@login_required
def tweet_edit(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user=request.user)
    if request.method == 'POST':
        form = TweetForm(request.POST, request.FILES, instance=tweet)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            return redirect('tweet_list')
    else:
        form = TweetForm(instance=tweet)
    return render(request, 'tweet_form.html', {'form': form})

@login_required
def tweet_delete(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user=request.user)
    tweet.delete()
    return redirect('tweet_list')

def register(request):
    if request.method == 'POST':
        UserRegisterForm(request.POST)
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request, user)
            return redirect('tweet_list')
    else:
        form = UserRegisterForm()

    return render(request, 'registration/register.html', {'form': form})

def search(request):
    query = request.GET.get('search', '')
    tweets = Tweet.objects.filter(text__icontains=query) if query else []
    return render(request, 'search.html', {'tweets': tweets, 'query': query})   
"""