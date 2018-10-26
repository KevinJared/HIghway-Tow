from django.shortcuts import render,redirect,get_object_or_404
from hightow.models import Post, Profile
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404,HttpResponseRedirect
from .forms import NewPostForm, UserForm, ProfileForm,CommentForm,NewsLetterForm
from django.contrib.auth.decorators import login_required
from .models import Room,NewsLetterRecipients
from .email import send_welcome_email


def index(request):
    user = request.user
    posts = Post.objects.all()
    if request.method == 'POST':
        form = NewsLetterForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['your_name']
            email = form.cleaned_data['email']

            recipient = NewsLetterRecipients(name = name,email =email)
            recipient.save()
            send_welcome_email(name,email)

            HttpResponseRedirect('index')
    else:
        form = NewsLetterForm()
    return render(request, 'index.html',{"letterForm":form}, locals())

@login_required(login_url='/accounts/login/')
def all_rooms(request):
    rooms = Room.objects.all()
    return render(request, 'chat/index.html', {'rooms': rooms})

@login_required(login_url='/accounts/login/')
def room_detail(request, slug):
    room = Room.objects.get(slug=slug)
    return render(request, 'chat/room_detail.html', {'room': room})

    

@login_required(login_url='/accounts/login/')
def new_post(request):
    current_user = request.user
    if request.method == 'POST':
        form = NewPostForm(request.POST, request.FILES)

        if form.is_valid():
            post = form.save(commit=False)
            post.user = current_user
            post.save()
            return redirect('index')
    else:
        form = NewPostForm()
    return render(request, 'new_post.html', {"form":form})

@login_required(login_url='/accounts/login/')
def profile(request,user_id=None):
    if user_id == None:
        user_id=request.user.id
    current_user = User.objects.get(id = user_id)
    user = current_user
    images = Post.objects.filter(user=current_user)
    profile = Profile.objects.all()
    return render(request, 'profile.html', locals())

@login_required
def userprofile(request, user_id):
    users = User.objects.get(id=user_id)
    profile = Profile.objects.get(user=users)
    images = Post.objects.filter(user=users)
    posts = len(Image.objects.filter(user=users))

    return render(request, 'profile/userprofile.html', {"user": users, "profile": profile, "images": images})


@login_required(login_url='/accounts/login')
def updateprofile(request):
	if request.method == 'POST':
		form = ProfileForm(request.POST,request.FILES, instance=request.user.profile)
		if form.is_valid():
			form.save()
			return redirect('profile')

	else:
			form = ProfileForm()
	return render(request, 'updateprofile.html',{"form":form })

def search_results(request):

    if 'profile' in request.GET and request.GET["profile"]:
        search_term = request.GET.get("profile")
        searched_profiles = Profile.search_by_user(search_term)
        message = f"{search_term}"

        return render(request, 'search.html',{"message":message,"profile": searched_profiles})

    else:
        message = "You haven't searched for any term"
        return render(request, 'search.html',{"message":message})

def newsletter(request):
    name = request.POST.get('your_name')
    email = request.POST.get('email')

    recipient = NewsLetterRecipients(name=name, email=email)
    recipient.save()
    send_welcome_email(name, email)
    data = {'success': 'You have been successfully added to mailing list'}
    return JsonResponse(data)
