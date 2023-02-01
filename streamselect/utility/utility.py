import re
from io import BytesIO
import base64, uuid
from django.utils.crypto import get_random_string

from django.core.files.uploadedfile import InMemoryUploadedFile



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
