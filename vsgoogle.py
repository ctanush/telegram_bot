import io
from google.oauth2 import service_account
from google.cloud import vision
from Keys import Google_api_key

credentials = service_account.Credentials.from_service_account_file(
    Google_api_key)

client = vision.ImageAnnotatorClient(credentials=credentials)

def read_image(filepath):
    with io.open(filepath, 'rb') as image_file:
        content = image_file.read()
    image = vision.types.Image(content=content)
    response = client.document_text_detection(image=image)
    document = response.full_text_annotation.text
    
    if document == '':
        return "No Text Found"
    else:
        return document