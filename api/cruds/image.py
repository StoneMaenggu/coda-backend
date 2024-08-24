# import boto3
# from botocore.exceptions import NoCredentialsError
# from fastapi import HTTPException
# from typing import Tuple
# from uuid import uuid4

# # S3 클라이언트 생성
# s3_client = boto3.client(
#     's3',
#     aws_access_key_id='AKIAQLVQQZWMOOLDVB5Z',
#     aws_secret_access_key='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'
# )

# BUCKET_NAME = 'codabucket-flyai'
# REGION_NAME = 'ap-northeast-1'

# async def upload_image_to_s3(file: bytes, filename: str) -> Tuple[str, str]:
#     """
#     S3에 이미지 파일을 업로드하는 함수.
#     :param file: 업로드할 파일의 바이트.
#     :param filename: 업로드할 파일의 이름.
#     :return: 업로드된 파일의 URL 및 파일 이름.
#     """
#     try:
#         # 고유한 파일명을 생성하기 위해 UUID 사용
#         unique_filename = f"{uuid4()}_{filename}"
#         s3_client.put_object(Bucket=BUCKET_NAME, Key=unique_filename, Body=file, ContentType='image/jpeg')
        
#         # S3 URL 생성
#         url = f"https://{BUCKET_NAME}.s3.{REGION_NAME}.amazonaws.com/{unique_filename}"
#         return unique_filename, url

#     except NoCredentialsError:
#         raise HTTPException(status_code=500, detail="AWS S3 Credentials are not available.")
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

import aioboto3
from botocore.exceptions import NoCredentialsError
from fastapi import HTTPException
from typing import Tuple
from uuid import uuid4
from api.access import Access


BUCKET_NAME = 'codabucket-flyai'
REGION_NAME = 'ap-northeast-1'
s3_access_key = Access().s3_access_key
s3_secret_key = Access().s3_secret_key

async def upload_image_to_s3(file: bytes, filename: str) -> Tuple[str, str]:
    """
    S3에 이미지 파일을 업로드하는 비동기 함수.
    :param file: 업로드할 파일의 바이트.
    :param filename: 업로드할 파일의 이름.
    :return: 업로드된 파일의 URL 및 파일 이름.
    """

    # S3 클라이언트 생성
    session = aioboto3.Session()

    
    try:
        # 고유한 파일명을 생성하기 위해 UUID 사용
        unique_filename = f"{uuid4()}_{filename}"
        async with session.client(
            's3',
            aws_access_key_id=s3_access_key,
            aws_secret_access_key=s3_secret_key
        ) as s3_client:
            await s3_client.put_object(Bucket=BUCKET_NAME, Key=unique_filename, Body=file, ContentType='image/jpeg')
        
        # S3 URL 생성
        url = f"https://{BUCKET_NAME}.s3.{REGION_NAME}.amazonaws.com/{unique_filename}"
        return unique_filename, url

    except NoCredentialsError:
        raise HTTPException(status_code=500, detail="AWS S3 Credentials are not available.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
