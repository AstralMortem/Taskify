from enum import StrEnum


class Action(StrEnum):
    READ = 'retrive'
    CREATE = 'create'
    UPDATE = 'update'
    DELETE = 'delete'