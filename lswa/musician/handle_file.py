import os.path
def handle_uploaded_file(f, name):
    with open(name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
def find_ext(name):
    extension = os.path.splitext(name)[1]
    return extension
