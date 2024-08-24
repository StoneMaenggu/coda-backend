# from fastapi import APIRouter, File, UploadFile, HTTPException
# from api.cruds.image import upload_image_to_s3
# from api.schemas.image import ImageUploadResponse

# router = APIRouter()

# @router.post("/upload-image/", response_model=ImageUploadResponse)
# async def upload_image(file: UploadFile = File(...)):
#     """
#     이미지 파일을 S3에 업로드하는 엔드포인트.
#     :param file: 업로드할 이미지 파일.
#     :return: 업로드된 이미지 파일의 URL 및 파일 이름.
#     """
#     if file.content_type != "image/jpeg":
#         raise HTTPException(status_code=400, detail="Only JPEG images are allowed.")

#     file_bytes = await file.read()
#     filename, url = upload_image_to_s3(file_bytes, file.filename)

#     return ImageUploadResponse(filename=filename, url=url)


from fastapi import APIRouter, File, UploadFile, HTTPException
from typing import List
from api.cruds.image import upload_image_to_s3
from api.schemas.image import ImageUploadResponse

router = APIRouter()

@router.post("/upload-images", response_model=List[ImageUploadResponse])
async def upload_images(files: List[UploadFile] = File(...)):
    """
    여러 이미지 파일을 S3에 업로드하는 엔드포인트.
    :param files: 업로드할 이미지 파일 리스트.
    :return: 업로드된 이미지 파일들의 URL 및 파일 이름 리스트.
    """
    upload_responses = []

    for file in files:
        if file.content_type != "image/jpeg":
            raise HTTPException(status_code=400, detail="Only JPEG images are allowed.")

        file_bytes = await file.read()
        filename, url = await upload_image_to_s3(file_bytes, file.filename)
        upload_responses.append(ImageUploadResponse(filename=filename, url=url))

    return upload_responses