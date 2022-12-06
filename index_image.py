import os
import time
import boto3
import base64
import uuid
from botocore.config import Config
from botocore.exceptions import ClientError
from PIL import Image, ExifTags


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


def s3_image_upload(file_path, region=None, bucket_name="new-test-bkt-1"):
    print(file_path)
    s3_client = create_boto_client_s3()
    im = Image.open(file_path)
    width, height = im.size
    im = im.convert('RGB')
    im = im.resize((400, int(height*400/width)))
    im.save(file_path)

    object_name = file_path.split("/")[-1].lower()
    try:
        response = s3_client.upload_file(file_path, bucket_name, object_name)
    except ClientError as e:
        print(e)
        return False, "", ""
    return True, object_name, file_path

def create_collection(collection_id):
    client = create_boto_client_aws()
    try:
        response = client.create_collection(CollectionId=collection_id)
    except ClientError as e:
        print(e)
        return False

    return True

def list_faces_in_collection(collection_id):


    maxResults=2
    faces_count=0
    tokens=True

    client = create_boto_client_aws()
    response=client.list_faces(CollectionId=collection_id,
                               MaxResults=maxResults)

    # print('Faces in collection ' + collection_id)

 
    while tokens:

        faces=response['Faces']

        for face in faces:
            # print (face)
            faces_count+=1
        if 'NextToken' in response:
            nextToken=response['NextToken']
            response=client.list_faces(CollectionId=collection_id,
                                       NextToken=nextToken,MaxResults=maxResults)
        else:
            tokens=False
    return faces_count   

path = "/Users/amittomar/Downloads/Male/"
if __name__ == '__main__':
	# create_collection("demo_imgs_clt")
	# print(list_faces_in_collection("demo_imgs_clt"))
    list_celeb = []
    for file in os.listdir(path):
        filename = os.fsdecode(file)
        # os.rename(path+filename, path + filename.lower())
        if filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".png"):
            is_uploaded, object_name, file_path = s3_image_upload(path+filename)
            if is_uploaded:
                _ = aws_index_image(object_name, "celeb_male_ffi")
                list_celeb.append(file)
            else:
                print("Image is not uploaded correctly!")
        else:
            print("image_not_correct_format: ", filename)