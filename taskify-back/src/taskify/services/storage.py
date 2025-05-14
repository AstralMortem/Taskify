from io import BytesIO
import aioboto3
from fastapi import UploadFile
from taskify.config import settings

from taskify.core.exception import TaskifyException, status
from taskify.models.auth import User
from taskify.repositories.auth import UserRepository
from taskify.schemas.storage import FileUploadResponse


class StorageService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo
        self.session = aioboto3.Session(
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION_NAME,
        )
        self.bucket_name = settings.BUCKET_NAME
        self.endpoint_url = settings.AWS_ENDPOINT_URL

    async def upload_file(
        self, file: UploadFile, object_key: str | None = None, **kwargs
    ) -> FileUploadResponse:
        if object_key is None:
            object_key = file.filename or ""

        try:
            async with self.session.client(
                "s3", endpoint_url=self.endpoint_url
            ) as s3_client:
                await s3_client.upload_fileobj(
                    Fileobj=BytesIO(await file.read()),
                    Bucket=self.bucket_name,
                    Key=object_key,
                    ExtraArgs=kwargs,
                )
        except Exception as e:
            raise TaskifyException(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                "Unable to upload file",
                "Unable to upload file to s3 server",
                debug=e,
            )

        object_url = await self.generate_presigned_url(object_key)

        return FileUploadResponse(
            filename=object_key.rsplit("/", 1)[1],
            object_key=object_key,
            bucket=self.bucket_name,
            domain_url=object_url,
            size=file.size or 0,
        )

    async def generate_presigned_url(
        self, object_key: str, expiration: int = 3600
    ) -> str:
        try:
            async with self.session.client(
                "s3", endpoint_url=self.endpoint_url
            ) as s3_client:
                url = await s3_client.generate_presigned_url(
                    "get_object", Params={"Bucket": self.bucket_name, "Key": object_key}
                )
                return url
        except Exception as e:
            raise TaskifyException(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                "Unable to generate file object url",
                debug=e,
            )

    async def upload_avatar(self, file: UploadFile, user: User):
        if not file.filename:
            raise TaskifyException(400, "Filename not set")

        filename, ext = file.filename.split(".")
        if filename != str(user.id):
            filename = str(user.id)

        object_key = f"/avatars/{filename}.{ext}"
        response = await self.upload_file(file, object_key)
        return await self.user_repo.update(user, {"avatar": response.url})
