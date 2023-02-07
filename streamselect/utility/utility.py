import re
from io import BytesIO
import base64, uuid
from django.utils.crypto import get_random_string

from django.core.files.uploadedfile import InMemoryUploadedFile
# importing the necessary libraries
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

# defining the function to convert an HTML file to a PDF file
def html_to_pdf(template_src, context_dict={}):
     template = get_template(template_src)
     html  = template.render(context_dict)
     result = BytesIO()
     pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
     if not pdf.err:
         return HttpResponse(result.getvalue(), content_type='application/pdf')
     return None


def remove_spaces_with_underscore(s):
    s = re.sub(r"\s+", '-', s)
    return s


def getsize(f):
    f.seek(0)
    f.read()
    s = f.tell()
    f.seek(0)
    return s

def base64StringToInMemoryImage(b64String):
    textData = base64.b64decode(b64String)
    strIO = BytesIO(textData)
    size = getsize(strIO)
    uuid = get_random_string(8)
    name = '%s.%s' % (uuid, 'jpg')
    image = InMemoryUploadedFile(strIO, 'image', name, 'image/jpg', size, 'utf-8')
    return image
