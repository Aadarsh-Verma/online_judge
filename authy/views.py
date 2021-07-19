from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from authy.forms import UpdateUserForm, UpdateProfileForm, SignUpForm
from authy.models import Profile
from judge.models import Submission


def SignUpView(request):
    print("sign up called")
    if request.method == "POST":
        form = SignUpForm(request.POST)
        print(form)
        if form.is_valid():
            print("form valid")
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            email = form.cleaned_data.get('email')
            curr_user = User.objects.create_user(username=username, password=password, email=email)
            new_form = form.save(commit=False)
            new_form.user = curr_user
            new_form.save()
            return redirect('login')
    form = SignUpForm()
    return render(request, 'authy/Registration.html', {'form': form})


@login_required
def EditProfileView(request):
    if request.method == "POST":
        user_form = UpdateUserForm(request.POST, request.FILES, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            email = user_form.cleaned_data.get('email')
            new_form = profile_form.save()
            new_form.email = email
            new_form.save()
            Profile.objects.get(user__username=user_form.cleaned_data.get('username')).refresh_from_db()
            print(Profile.objects.get(user__username=user_form.cleaned_data.get('username')))
            return redirect('viewProfile')
    user_form = UpdateUserForm(instance=request.user)
    profile_form = UpdateProfileForm(instance=request.user.profile)
    context = {'user_form': user_form, 'profile_form': profile_form}
    return render(request, 'authy/EditProfileForm.html', context)


@login_required
def ProfileView(request, pk):
    profile = Profile.objects.get(user_id=pk)
    submissions = Submission.objects.filter(user_id=pk)[0:5]
    context = {
        'object': profile,
        'submissions': submissions,
    }
    return render(request, 'authy/profile_detail.html', context)
