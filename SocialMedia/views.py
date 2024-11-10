from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import UserRegistrationForm, SignUpForm, PostForm, CommentForm, ProfileForm, UsernameForm, PronounsForm, BioForm, UserUpdateForm, CardForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from .models import FriendRequest, Friendship, Post, Comment, Profile, Bookmark, Card
from django.shortcuts import redirect, get_object_or_404
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.template.loader import render_to_string
import logging


@login_required
def home(request):
    friendships = request.user.friend1.all() | request.user.friend2.all()
    friends = list(set(friendship.user2 if friendship.user1 == request.user else friendship.user1 for friendship in friendships))
    posts = Post.objects.filter(is_short=False)

    for post in posts:
        post.comments_list = post.comments.all() 

    if 'id' in request.GET:
        post_id = request.GET['id']
        post = get_object_or_404(Post, id=post_id)
        return render(request, 'post_detail.html', {'post': post})
    else:
        # Default behavior (e.g. showing the post list on home)
        posts = Post.objects.all()

    return render(request, 'Index/index.html', {'posts': posts, 'friends': friends})



def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")  # Add an error message
    return render(request, 'registration/login.html')


def user_logout(request):
    logout(request)
    return redirect('login')  # Redirect to the login page after logout

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)  # Use SignUpForm here
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Set the password after hashing
            user.save()

            # Log the user in after registration
            login(request, user)

            messages.success(request, 'Account created and logged in successfully!')  # Success message
            return redirect('home')  # Redirect to homepage after successful sign-up and login
    else:
        form = SignUpForm()  # Use SignUpForm here
    
    # Return the response with the form context
    return render(request, 'registration/signup.html', {'form': form})




# sending friend request


@login_required
def send_friend_request(request, user_id):
    receiver = get_object_or_404(User, id=user_id)
    FriendRequest.objects.create(sender=request.user, receiver=receiver)
    # return JsonResponse({'success': True})






# accepting friend request


@login_required
def accept_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id)
    Friendship.objects.create(user1=friend_request.sender, user2=friend_request.receiver)
    friend_request.delete()
    return JsonResponse({'success': True})






# rejecting friend request


@login_required
def reject_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id)
    friend_request.delete()
    return JsonResponse({'success': True})




# friend requests page
@login_required
def friend_requests(request):
    requests = FriendRequest.objects.filter(receiver=request.user)
    return render(request, 'Friend_Request/friend_requests.html', {'friend_requests': requests})



@login_required
def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("home")
        
    else:
        form = PostForm()

    return render (request, 'create_post.html', {"form":form})


# VIEW TO ADD A COMMENT

@login_required
def add_comment(request, post_id):
    if request.method == 'POST':
        name = request.POST.get('name')
        body = request.POST.get('body')
        comment = Comment.objects.create(post_id=post_id, name=name, body=body)
        return JsonResponse({
            'success': True,
            'name': comment.name,
            'body': comment.body,
            'date_added': comment.date_added.strftime("%Y-%m-%d %H:%M:%S"),
        })


# view for profile picture submission

@login_required
def update_profile(request, username):
    user = get_object_or_404(User, username=username)

    if request.method == "POST":
        # Handle the forms
        profile_form = ProfileForm(request.POST, request.FILES, instance=user.profile)  # Ensure request.FILES is passed

        if profile_form.is_valid():
            profile_form.save()  # Update profile (profile_picture, bio, etc.)
            messages.success(request, f'{user.username}, your profile has been updated.')
            return redirect('profile_view', username=user.username)
        else:
            messages.error(request, 'There was an error updating your profile. Please try again.')
    else:
        # If GET request, create empty form instances
        profile_form = ProfileForm(instance=user.profile)

    context = {
        "profile_form": profile_form,
        "user": user
    }

    return render(request, 'update_profile.html', context)

# @login_required(login_url='login')
# def profile_view(request, username):
#     user = get_object_or_404(User, username=username)
#     return render(request, 'profile.html', {'user': user})




@login_required
def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    posts_count = user.posts.count()  # Count the user's posts
    friendships = Friendship.objects.filter(user1=user) | Friendship.objects.filter(user2=user)
    friends = list(set(friendship.user2 if friendship.user1 == user else friendship.user1 for friendship in friendships))
    friends_count = len(friends)
    profile_user = get_object_or_404(User, username=username)

    context = {
        'user': user,
        'posts_count': posts_count,
        'friends_count': friends_count,
        'profile_user': profile_user,  # Ensure the correct profile_user is passed
    }
    return render(request, 'profile.html', context)



@login_required
def user_logout(request):
    logout(request)
    return render(request, 'logout.html')


def delete_post(request, post_id):
    if request.method == "POST":
        try:
            post = Post.objects.get(id=post_id, author=request.user)
            post.delete()
            return JsonResponse({'success': True})
        except Post.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Post not found.'}, status=404)
    return JsonResponse({'success': False}, status=400)

def update_username(request, username):
    user = get_object_or_404(User, username=username)
    if request.method == 'POST':
        form = UsernameForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile_view', username=user.username)
    else:
        form = UsernameForm(instance=user)
    return render(request, 'update_username.html', {'form': form})

def update_pronouns(request, username):
    user = get_object_or_404(User, username=username)
    if request.method == 'POST':
        form = PronounsForm(request.POST, instance=user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile_view', username=user.username)
    else:
        form = PronounsForm(instance=user.profile)
    return render(request, 'update_pronouns.html', {'form': form})

def update_bio(request, username):
    user = get_object_or_404(User, username=username)
    if request.method == 'POST':
        form = BioForm(request.POST, instance=user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile_view', username=user.username)
    else:
        form = BioForm(instance=user.profile)
    return render(request, 'update_bio.html', {'form': form})



@require_http_methods(["DELETE"])
def unfriend_view(request, user_id):
    friendship = Friendship.objects.filter(
        (Q(user1=request.user) & Q(user2_id=user_id)) |
        (Q(user1_id=user_id) & Q(user2=request.user))
    ).first()

    if friendship:
        friendship.delete()
        return JsonResponse({'message': 'Unfriended successfully.'}, status=200)
    else:
        return JsonResponse({'error': 'Friendship does not exist.'}, status=404)



@login_required
def friends_view(request):
    friendships = Friendship.objects.filter(user1=request.user) | Friendship.objects.filter(user2=request.user)
    friends = []

    for friendship in friendships:
        if friendship.user1 == request.user:
            friends.append(friendship.user2)
        else:
            friends.append(friendship.user1)

    return render(request, 'friends.html', {'friends': friends})


@login_required
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == 'POST':
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
            is_liked = False
        else:
            post.likes.add(request.user)
            is_liked = True

        # Return the total number of likes
        return JsonResponse({
            'is_liked': is_liked,
            'total_likes': post.total_likes()
        })
    

from django.shortcuts import render
from moviepy.editor import VideoFileClip
from .models import Post
def shorts_view(request):
    shorts = []
    current_index = int(request.GET.get('index', 0))  # Get the index from the URL or default to 0

    for post in Post.objects.filter(video__isnull=False, is_short=True):
        if post.video:
            clip = VideoFileClip(post.video.path)
            if clip.duration < 60:
                shorts.append(post)

    # Ensure current_index is within bounds
    current_index = max(0, min(current_index, len(shorts) - 1))

    # Get the current short based on the index
    current_short = shorts[current_index] if shorts else None

    return render(request, 'shorts.html', {'shorts': shorts, 'current_index': current_index, 'current_short': current_short})



@login_required
def upload_view(request):
    if request.method == 'POST':
        video_file = request.FILES.get('video')
        if video_file:
            post = Post(author=request.user, video=video_file, is_short=True)  # Set is_short to True
            post.save()
            return redirect('shorts_view')

    return render(request, 'upload.html')



# MESSAGING VIEWS

from django.views import View
from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Message

class MessagesView(View):
    def get(self, request):
        friendships = request.user.friend1.all() | request.user.friend2.all()
        friends = list(set(friendship.user2 if friendship.user1 == request.user else friendship.user1 for friendship in friendships))

        return render(request, 'messages.html', {'friends': friends})

class ChatRoomView(View):
    def get(self, request, username):
        friend = get_object_or_404(User, username=username)
        user = request.user
        messages = Message.objects.filter(
            (Q(sender=user) & Q(receiver=friend)) |
            (Q(sender=friend) & Q(receiver=user))
        ).order_by('timestamp')

        return render(request, 'chat_room.html', {
            'username': friend.username,
            'messages': messages
        })


@login_required
def bookmarks_view(request):
    # Fetch the posts bookmarked by the user
    bookmarked_posts = Bookmark.objects.filter(user=request.user)
    return render(request, 'bookmarks.html', {'bookmarked_posts': bookmarked_posts})


logger = logging.getLogger(__name__)

@login_required
def toggle_bookmark(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        action = request.POST.get('action')
        
        post = get_object_or_404(Post, id=post_id)

        # Check if the user has already bookmarked the post
        if action == 'bookmark':
            # Create a new bookmark
            Bookmark.objects.create(user=request.user, post=post)
        elif action == 'unbookmark':
            # Remove the bookmark
            Bookmark.objects.filter(user=request.user, post=post).delete()

        return JsonResponse({'success': True})


@login_required
def cards_view(request):
    # Get the logged-in user's cards
    cards = Card.objects.filter(user=request.user)
    
    # Handle card creation for the logged-in user
    if request.method == 'POST':
        form = CardForm(request.POST, request.FILES)
        if form.is_valid():
            new_card = form.save(commit=False)
            new_card.user = request.user  # Associate the card with the logged-in user
            new_card.save()
            return redirect('cards')  # Redirect back to the logged-in user's cards page
    else:
        form = CardForm()

    # Pass the logged-in user as profile_user to the context
    return render(request, 'cards.html', {
        'cards': cards,
        'form': form,
        'profile_user': request.user,  # Display the logged-in user's profile
    })

@login_required
def other_user_cards_view(request, username):
    # Get the other user whose cards we want to show
    profile_user = get_object_or_404(User, username=username)
    
    # Get the cards for the profile_user
    cards = Card.objects.filter(user=profile_user)
    
    return render(request, 'cards.html', {
        'cards': cards,
        'profile_user': profile_user,  # Display the other user's profile
    })
