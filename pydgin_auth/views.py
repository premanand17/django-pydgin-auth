from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.template.context import RequestContext
from pydgin_auth.forms import PydginUserCreationForm
import os.path
from django.contrib.auth.decorators import login_required
from rest_framework.authtoken.models import Token


def login_home(request):
    context = RequestContext(request, {'request': request, 'user': request.user})
    return render_to_response('registration/login.html', context_instance=context)


def permission_denied(request):
    context = RequestContext(request, {'request': request, 'user': request.user})
    return render_to_response('registration/permission_denied.html', context_instance=context)


@login_required(login_url='/accounts/login/')
def profile(request):
    try:
        token = Token.objects.get_or_create(user=request.user)
    except Token.DoesNotExist:
        print('Exception while creating tokens')
        pass

    print(request.user.username)
    print(token)
    context = RequestContext(request, {'request': request, 'user': request.user, 'api_key': token})
    return render_to_response('registration/profile.html', context_instance=context)


def registration_complete(request):
    print("Registration complete called")
    return render_to_response('registration/registration_form_complete.html')


def register(request):
    print('register called')
    # read the terms and conditions file
    curr_path = os.path.dirname(os.path.realpath(__file__))
    with open(curr_path + "/templates/registration/IMB_TOC_draft.html", "r") as myfile:
        terms_n_condition_txt = myfile.read().replace('\n', '<br/>')

    if request.method == 'POST':
        form = PydginUserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            new_user.backend = 'django.contrib.auth.backends.ModelBackend'
            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'],
                                    email=form.cleaned_data['email'],
                                    is_terms_agreed=form.cleaned_data['is_terms_agreed'])
            login(request, new_user)
            messages.info(request, "Thanks for registering. You are now logged in.")
            return HttpResponseRedirect('/')

    else:
        form = PydginUserCreationForm()
    token = {}
    token.update(csrf(request))
    token['form'] = form
    token['terms_n_condition'] = terms_n_condition_txt

    return render_to_response('registration/registration_form.html', token)
