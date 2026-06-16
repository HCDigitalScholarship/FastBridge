"""
Collaboration permission utilities.

Single source of truth for the "who can do what on a shared resource" model used
across the app. A collaboration resource has an owner (who implicitly holds the
top role) and a ``permissions`` map of ``{user_id: {"level": <value>}}``. The
role hierarchy, the permission check, and the require/error behaviour are
identical across resource types and live in :class:`PermissionPolicy`. Only the
resource-specific lookup (how a list or a lemma project is found in MongoDB)
differs, and that lives in the thin checker classes that delegate to a shared
policy.

  - :class:`PermissionChecker`      -- vocabulary lists (formerly utils.permissions)
  - :class:`LemmaPermissionChecker` -- lemmatization projects (formerly utils.lemma_permissions)
"""

from typing import Optional, Tuple, Type, Dict, Sequence
from enum import Enum

from models.user_models import PermissionLevel
from models.lemma_models import LemmaPermissionLevel
from mongo_connection import atlas_client
from utils.error_handlers import AuthorizationError


class PermissionPolicy:
    """Role hierarchy + permission-check engine shared by all collaboration resources.

    Add a role or fix the hierarchy here once, and every resource type benefits.
    """

    def __init__(
        self,
        level_enum: Type[Enum],
        ordered_levels: Sequence[Enum],
        owner_level: Enum,
        default_level: Enum,
        resource_noun: str,
    ):
        """
        Args:
            level_enum: The permission-level enum for this resource type.
            ordered_levels: Levels ordered from least to most privileged.
            owner_level: Level the owner is treated as holding.
            default_level: Level assumed when a grant omits an explicit level.
            resource_noun: Word used in "no access to this <noun>" errors.
        """
        self._level_enum = level_enum
        self._owner_level = owner_level
        self._default_level = default_level
        self._resource_noun = resource_noun
        self._rank = {level: index for index, level in enumerate(ordered_levels)}

    @property
    def owner_level(self) -> Enum:
        return self._owner_level

    def evaluate(
        self,
        user_id: str,
        owner_id: Optional[str],
        permissions: Optional[Dict],
        required: Enum,
    ) -> Tuple[bool, Optional[Enum]]:
        """
        Resolve a user's effective permission and whether it meets ``required``.

        The owner implicitly holds ``owner_level``; any other user gets the level
        recorded in ``permissions`` for them, or no access at all.

        Returns:
            Tuple of (has_permission, actual_permission_level). ``actual`` is
            ``None`` when the user has no access.
        """
        if owner_id is not None and user_id == owner_id:
            return True, self._owner_level

        user_perm = (permissions or {}).get(user_id)
        if not user_perm:
            return False, None

        actual = self._level_enum(user_perm.get("level", self._default_level.value))
        has_permission = self._rank[actual] >= self._rank[required]
        return has_permission, actual

    def require(self, has_permission: bool, actual: Optional[Enum], required: Enum) -> None:
        """Raise :class:`AuthorizationError` if a check (from :meth:`evaluate`) did not pass."""
        if has_permission:
            return
        if actual is None:
            raise AuthorizationError(f"You do not have access to this {self._resource_noun}")
        raise AuthorizationError(
            f"This action requires {required.value} permission. "
            f"You have {actual.value} permission."
        )


# Per-resource policies -- the single place where each resource's roles live.
_LIST_POLICY = PermissionPolicy(
    level_enum=PermissionLevel,
    ordered_levels=(PermissionLevel.VIEW, PermissionLevel.EDIT, PermissionLevel.ADMIN),
    owner_level=PermissionLevel.ADMIN,
    default_level=PermissionLevel.VIEW,
    resource_noun="list",
)

_LEMMA_POLICY = PermissionPolicy(
    level_enum=LemmaPermissionLevel,
    ordered_levels=(LemmaPermissionLevel.CAN_VIEW, LemmaPermissionLevel.CAN_EDIT),
    owner_level=LemmaPermissionLevel.CAN_EDIT,
    default_level=LemmaPermissionLevel.CAN_VIEW,
    resource_noun="project",
)


class PermissionChecker:
    """Permission checks for vocabulary lists.

    A list is stored as an embedded sub-document inside its owner's ``lists``
    document, addressed by ``(owner_id, language, list_name)``.
    """

    @staticmethod
    def _get_list_permissions(owner_id: str, language: str, list_name: str) -> Optional[Dict]:
        """Return the permissions map for a list, or ``None`` if the list is not found."""
        storage = atlas_client.get_database("App-Storage")
        owner_doc = storage.lists.find_one(
            {"user_id": owner_id, f"languages.{language}.name": list_name},
            {f"languages.{language}.$": 1},
        )

        if not owner_doc or "languages" not in owner_doc:
            return None

        lists = owner_doc["languages"].get(language, [])
        if not lists:
            return None

        return lists[0].get("permissions", {})

    @staticmethod
    async def check_list_permission(
        user_id: str,
        owner_id: str,
        language: str,
        list_name: str,
        required_permission: PermissionLevel,
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
        # Owner always has admin permission -- skip the lookup entirely.
        if user_id == owner_id:
            return True, PermissionLevel.ADMIN

        permissions = PermissionChecker._get_list_permissions(owner_id, language, list_name)
        return _LIST_POLICY.evaluate(user_id, owner_id, permissions, required_permission)

    @staticmethod
    async def get_user_permission(
        user_id: str,
        owner_id: str,
        language: str,
        list_name: str,
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
        required_permission: PermissionLevel,
    ):
        """Raise AuthorizationError if user doesn't have required permission"""
        has_permission, actual_level = await PermissionChecker.check_list_permission(
            user_id, owner_id, language, list_name, required_permission
        )
        _LIST_POLICY.require(has_permission, actual_level, required_permission)


class LemmaPermissionChecker:
    """Permission checks for lemmatization projects.

    A project is a top-level document in ``lemma_projects`` addressed by
    ``project_id``; the owner is recorded on the document itself.
    """

    @staticmethod
    def _get_project(project_id: str, projection: Dict) -> Optional[Dict]:
        storage = atlas_client.get_database("App-Storage")
        return storage.lemma_projects.find_one({"project_id": project_id}, projection)

    @staticmethod
    async def check_project_permission(
        user_id: str,
        project_id: str,
        required_permission: LemmaPermissionLevel,
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
        project = LemmaPermissionChecker._get_project(
            project_id, {"owner_id": 1, "permissions": 1}
        )
        if not project:
            return False, None

        return _LEMMA_POLICY.evaluate(
            user_id,
            project.get("owner_id"),
            project.get("permissions", {}),
            required_permission,
        )

    @staticmethod
    async def get_user_permission(
        user_id: str,
        project_id: str,
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
        required_permission: LemmaPermissionLevel,
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
        _LEMMA_POLICY.require(has_permission, actual_level, required_permission)

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
        project = LemmaPermissionChecker._get_project(project_id, {"owner_id": 1})
        return bool(project) and user_id == project.get("owner_id")

    @staticmethod
    async def get_project_owner_id(project_id: str) -> Optional[str]:
        """
        Get the owner ID of a project.

        Args:
            project_id: Project identifier

        Returns:
            Owner user ID or None if project not found
        """
        project = LemmaPermissionChecker._get_project(project_id, {"owner_id": 1})
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
        project = LemmaPermissionChecker._get_project(project_id, {"permissions": 1})
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
