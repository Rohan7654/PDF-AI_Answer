from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse

def upload_pdf(request):
    if request.method == 'POST' and request.FILES.get('pdf_file', False):
        pdf_file = request.FILES['pdf_file']
        if not pdf_file.name.endswith('.pdf'):
            return HttpResponse('File is not PDF type.')
        fs = FileSystemStorage()
        filename = fs.save(pdf_file.name, pdf_file)
        file_path = fs.path(filename)
        from utils import process_pdf_questions
        processed_pdf = process_pdf_questions(file_path)
        # Assuming the processed_pdf is a file-like object
        fs = FileSystemStorage()
        new_filename = fs.save("processed_" + pdf_file.name, processed_pdf)
        file_url = fs.url(new_filename)
        return render(request, 'pdf_upload/upload_success.html', {'uploaded_file_url': file_url})
    else:
        return render(request, 'pdf_upload/upload.html')
