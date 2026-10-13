from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse
from.models import *
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.core.mail import send_mass_mail

# @login_required(login_url='login')
def index(request):
    user = User.objects.all()
    clubs = Club.objects.all()
    startups = Startup.objects.all()
    return render(request, 'index.html',{'user': user ,'clubs':clubs,'startups':startups})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Check in default User model
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')  # Replace with the URL you want to redirect to
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'login.html')

def signup(request):
    if request.method == 'POST':
        form_type = request.POST.get('form_type')
        if form_type == 'student':
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            roll_no = request.POST['roll_no']
            reg_no = request.POST['reg_no']
            year = request.POST['year']
            dep = request.POST['dep']
            email = request.POST['email']
            ph_no = request.POST['ph_no']
            password = request.POST['password']
            profile_pic = request.FILES.get('profile_pic')
            hostel = request.POST['hostel']
            user = User.objects.create_user(username=first_name+' '+last_name,first_name=first_name,last_name=last_name,password=password,email=email,roll_no=roll_no,reg_no=reg_no,dep=dep,year=year,profile_pic=profile_pic,ph_no=ph_no,hostel=hostel,people=form_type)
            send_mail(
                'Welcome to CIET Talent Hub😊',  # No newline in the subject
                f"User name: {first_name}\nYour password is: {password}\n\ndon't share this with anyone",
                'aakilesh953@gmail.com',
                [email],
                fail_silently=False
            )

            messages.success(request, "Signup successful! You can now log in.")
            return redirect("login")
        if form_type == 'faculty':
            username = request.POST.get('username')
            user_id = request.POST.get('user_id')
            dep = request.POST.get('dep')
            password = request.POST.get('password')
            email = request.POST.get('email')
            ph_no = request.POST.get('ph_no')
            profile_pic = request.FILES.get('profile_pic')
            linkedin = request.POST.get('linkedin')

            # Save the data into the model
            user = User.objects.create_user(username=username,password=password,email=email,roll_no=user_id,dep=dep,profile_pic=profile_pic,ph_no=ph_no,people=form_type,linkedin=linkedin)
            send_mail(
                'Welcome to CIET Talent Hub😊',  # No newline in the subject
                f"User name: {username}\nYour password is: {password}\n\ndon't share this with anyone",
                'aakilesh953@gmail.com',
                [email],
                fail_silently=False
            )
            messages.success(request, "Signup successful! You can now log in.")
            return redirect("login")
    return render(request, 'signup.html')

def logout_view(request):
    logout(request)  # This will log out the user
    return redirect('login')

def base(request):
    return render(request, 'base.html')

@login_required
def profile(request):
    user = request.user

    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        # Handle User Information Update
        if form_type == 'user_info':
            user.username = request.POST.get('username', user.username)
            user.roll_no = request.POST.get('roll_no', user.roll_no)
            user.reg_no = request.POST.get('reg_no', user.reg_no)
            user.email = request.POST.get('email', user.email)
            user.dep = request.POST.get('dep', user.dep)
            user.year = request.POST.get('year', user.year)
            user.ph_no = request.POST.get('ph_no', user.ph_no)  # Ensure input is numeric
            user.linkedin = request.POST.get('linkedin', user.linkedin)
            user.github = request.POST.get('github', user.github)
            user.filed = request.POST.get('filed', user.filed)
            user.hostel = request.POST.get('hostel', user.hostel)

            # Update profile picture if uploaded
            if 'profile_pic' in request.FILES:
                user.profile_pic = request.FILES['profile_pic']

            user.save()

    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        # Handle Certificate Form
        if form_type == 'certificate':
            googledrive_link = request.POST.get('googledrive_link')
            about_certificate = request.POST.get('about_certificate')
            Certificate.objects.create(
                student=request.user,
                googledrive_link=googledrive_link,
                about_certificate=about_certificate,
                uploaded_at=now()
            )

        # Handle Skill Form
        elif form_type == 'skill':
            skill_name = request.POST.get('skill_name')
            Skill.objects.create(
                student=request.user,
                skill_name=skill_name,
                added_at=now()
            )

        # Handle Timeline Post Form
        elif form_type == 'timeline':
            content = request.POST.get('content')
            media_link = request.POST.get('media_link')
            Timeline.objects.create(
                student=request.user,
                content=content,
                media_link=media_link,
                created_at=now()
            )

        return redirect('profile')  # Refresh page after submission

    # Fetch existing data
    certificates = Certificate.objects.filter(student=request.user)
    skills = Skill.objects.filter(student=request.user)
    timeline_posts = Timeline.objects.filter(student=request.user)

    return render(request, 'profile.html', {
        'certificates': certificates,
        'skills': skills,
        'timeline_posts': timeline_posts,
        'user': request.user,
    })

@login_required
def post(request):
    posts = Post.objects.all().order_by('-created_at')  # Fetch posts, most recent first

    form_type = request.POST.get('form_type')
    if request.method == 'POST':
        if form_type == 'post':
            content = request.POST.get('content', '')
            image = request.FILES.get('image')
            video = request.FILES.get('video')

            # Check if the post is an update
            post_id = request.POST.get('post_id')  # Optional for updates
            if post_id:
                post_instance = Post.objects.get(id=post_id)
                post_instance.content = content
                post_instance.image = image or post_instance.image
                post_instance.video = video or post_instance.video
                post_instance.save()

                # Send email notifications to all users
                send_update_emails(post_instance)
            else:
                # Create a new post
                Post.objects.create(user=request.user, content=content, image=image, video=video)

            return redirect('post')

        if form_type == 'story':
            """View to handle story upload."""
            if request.method == 'POST' and request.FILES.get('media'):
                media_file = request.FILES['media']
                story = Story.objects.create(
                    user=request.user,
                    media=media_file
                )
                story.save()
                return redirect('post')

    # Fetch only stories that haven't expired
    current_time = now()
    active_stories = Story.objects.filter(expiry_time__gte=current_time)

    return render(request, 'post.html', {'posts': posts, 'stories': active_stories})


def send_update_emails(post_instance):
    """Send email notifications when a post is updated."""
    subject = f"Post Updated by {post_instance.user.username}"
    message = f"""
    Hello,
    A post has been updated on the platform
    Updated Content:
    {post_instance.content}
    Check it out now!
    Best Regards,Your Team """
    # Get all user emails
    recipient_list = User.objects.exclude(email='').values_list('email', flat=True)

    # Prepare email tuples
    email_messages = [
        (subject, message, 'aakilesh953@gmail.com', [email]) for email in recipient_list
    ]

    # Send emails
    send_mass_mail(email_messages, fail_silently=False)

def fields(request):
    return render(request, 'fields_list.html')

def profile_list(request):
    field = request.POST['field']
    data = User.objects.filter(filed=field)
    count = User.objects.filter(filed=field).count()
    context={
        'data':data,
        'count':count,
        'field':field,
    }
    return render(request, 'profile_list.html', context)

def profile_view(request, user_id):
    # Get the specific user
    user = get_object_or_404(User, id=user_id)
    
    # Filter related data
    certificates = Certificate.objects.filter(student=user)
    skills = Skill.objects.filter(student=user)
    timeline_posts = Timeline.objects.filter(student=user).order_by('-created_at')  # Ordered by most recent
    
    # Pass the data to the template
    return render(request, 'profile_view.html', {
        'user': user,
        'certificates': certificates,
        'skills': skills,
        'timeline_posts': timeline_posts,
    })

# Club views
def add_club(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        logo = request.FILES.get('logo')
        head = request.POST.get('head')
        email = request.POST.get('email')
        Club.objects.create(name=name, logo=logo, head=head, email=email)
        return redirect('club_list')  # Redirect to the club list page
    return render(request, 'add_club.html')

def club_list(request):
    clubs = Club.objects.all()
    return render(request, 'club_list.html', {'clubs': clubs})

# Startup views
def add_startup(request):
    if request.method == 'POST':
        company_name = request.POST.get('company_name')
        logo = request.FILES.get('logo')
        founder_name = request.POST.get('founder_name')
        founder_profile_pic = request.FILES.get('founder_profile_pic')
        types_of_company = request.POST.get('types_of_company')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        role_of_company = request.POST.get('role_of_company')
        Startup.objects.create(
            company_name=company_name,
            logo=logo,
            founder_name=founder_name,
            founder_profile_pic=founder_profile_pic,
            types_of_company=types_of_company,
            email=email,
            phone=phone,
            role_of_company=role_of_company,
        )
        return redirect('startup_list')  # Redirect to the startup list page
    return render(request, 'add_startup.html')

def startup_list(request):
    startups = Startup.objects.all()
    return render(request, 'startup_list.html', {'startups': startups})

def startup_detail(request, id):
    startup = get_object_or_404(Startup, id=id)
    return render(request, 'startup_detail.html', {'startup': startup})

def dep(request):
    return render(request, 'dep.html')

def dep_list(request):
    field = request.POST['field']
    data = User.objects.filter(dep=field)
    count = User.objects.filter(dep=field).count()
    context={
        'data':data,
        'count':count,
        'field':field,
    }
    return render(request, 'dep_list.html', context)




