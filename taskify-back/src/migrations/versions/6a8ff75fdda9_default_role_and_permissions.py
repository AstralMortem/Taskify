"""default_role_and_permissions

Revision ID: 6a8ff75fdda9
Revises: 9dd2881a3d64
Create Date: 2025-05-14 14:05:16.681137

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.orm import Session
from taskify.models.auth import Permission, Role
from taskify.schemas.rbac import Action


# revision identifiers, used by Alembic.
revision: str = '6a8ff75fdda9'
down_revision: Union[str, None] = '9dd2881a3d64'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    bind = op.get_bind()
    session = Session(bind)

    p_users_read = Permission(action=Action.READ, resource='users')

    p_boards_read = Permission(action=Action.READ, resource='boards')
    p_boards_update = Permission(action=Action.UPDATE, resource='boards')
    p_boards_create = Permission(action=Action.CREATE, resource='boards')
    p_boards_delete = Permission(action=Action.DELETE, resource='boards')

    p_lists_read = Permission(action=Action.READ, resource='lists')
    p_lists_update = Permission(action=Action.UPDATE, resource='lists')
    p_lists_create = Permission(action=Action.CREATE, resource='lists')
    p_lists_delete = Permission(action=Action.DELETE, resource='lists')

    p_cards_read = Permission(action=Action.READ, resource='cards')
    p_cards_update = Permission(action=Action.UPDATE, resource='cards')
    p_cards_create = Permission(action=Action.CREATE, resource='cards')
    p_cards_delete = Permission(action=Action.DELETE, resource='cards')

    p_storage_avatar = Permission(action='avatar', resource='storage')
    p_storage_upload = Permission(action='upload', resource='storage')

    USER_ROLES = [p_users_read, p_boards_update, p_boards_create, p_boards_read, p_boards_delete, p_lists_read, p_lists_update, p_lists_create, p_lists_delete,
                  p_cards_create, p_cards_read, p_cards_delete, p_cards_update, p_storage_avatar]
    
    ADMIN_ROLES = USER_ROLES + [p_storage_upload]

    default_role = Role(name="USER", permissions=USER_ROLES)
    admin_role = Role(name="ADMIN", permissions=ADMIN_ROLES)

    session.add_all(ADMIN_ROLES + [
        default_role,
        admin_role
    ])

    session.commit()
    


def downgrade() -> None:
    """Downgrade schema."""
    op.execute('DELETE FROM roles')
    op.execute('DELETE FROM permissions')