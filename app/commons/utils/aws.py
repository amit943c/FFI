#Copyright 2018 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#PDX-License-Identifier: MIT-0 (For details, see https://github.com/awsdocs/amazon-rekognition-developer-guide/blob/master/LICENSE-SAMPLECODE.)
import os
import time
import boto3
import base64
import uuid
from botocore.config import Config
from botocore.exceptions import ClientError
from PIL import Image, ExifTags

def create_collection(collection_id):

    client=boto3.client('rekognition')

    #Create a collection
    print('Creating collection:' + collection_id)
    response=client.create_collection(CollectionId=collection_id)
    print('Collection ARN: ' + response['CollectionArn'])
    print('Status code: ' + str(response['StatusCode']))
    print('Done...')
    
def main():
    collection_id='Collection'
    create_collection(collection_id)

if __name__ == "__main__":
    main()

def s3_image_upload(file_path, region=None, bucket_name="new-test-bkt-1"):
    print(file_path)
    s3_client = create_boto_client_s3()
    im = Image.open(file_path)
    width, height = im.size
    im = im.convert('RGB')
    im = im.resize((400, int(height*400/width)))
    im.save(file_path)

    object_name = file_path.split("/")[-1]
    try:
        response = s3_client.upload_file(file_path, bucket_name, object_name)
    except ClientError as e:
        print(e)
        return False, "", ""
    return True, object_name, file_path


def resize_image(object_name, path_prefix):
    file_path = path_prefix + object_name
    im = rotate_exif(file_path)
    width, height = im.size
    # print("THIFJGKASNg", width, height)
    im = im.convert('RGB')

    im = im.resize((200, int(height*200/width)))
    im.save(file_path)

    return

def rotate_exif(file_path):
    image = Image.open(file_path)

    for orientation in ExifTags.TAGS.keys():
        if ExifTags.TAGS[orientation]=='Orientation':
            break
    
    exif = image._getexif()

    try:
        if exif[orientation] == 3:
            image = image.rotate(180, expand=True)
        elif exif[orientation] == 6:
            image = image.rotate(270, expand=True)
        elif exif[orientation] == 8:
            image = image.rotate(90, expand=True)
    except Exception as e:
        print(e)

    return image

def s3_create_bucket(region=None, bucket_name=None):
    region = os.getenv("AWS_REGION")
    object_name = "{}.jpg".format(uuid.uuid4())
    s3_client = create_boto_client_s3()
    try:
        location = {'LocationConstraint': region}
        s3_client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration=location)
    except ClientError as e:
        print(e)
        return False
    return True

def aws_index_image(object_name, collection_id="collection_id", region=None, bucket_name="new-test-bkt-1"):
    client = create_boto_client_aws()
    try:
        response = client.index_faces(
            CollectionId=collection_id,
            Image={'S3Object':{'Bucket':bucket_name,'Name':object_name}},
            ExternalImageId=object_name,
            MaxFaces=1,
            QualityFilter="AUTO",
            DetectionAttributes=['ALL']
        )
    except ClientError as e:
        print(e)
        return False
    return True

def create_boto_client_aws():
    my_config = Config(
        region_name = 'us-west-2',
        signature_version = 'v4',
        retries = {
            'max_attempts': 10,
            'mode': 'standard'
        }
    )
    client = boto3.client('rekognition', config=my_config)

    return client

def create_boto_client_s3():
    region = os.getenv("AWS_REGION")
    s3_client = boto3.client('s3', region_name=region)

    return s3_client

def search_face(object_name, collection_id="collection_id", bucket_name="new-test-bkt-1", threshold=90, max_faces=10):
    start_time = time.time()
    client = create_boto_client_aws()
    base_path = os.getenv("PATH_PREFIX_CAMERA_IMG")
    file_path = base_path + object_name
    
    response = {}
    with open(file_path, 'rb') as image:
        response = client.search_faces_by_image(
            CollectionId=collection_id,
            Image={'Bytes': image.read()},
            FaceMatchThreshold=threshold,
            MaxFaces=max_faces
            )
    faces = []
    start_time_2 = time.time()
    print("Face search time: ", start_time_2 - start_time)
    try:
        face_matches = response['FaceMatches']
        for face in face_matches:
            img_path = face['Face']['ExternalImageId']
            faces.append(
                    {
                        'similarity': format(face['Similarity'], ".2f"), 
                        'face_image': "celeb/" + img_path
                    }
                )
    except Exception as e:
        print(e)
    start_time_3 = time.time()
    print("Image download time: ", start_time_3 - start_time_2)
    return faces

def create_collection(collection_id):
    client = create_boto_client_aws()
    try:
        response = client.create_collection(CollectionId=collection_id)
    except ClientError as e:
        print(e)
        return False

    return True

