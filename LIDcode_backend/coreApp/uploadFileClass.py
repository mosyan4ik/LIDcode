import boto3
import datetime
import os


class FileHosting:
    s3 = boto3.client(
        service_name='s3',
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID_S3"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY_S3"),
        region_name='ru-central1',
        endpoint_url="https://storage.yandexcloud.net"
    )

    def upload_file(self, image_path):
        strdatetime = str(datetime.datetime.now().strftime('%Y-%d-%m'))
        self.s3.upload_file(image_path, 'staticlidcode', f"{strdatetime}/" + image_path.split('/')[-1])
        presigned_url = os.environ.get("PRESIGNED_URL_S3") + f"{strdatetime}/" + image_path.split('/')[-1]
        return presigned_url
