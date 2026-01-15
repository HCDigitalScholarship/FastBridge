"""
Pydantic models for Lemmatization Workspace feature.

These models handle data validation and serialization for collaborative
CSV editing with confidence-based highlighting and real-time collaboration.
"""

from pydantic import BaseModel, Field, field_validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum
import uuid
import re


class LemmaPermissionLevel(str, Enum):
    """Permission levels for lemmatization projects."""
    CAN_VIEW = "CAN_VIEW"    # Read-only + comment
    CAN_EDIT = "CAN_EDIT"    # Can modify cells


class PermissionGrant(BaseModel):
    """Permission grant information stored in project document."""
    level: LemmaPermissionLevel = Field(..., description="Permission level granted")
    granted_at: datetime = Field(default_factory=datetime.now, description="When permission was granted")
    granted_by: str = Field(..., description="User ID who granted the permission")


class FileMetadata(BaseModel):
    """Metadata about uploaded CSV file."""
    original_filename: str = Field(..., description="Original uploaded filename")
    row_count: int = Field(..., description="Number of data rows")
    column_names: List[str] = Field(..., description="List of column names from CSV")


class LemmaProject(BaseModel):
    """Main project document structure."""
    project_id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique project identifier")
    owner_id: str = Field(..., description="Firebase user ID of project owner")
    project_name: str = Field(..., min_length=1, max_length=200, description="Project name")
    description: Optional[str] = Field(None, max_length=1000, description="Optional project description")
    created_at: datetime = Field(default_factory=datetime.now, description="Project creation timestamp")
    last_modified: datetime = Field(default_factory=datetime.now, description="Last modification timestamp")
    file_metadata: FileMetadata = Field(..., description="CSV file metadata")
    permissions: Dict[str, Dict] = Field(default={}, description="User permissions dict")
    share_links: Dict[str, str] = Field(
        default_factory=lambda: {
            "view": str(uuid.uuid4()),
            "edit": str(uuid.uuid4())
        },
        description="Share links for view and edit access"
    )


class LemmaRow(BaseModel):
    """Individual row in the CSV data."""
    row_id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique row identifier")
    row_index: int = Field(..., ge=0, description="Row position in original CSV")
    confidence: float = Field(default=50.0, ge=0.0, le=100.0, description="Confidence score (0-100)")
    data: Dict[str, str] = Field(..., description="Column name -> value mapping")
    last_modified: datetime = Field(default_factory=datetime.now, description="Last edit timestamp")
    last_modified_by: str = Field(..., description="User ID of last editor")


class LemmaDataDocument(BaseModel):
    """Document containing all rows for a project."""
    project_id: str = Field(..., description="Project identifier")
    rows: List[LemmaRow] = Field(default=[], description="List of data rows")


class LemmaComment(BaseModel):
    """Row-level comment."""
    comment_id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique comment identifier")
    project_id: str = Field(..., description="Project identifier")
    row_id: str = Field(..., description="Row identifier")
    user_id: str = Field(..., description="Commenter user ID")
    username: str = Field(..., description="Commenter display name")
    comment_text: str = Field(..., min_length=1, max_length=5000, description="Comment text")
    created_at: datetime = Field(default_factory=datetime.now, description="Comment timestamp")
    resolved: bool = Field(default=False, description="Whether comment is resolved")


class SuggestionStatus(str, Enum):
    """Status of edit suggestion."""
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"


class LemmaSuggestion(BaseModel):
    """Track-changes style edit suggestion."""
    suggestion_id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique suggestion identifier")
    project_id: str = Field(..., description="Project identifier")
    row_id: str = Field(..., description="Row identifier")
    suggested_by: str = Field(..., description="Suggester user ID")
    suggested_by_name: str = Field(..., description="Suggester display name")
    status: SuggestionStatus = Field(default=SuggestionStatus.PENDING, description="Suggestion status")
    original_data: Dict[str, str] = Field(..., description="Original values before suggestion")
    suggested_data: Dict[str, str] = Field(..., description="Suggested new values")
    changes: Dict[str, Dict[str, str]] = Field(..., description="Field-level changes {field: {from, to}}")
    comment: Optional[str] = Field(None, max_length=1000, description="Reason for suggestion")
    created_at: datetime = Field(default_factory=datetime.now, description="Suggestion timestamp")


class EditAction(str, Enum):
    """Types of actions that can be logged."""
    EDIT = "edit"
    COMMENT = "comment"
    SUGGEST = "suggest"
    ACCEPT_SUGGESTION = "accept_suggestion"
    REJECT_SUGGESTION = "reject_suggestion"
    CREATE_PROJECT = "create_project"
    DELETE_PROJECT = "delete_project"
    GRANT_PERMISSION = "grant_permission"
    REVOKE_PERMISSION = "revoke_permission"


class LemmaEditHistory(BaseModel):
    """Audit log entry for changes."""
    history_id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique history entry identifier")
    project_id: str = Field(..., description="Project identifier")
    row_id: Optional[str] = Field(None, description="Row identifier (if applicable)")
    user_id: str = Field(..., description="User who performed action")
    username: str = Field(..., description="User display name")
    action: EditAction = Field(..., description="Type of action")
    timestamp: datetime = Field(default_factory=datetime.now, description="Action timestamp")
    changes: Optional[Dict[str, Any]] = Field(None, description="Details of changes made")


class SharedProjectInfo(BaseModel):
    """Information about a project shared with a user."""
    project_id: str = Field(..., description="Project identifier")
    project_name: str = Field(..., description="Project name")
    permission: LemmaPermissionLevel = Field(..., description="Permission level granted")
    shared_at: datetime = Field(default_factory=datetime.now, description="When project was shared")


class LemmaUserWorkspace(BaseModel):
    """User's workspace document linking them to projects."""
    user_id: str = Field(..., description="Firebase user ID")
    owned_projects: List[str] = Field(default=[], description="List of owned project IDs")
    shared_with_me: Dict[str, List[SharedProjectInfo]] = Field(
        default={},
        description="Projects shared with this user, grouped by owner"
    )


# API Request/Response Models

class CreateProjectRequest(BaseModel):
    """Request to create a new project."""
    project_name: str = Field(..., min_length=1, max_length=200, description="Project name")
    description: Optional[str] = Field(None, max_length=1000, description="Optional description")
    # Note: CSV file is handled separately via UploadFile

    @field_validator('project_name')
    @classmethod
    def validate_project_name(cls, v):
        """Ensure project name doesn't contain problematic characters."""
        if not v.strip():
            raise ValueError("Project name cannot be empty or whitespace only")
        # Remove any potentially problematic characters
        invalid_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
        for char in invalid_chars:
            if char in v:
                raise ValueError(f"Project name cannot contain '{char}'")
        return v.strip()


class EditRowRequest(BaseModel):
    """Request to edit a row cell."""
    field: str = Field(..., min_length=1, description="Column name to edit")
    new_value: str = Field(..., description="New cell value")


class CreateCommentRequest(BaseModel):
    """Request to add a comment."""
    row_id: str = Field(..., description="Row to comment on")
    comment_text: str = Field(..., min_length=1, max_length=5000, description="Comment text")


class CreateSuggestionRequest(BaseModel):
    """Request to create an edit suggestion."""
    row_id: str = Field(..., description="Row to suggest changes for")
    changes: Dict[str, str] = Field(..., description="Field -> new value mapping")
    comment: Optional[str] = Field(None, max_length=1000, description="Reason for suggestion")

    @field_validator('changes')
    @classmethod
    def validate_changes_not_empty(cls, v):
        """Ensure at least one change is provided."""
        if not v:
            raise ValueError("Must provide at least one field change")
        return v


class GrantPermissionRequest(BaseModel):
    """Request to grant permission to another user."""
    recipient_email: str = Field(..., description="Email of user to grant access to")
    permission: LemmaPermissionLevel = Field(..., description="Permission level to grant")

    @field_validator('recipient_email')
    @classmethod
    def validate_email(cls, v):
        """Validate email format."""
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, v):
            raise ValueError('Invalid email format')
        return v.lower().strip()


class ModifyPermissionRequest(BaseModel):
    """Request to modify an existing permission."""
    recipient_id: str = Field(..., description="User ID of recipient")
    new_permission: LemmaPermissionLevel = Field(..., description="New permission level")


class RevokePermissionRequest(BaseModel):
    """Request to revoke user's permission."""
    recipient_id: str = Field(..., description="User ID to revoke access from")


# Response Models

class ProjectListResponse(BaseModel):
    """Response containing list of projects."""
    owned_projects: List[Dict[str, Any]] = Field(..., description="Projects owned by user")
    shared_projects: List[Dict[str, Any]] = Field(..., description="Projects shared with user")


class ProjectDetailResponse(BaseModel):
    """Response with project details."""
    project: LemmaProject
    user_permission: LemmaPermissionLevel
    is_owner: bool


class RowsResponse(BaseModel):
    """Response containing paginated rows."""
    rows: List[LemmaRow]
    total_rows: int
    page: int
    page_size: int
    total_pages: int


class CommentsResponse(BaseModel):
    """Response containing comments."""
    comments: List[LemmaComment]
    total: int


class SuggestionsResponse(BaseModel):
    """Response containing suggestions."""
    suggestions: List[LemmaSuggestion]
    total: int


class PermissionsListResponse(BaseModel):
    """Response listing all users with access."""
    permissions: List[Dict[str, Any]]  # {user_id, email, username, permission, granted_at}


class ActiveUsersResponse(BaseModel):
    """Response with active users in a project."""
    active_users: List[Dict[str, str]]  # {user_id, username}
    count: int
