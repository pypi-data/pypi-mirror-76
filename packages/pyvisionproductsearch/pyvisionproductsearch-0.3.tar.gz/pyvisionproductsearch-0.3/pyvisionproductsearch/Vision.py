from google.cloud import vision
from google.cloud.vision import types
import io

def detectLabels(file_path=None, image_uri=None):

    if bool(file_path) == bool(image_uri):
        raise Exception(
            "Must provide one of either a file path or an image uri")
    
    client = vision.ImageAnnotatorClient()

    if file_path:
        with io.open(file_path, 'rb') as image_file:
            content = image_file.read()
            image = vision.types.Image(content=content)
    else:
        image_source = vision.types.ImageSource(image_uri=image_uri)
        image = vision.types.Image(source=image_source)

    # Performs label detection on the image file
    response = client.label_detection(image=image)
    return response.label_annotations
    # objects = client.object_localization(
    #     image=image).localized_object_annotations


def detectObjects(file_path=None, image_uri=None):

    if bool(file_path) == bool(image_uri):
        raise Exception(
            "Must provide one of either a file path or an image uri")
    
    client = vision.ImageAnnotatorClient()

    if file_path:
        with io.open(file_path, 'rb') as image_file:
            content = image_file.read()
            image = vision.types.Image(content=content)
    else:
        image_source = vision.types.ImageSource(image_uri=image_uri)
        image = vision.types.Image(source=image_source)

    # Performs label detection on the image file
    objects = client.object_localization(
        image=image).localized_object_annotations
    return objects

# print('Number of objects found: {}'.format(len(objects)))
# for object_ in objects:
#     print('\n{} (confidence: {})'.format(object_.name, object_.score))
#     print('Normalized bounding polygon vertices: ')
#     for vertex in object_.bounding_poly.normalized_vertices:
#         print(' - ({}, {})'.format(vertex.x, vertex.y))