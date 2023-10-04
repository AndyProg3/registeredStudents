from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render
from django.shortcuts import redirect
from django.utils.html import escape
import bleach
import hashlib

from registeredStudents import settings

from registeredStudents.libs import wiregrassLogin
from registeredStudents.libs import data
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def index(request):
    if request.COOKIES.get("authtoke"):
        text = 'logged in'
        str = hashlib.sha256(text.encode('utf-8'))
        text_hashed = str.hexdigest()
        if request.COOKIES["authtoke"] == text_hashed:
            return redirect('/students')

    context = settings.DEFAULT_CONTEXT
    
    response = render(request, "login.html", context)
    return response

def students(request):
    if request.COOKIES.get("authtoke"):
        text = 'logged in'
        str = hashlib.sha256(text.encode('utf-8'))
        text_hashed = str.hexdigest()
        if request.COOKIES["authtoke"] != text_hashed:
            return redirect('/')

    context = settings.DEFAULT_CONTEXT

    termGet = None
    majorsGet = None
    if(request.method == "GET"):
        if request.GET.get('Term'):
            termGet = request.GET["Term"]
        
        if request.GET.get('Majors'):
            majorsGet = request.GET.getlist('Majors')

        context["Students"] = data.getData(termGet, majorsGet)
        

    context["Terms"] = data.getTerms()
    context["Majors"] = data.getMajors()
    context["termGet"] = termGet
    context["majorsGet"] = majorsGet

    response = render(request, "register_students.html", context)

    return response

@csrf_exempt
def login(request):
    returnMsg = None

    if request.method == "POST":
        print("POSTED")
        
        if request.GET.get('action'):
            action = request.GET["action"]

            if action == "login":
                print("\nLOGGING IN")

        uname = None
        pw = None

        if request.POST.get('userName'):
            uname = bleach.clean(request.POST["userName"],
                       tags=bleach.ALLOWED_TAGS,
                       attributes=bleach.ALLOWED_ATTRIBUTES, 
                       styles=bleach.ALLOWED_STYLES, 
                       strip=False, strip_comments=True)
            
        if request.POST.get('pw'):
            pw = bleach.clean(request.POST["pw"], 
                       tags=bleach.ALLOWED_TAGS,
                       attributes=bleach.ALLOWED_ATTRIBUTES, 
                       styles=bleach.ALLOWED_STYLES, 
                       strip=False, strip_comments=True)

        if wiregrassLogin.login(uname, pw) == 1:
            returnMsg = "success"
        else:
            returnMsg = "failed"

        response = HttpResponse(returnMsg)

        if returnMsg == "success":
            text = 'logged in'
            str = hashlib.sha256(text.encode('utf-8'))
            text_hashed = str.hexdigest()
            response.set_cookie("authtoke", text_hashed, max_age=864000)
        else:
            response.delete_cookie("authtoke")

    return response

