from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def home(request):
    if 'username' in request.session:
        del request.session['username']
    return render(request, "dashboard.html", locals())
