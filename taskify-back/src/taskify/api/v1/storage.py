from fastapi import Depends, UploadFile
from taskify.api.deps import get_file_storage, StorageService
from taskify.models.auth import User
from taskify.schemas.storage import FileUploadResponse
from taskify.schemas.user import UserRead
from taskify.utils.cbv import Controller
from taskify.utils.permissions import HasPermission


class FileStorageController(Controller):
    prefix = "/files"
    tags = ["Files"]
    resource = "storage"

    service: StorageService = Depends(get_file_storage)

    @Controller.put("/avatars", response_model=UserRead)
    async def upload_avatar(
        self, file: UploadFile, user: User = Depends(HasPermission("avatar"))
    ):
        return await self.service.upload_avatar(file, user)

    @Controller.put("/{object_key:path}", response_model=FileUploadResponse)
    async def upload_file(
        self, object_key: str, file: UploadFile, user=Depends(HasPermission("upload"))
    ):
        return await self.service.upload_file(file, object_key)
