from enum import Enum
import inspect
from typing import Callable, ClassVar, Literal, get_type_hints
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi.routing import APIRoute
from pydantic.v1.typing import is_classvar
from makefun import with_signature
from fastapi.params import Depends as DependsClass

from taskify.utils.permissions import Authorization

ROUTE_MARKER = "__is_controller_route__"
CONTROLLER_MARKER = "__is_controller__"


def override_permissions(cls: type["Controller"], func: Callable):
    params = list(inspect.signature(func).parameters.values())
    for idx, param in enumerate(params):
        if isinstance(param.default, DependsClass) and isinstance(
            param.default.dependency, Authorization
        ):
            if param.default.dependency.resource is None:
                param.default.dependency.resource = cls.resource
                params[idx].replace(default=param.default)

    return with_signature(inspect.Signature(params))(func)


def get_wrapped_route(
    func,
    path: str,
    method: Literal["get", "post", "put", "patch", "delete"],
    *,
    response_model=None,
    status_code=200,
    response_class=JSONResponse,
    dependencies: list = [],
    name: str | None = None,
):
    def wrapper(*args, **kwargs):
        cls: type[Controller] = kwargs.get("cls", None)
        function = override_permissions(cls, func)
        return APIRoute(
            path=path,
            endpoint=function,
            methods=[method],
            response_class=response_class,
            response_model=response_model,
            status_code=status_code,
            name=name or f"{cls.__name__}.{func.__name__}",
            tags=cls.tags,
            dependencies=dependencies,
        )

    setattr(wrapper, ROUTE_MARKER, True)
    return wrapper


class Controller:
    prefix: ClassVar[str] = ""
    tags: ClassVar[list[str | Enum]] = []
    resource: ClassVar[str] = ""

    @classmethod
    def as_router(cls, **kwargs):
        kwargs["prefix"] = kwargs.get("prefix", cls.prefix)
        kwargs["tags"] = kwargs.get("tags", cls.tags)
        router = APIRouter(**kwargs)

        cls._init_dependencies()
        cls._init_routers(router)

        return router

    @classmethod
    def _init_dependencies(cls):
        if getattr(cls, CONTROLLER_MARKER, False):
            return
        # get old init signature
        old_signature = inspect.signature(cls.__init__)
        old_params = list(old_signature.parameters.values())[1:]
        new_params = [
            x
            for x in old_params
            if x.kind
            not in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD)
        ]

        dep_names: list[str] = []
        for name, hint in get_type_hints(cls).items():
            if is_classvar(hint):
                continue
            dep_names.append(name)
            new_params.append(
                inspect.Parameter(
                    name=name,
                    kind=inspect.Parameter.KEYWORD_ONLY,
                    annotation=hint,
                    default=getattr(cls, name, Ellipsis),
                )
            )

        new_params = [
            inspect.Parameter(
                name="self",
                kind=inspect.Parameter.POSITIONAL_ONLY,
                annotation=cls,
            )
        ] + new_params

        new_signature = old_signature.replace(parameters=new_params)

        @with_signature(new_signature)
        def new_init(self, *args, **kwargs):
            for dep_name in dep_names:
                setattr(self, dep_name, kwargs.pop(dep_name))

        setattr(cls, "__init__", new_init)
        setattr(cls, CONTROLLER_MARKER, True)

    @classmethod
    def _init_routers(cls, router: APIRouter):
        for attr_name, attr in inspect.getmembers(cls, inspect.isfunction):
            if attr_name.startswith("__") and attr_name.endswith("__"):
                continue
            if hasattr(attr, ROUTE_MARKER):
                route: APIRoute = attr(cls=cls)
                old_route_signature = inspect.signature(route.endpoint)
                old_route_params = list(old_route_signature.parameters.values())
                new_self_param = old_route_params[0].replace(default=Depends(cls))
                new_params = [new_self_param] + [
                    parameter.replace(kind=inspect.Parameter.KEYWORD_ONLY)
                    for parameter in old_route_params[1:]
                ]

                new_signature = inspect.Signature(new_params)
                route.endpoint = with_signature(new_signature)(route.endpoint)
                route.path = router.prefix + route.path
                router.routes.append(route)
        return router

    @classmethod
    def get(
        cls,
        path,
        *,
        response_model=None,
        status_code=200,
        response_class=JSONResponse,
        dependencies: list = [],
        name: str | None = None,
    ):
        def decorator(func):
            return get_wrapped_route(
                func,
                path,
                "get",
                response_model=response_model,
                response_class=response_class,
                status_code=status_code,
                dependencies=dependencies,
                name=name,
            )

        return decorator

    @classmethod
    def post(
        cls,
        path,
        *,
        response_model=None,
        status_code=200,
        response_class=JSONResponse,
        dependencies: list = [],
        name: str | None = None,
    ):
        def decorator(func):
            return get_wrapped_route(
                func,
                path,
                "post",
                response_model=response_model,
                response_class=response_class,
                status_code=status_code,
                dependencies=dependencies,
                name=name,
            )

        return decorator

    @classmethod
    def put(
        cls,
        path,
        *,
        response_model=None,
        status_code=200,
        response_class=JSONResponse,
        dependencies: list = [],
        name: str | None = None,
    ):
        def decorator(func):
            return get_wrapped_route(
                func,
                path,
                "put",
                response_model=response_model,
                response_class=response_class,
                status_code=status_code,
                dependencies=dependencies,
                name=name,
            )

        return decorator

    @classmethod
    def patch(
        cls,
        path,
        *,
        response_model=None,
        status_code=200,
        response_class=JSONResponse,
        dependencies: list = [],
        name: str | None = None,
    ):
        def decorator(func):
            return get_wrapped_route(
                func,
                path,
                "patch",
                response_model=response_model,
                response_class=response_class,
                status_code=status_code,
                dependencies=dependencies,
                name=name,
            )

        return decorator

    @classmethod
    def delete(
        cls,
        path,
        *,
        response_model=None,
        status_code=200,
        response_class=JSONResponse,
        dependencies: list = [],
        name: str | None = None,
    ):
        def decorator(func):
            return get_wrapped_route(
                func,
                path,
                "delete",
                response_model=response_model,
                response_class=response_class,
                status_code=status_code,
                dependencies=dependencies,
                name=name,
            )

        return decorator
