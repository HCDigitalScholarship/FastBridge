"""
Permission checking utilities for Lemmatization Workspace.

Handles permission verification for collaborative CSV editing projects
with CAN_VIEW and CAN_EDIT permission levels.
"""

from typing import Optional, Tuple
from models.lemma_models import LemmaPermissionLevel
from mongo_connection import atlas_client
from utils.error_handlers import AuthorizationError


class LemmaPermissionChecker:
    """Utility class for checking permissions on lemmatization projects."""

    @staticmethod
    async def check_project_permission(
        user_id: str,
        project_id: str,
        required_permission: LemmaPermissionLevel
    ) -> Tuple[bool, Optional[LemmaPermissionLevel]]:
        """
        Check if user has required permission on a project.

        Args:
            user_id: User requesting access
            project_id: Project identifier
            required_permission: Minimum permission level required

        Returns:
            Tuple of (has_permission, actual_permission_level)
        """
        storage = atlas_client.get_database("App-Storage")

        # Find the project
        project = storage.lemma_projects.find_one(
            {"project_id": project_id},
            {"owner_id": 1, "permissions": 1}
        )

        if not project:
            return False, None

        # Owner always has CAN_EDIT permission
        if user_id == project.get("owner_id"):
            return True, LemmaPermissionLevel.CAN_EDIT

        # Check if user has explicit permission
        permissions = project.get("permissions", {})
        user_perm = permissions.get(user_id)

        if not user_perm:
            return False, None

        actual_level = LemmaPermissionLevel(user_perm.get("level", "CAN_VIEW"))

        # Permission hierarchy: CAN_EDIT > CAN_VIEW
        permission_hierarchy = {
            LemmaPermissionLevel.CAN_VIEW: 0,
            LemmaPermissionLevel.CAN_EDIT: 1
        }

        has_permission = permission_hierarchy[actual_level] >= permission_hierarchy[required_permission]

        return has_permission, actual_level

    @staticmethod
    async def get_user_permission(
        user_id: str,
        project_id: str
    ) -> Optional[LemmaPermissionLevel]:
        """
        Get user's permission level on a project (or None if no access).

        Args:
            user_id: User identifier
            project_id: Project identifier

        Returns:
            Permission level or None
        """
        _, permission = await LemmaPermissionChecker.check_project_permission(
            user_id, project_id, LemmaPermissionLevel.CAN_VIEW
        )
        return permission

    @staticmethod
    async def require_permission(
        user_id: str,
        project_id: str,
        required_permission: LemmaPermissionLevel
    ):
        """
        Raise AuthorizationError if user doesn't have required permission.

        Args:
            user_id: User identifier
            project_id: Project identifier
            required_permission: Minimum permission level required

        Raises:
            AuthorizationError: If user lacks required permission
        """
        has_permission, actual_level = await LemmaPermissionChecker.check_project_permission(
            user_id, project_id, required_permission
        )

        if not has_permission:
            if actual_level is None:
                raise AuthorizationError("You do not have access to this project")
            else:
                raise AuthorizationError(
                    f"This action requires {required_permission.value} permission. "
                    f"You have {actual_level.value} permission."
                )

    @staticmethod
    async def is_project_owner(user_id: str, project_id: str) -> bool:
        """
        Check if user is the owner of a project.

        Args:
            user_id: User identifier
            project_id: Project identifier

        Returns:
            True if user is owner, False otherwise
        """
        storage = atlas_client.get_database("App-Storage")

        project = storage.lemma_projects.find_one(
            {"project_id": project_id},
            {"owner_id": 1}
        )

        if not project:
            return False

        return user_id == project.get("owner_id")

    @staticmethod
    async def get_project_owner_id(project_id: str) -> Optional[str]:
        """
        Get the owner ID of a project.

        Args:
            project_id: Project identifier

        Returns:
            Owner user ID or None if project not found
        """
        storage = atlas_client.get_database("App-Storage")

        project = storage.lemma_projects.find_one(
            {"project_id": project_id},
            {"owner_id": 1}
        )

        return project.get("owner_id") if project else None

    @staticmethod
    async def list_project_permissions(project_id: str) -> dict:
        """
        Get all permissions for a project.

        Args:
            project_id: Project identifier

        Returns:
            Dict of {user_id: permission_info}
        """
        storage = atlas_client.get_database("App-Storage")

        project = storage.lemma_projects.find_one(
            {"project_id": project_id},
            {"permissions": 1}
        )

        return project.get("permissions", {}) if project else {}

    @staticmethod
    async def can_manage_permissions(user_id: str, project_id: str) -> bool:
        """
        Check if user can manage permissions (only owner can).

        Args:
            user_id: User identifier
            project_id: Project identifier

        Returns:
            True if user can manage permissions, False otherwise
        """
        return await LemmaPermissionChecker.is_project_owner(user_id, project_id)
