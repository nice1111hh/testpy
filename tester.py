# forms.py
from django import forms

class UploadFileForm(forms.Form):
    files = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

# views.py
from django.shortcuts import render
from .forms import UploadFileForm

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            files = request.FILES.getlist('files')
            for f in files:
                # Vulnerable: Assuming all files are valid if the last one is valid
                handle_uploaded_file(f)
            return render(request, 'upload_success.html')
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})

def handle_uploaded_file(f):
    with open(f.name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

# upload.html
<form method="post" enctype="multipart/form-data">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Upload</button>
</form>
