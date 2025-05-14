from types import UnionType
from typing import Any
from taskify.core.exception import TaskifyException, status
from taskify.api.deps import auth_required
from taskify.models.auth import User

from fastapi import Depends


class Authorization:
    resource: str

    def __or__(self, value: "Authorization"):
        return _ORAuthorization(self, value)

    def __and__(self, value: "Authorization"):
        return _ANDAuthorization(self, value)

    def check(self, user: User) -> bool:
        raise NotImplementedError

    async def __call__(self, user: User = Depends(auth_required)):
        if not self.check(user):
            raise TaskifyException(
                status.HTTP_403_FORBIDDEN,
                "Access Denied",
                f"You don't have permission to perform action on {self.resource} resource",
            )
        return user


class _ORAuthorization(Authorization):
    def __init__(self, left: Authorization, right: Authorization):
        self.left = left
        self.right = right

    def __or__(self, user: User) -> bool:
        return self.left.check(user) or self.right.check(user)

    def __repr__(self) -> str:
        return f"({self.left}) | ({self.right})"


class _ANDAuthorization(Authorization):
    def __init__(self, left: Authorization, right: Authorization):
        self.left = left
        self.right = right

    def __and__(self, user: User) -> bool:
        return self.left.check(user) and self.right.check(user)

    def __repr__(self) -> str:
        return f"({self.left}) & ({self.right})"


class HasPermission(Authorization):
    def __init__(self, action: str, resource: str | None = None):
        self.action = action
        self.resource = resource

    def check(self, user: User) -> bool:
        permissions = user.role.permissions
        return any(
            p.action == self.action and p.resource.lower() == self.resource.lower()
            for p in permissions
        )

    def __repr__(self) -> str:
        return f"HasPermission({self.resource.lower()}:{self.action})"


class HasRole(Authorization):
    def __init__(self, role: str):
        self.role = role

    def check(self, user: User) -> bool:
        return user.role.name.lower() == self.role.lower()

    def __repr__(self) -> str:
        return f"HasRole({self.role})"

__all__ = ["Authorization", "HasRole", "HasPermission"]