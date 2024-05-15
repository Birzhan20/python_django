from django.core.files.storage import FileSystemStorage
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest
from django.shortcuts import render


def process_get_view(request: HttpRequest) -> HttpResponse:
    a = request.GET.get("a", "")
    b = request.GET.get("b", "")
    result = a + b
    context = {
        "a": a,
        "b": b,
        "result": result,
    }
    return render(request, "requestdataapp/request-query-params.html", context=context)


def user_form(request: HttpRequest) -> HttpResponse:
    return render(request, "requestdataapp/user-bio-form.html")


def handle_file_uoload(request: HttpRequest) -> HttpResponse:
    if request.method == "POST" and request.FILES.get("myfile"):
        myfile = request.FILES["myfile"]

        max_size_bytes = 1048576
        if myfile.size > max_size_bytes:
            return HttpResponseBadRequest("The file size exceeds the limit (1 MB).")

        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        print("saved file", filename)
    return render(request, "requestdataapp/file-upload.html")
