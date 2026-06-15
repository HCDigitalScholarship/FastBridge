from typing import Optional, Tuple
from models.user_models import PermissionLevel
from mongo_connection import atlas_client
from utils.error_handlers import AuthorizationError

class PermissionChecker:
    """Utility class for checking permissions on vocabulary lists"""

    @staticmethod
    async def check_list_permission(
        user_id: str,
        owner_id: str,
        language: str,
        list_name: str,
        required_permission: PermissionLevel
    ) -> Tuple[bool, Optional[PermissionLevel]]:
        """
        Check if user has required permission on a list.

        Args:
            user_id: User requesting access
            owner_id: Owner of the list
            language: Language of the list
            list_name: Name of the list
            required_permission: Minimum permission level required

        Returns:
            Tuple of (has_permission, actual_permission_level)
        """
        # Owner always has admin permission
        if user_id == owner_id:
            return True, PermissionLevel.ADMIN

        storage = atlas_client.get_database("App-Storage")

        # Find the list in owner's document
        owner_doc = storage.lists.find_one(
            {"user_id": owner_id, f"languages.{language}.name": list_name},
            {f"languages.{language}.$": 1}
        )

        if not owner_doc or "languages" not in owner_doc:
            return False, None

        lists = owner_doc["languages"].get(language, [])
        if not lists:
            return False, None

        target_list = lists[0]
        permissions = target_list.get("permissions", {})

        # Check if user has any permission
        user_perm = permissions.get(user_id)
        if not user_perm:
            return False, None

        actual_level = PermissionLevel(user_perm.get("level", "view"))

        # Permission hierarchy: admin > edit > view
        permission_hierarchy = {
            PermissionLevel.VIEW: 0,
            PermissionLevel.EDIT: 1,
            PermissionLevel.ADMIN: 2
        }

        has_permission = permission_hierarchy[actual_level] >= permission_hierarchy[required_permission]

        return has_permission, actual_level

    @staticmethod
    async def get_user_permission(
        user_id: str,
        owner_id: str,
        language: str,
        list_name: str
    ) -> Optional[PermissionLevel]:
        """Get user's permission level on a list (or None if no access)"""
        _, permission = await PermissionChecker.check_list_permission(
            user_id, owner_id, language, list_name, PermissionLevel.VIEW
        )
        return permission

    @staticmethod
    async def require_permission(
        user_id: str,
        owner_id: str,
        language: str,
        list_name: str,
        required_permission: PermissionLevel
    ):
        """Raise AuthorizationError if user doesn't have required permission"""
        has_permission, actual_level = await PermissionChecker.check_list_permission(
            user_id, owner_id, language, list_name, required_permission
        )

        if not has_permission:
            if actual_level is None:
                raise AuthorizationError(f"You do not have access to this list")
            else:
                raise AuthorizationError(
                    f"This action requires {required_permission.value} permission. "
                    f"You have {actual_level.value} permission."
                )
