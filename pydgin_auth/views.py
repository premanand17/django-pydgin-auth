'''Manage views for pydgin_auth'''
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.template.context import RequestContext
from pydgin_auth.forms import PydginUserCreationForm
import os.path
from django.contrib.auth.decorators import login_required
from rest_framework.authtoken.models import Token
import logging
from django.conf import settings
logger = logging.getLogger(__name__)


def login_home(request):
    '''renders login home page'''
    return render(request, 'registration/login.html')


def permission_denied(request):
    '''renders permission denied page'''
    return render(request, 'registration/permission_denied.html')


@login_required(login_url='/accounts/login/')
def profile(request):
    '''renders user profile page'''
    try:
        token = Token.objects.get_or_create(user=request.user)
    except Token.DoesNotExist:
        logging.debug('Exception while creating tokens')
        pass

    # context = RequestContext(request, {'request': request, 'user': request.user, 'api_key': token})
    request_context = RequestContext(request)
    request_context.push({"api_key": token})
    return render(request, 'registration/profile.html', context_instance=request_context)


def registration_complete(request):
    '''renders registration complete page'''
    return render(request, 'registration/registration_form_complete.html')


def register(request):
    '''register a new user after agreeing to terms and condition'''
    # read the terms and conditions file
    curr_path = os.path.dirname(os.path.realpath(__file__))
    with open(curr_path + "/templates/registration/IMB_TOC_draft.html", "r", encoding="utf-8") as myfile:
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
    token['terms_n_condition'] = terms_n_condition_txt

    try:
        base_html_dir = settings.BASE_HTML_DIR
    except AttributeError:
        base_html_dir = ''

    token['basehtmldir'] = base_html_dir

    request_context = RequestContext(request)
    request_context.push({"token": token})

    return render(request, 'registration/registration_form.html', token)
