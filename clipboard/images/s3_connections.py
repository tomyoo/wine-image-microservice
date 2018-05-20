import boto3

s3 = boto3.resource('s3')
client = boto3.client('s3')


def upload_image_to_hf_bucket(image):
    data = open(image, 'rb')
    s3.meta.client.upload_file(
        image, 'lot18-partner', 'HelloFreshTest/{}'.format(image))
