from pydantic import BaseModel, EmailStr, Field, field_validator, field_serializer
from typing import Optional, List, Dict, Any, Literal
from datetime import datetime
from enum import Enum
import uuid

class LanguageType(str, Enum):
    LATIN = "Latin"
    GREEK = "Greek"

class ShareMode(str, Enum):
    COPY = "copy"
    LIVE = "live"

class PermissionLevel(str, Enum):
    VIEW = "view"
    CONTRIBUTE = "contribute"
    EDIT = "edit"

class PermissionGrant(BaseModel):
    level: PermissionLevel = Field(..., description="Permission level granted")
    granted_at: datetime = Field(default_factory=datetime.now, description="When permission was granted")
    granted_by: str = Field(..., description="User ID who granted the permission")

class SharedListInfo(BaseModel):
    list_name: str = Field(..., description="Name of the shared list")
    permission: PermissionLevel = Field(..., description="Permission level for this list")
    shared_at: datetime = Field(default_factory=datetime.now, description="When list was shared")

class GrantPermissionRequest(BaseModel):
    list_name: str = Field(..., min_length=1, description="Name of list to share")
    language: LanguageType = Field(..., description="Language of the list")
    recipient_email: str = Field(..., description="Email of user to grant access to")
    permission: PermissionLevel = Field(..., description="Permission level to grant")
    owner_id: Optional[str] = Field(None, description="Owner ID (for admin users granting on behalf of owner)")

class ModifyPermissionRequest(BaseModel):
    list_name: str = Field(..., min_length=1, description="Name of list")
    language: LanguageType = Field(..., description="Language of the list")
    recipient_id: str = Field(..., description="User ID of recipient")
    new_permission: PermissionLevel = Field(..., description="New permission level")
    owner_id: Optional[str] = Field(None, description="Owner ID (for admin users modifying on behalf of owner)")

class RevokePermissionRequest(BaseModel):
    list_name: str = Field(..., min_length=1, description="Name of list")
    language: LanguageType = Field(..., description="Language of the list")
    recipient_id: str = Field(..., description="User ID to revoke access from")
    owner_id: Optional[str] = Field(None, description="Owner ID (for admin users revoking on behalf of owner)")

class UnlinkListRequest(BaseModel):
    list_name: str = Field(..., min_length=1, description="Name of list to unlink")
    language: LanguageType = Field(..., description="Language of the list")
    owner_id: str = Field(..., description="Owner's user ID")

class UserProfile(BaseModel):
    uid: str = Field(..., description="Firebase user ID")
    email: EmailStr = Field(..., description="User email address")
    display_name: Optional[str] = Field(None, description="User display name")
    created_at: datetime = Field(default_factory=datetime.now, description="Account creation timestamp")
    last_login: Optional[datetime] = Field(None, description="Last login timestamp")
    is_active: bool = Field(default=True, description="Account active status")

    @field_serializer('created_at', 'last_login', when_used='json')
    def serialize_datetime(self, dt: Optional[datetime]) -> Optional[str]:
        return dt.isoformat() if dt else None

# ShareLinks as a simple factory function to avoid Pydantic field name conflicts
def create_share_links() -> Dict[str, str]:
    """Create default share links dictionary"""
    return {
        "copy": str(uuid.uuid4()),
        "live": str(uuid.uuid4())
    }

class VocabularyWord(BaseModel):
    lemma: str = Field(..., min_length=1, description="The word lemma")
    definition: str = Field(..., description="Word definition or translation")

class VocabularyList(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="List name")
    words: List[VocabularyWord] = Field(default=[], description="List of vocabulary words")
    owner_id: str = Field(..., description="Owner's Firebase user ID")
    original_owner_id: Optional[str] = Field(None, description="Original owner if copied from another user")
    created_at: datetime = Field(default_factory=datetime.now, description="Creation timestamp")
    last_update: Optional[datetime] = Field(None, description="Last update timestamp")
    share_links: Dict[str, str] = Field(default_factory=create_share_links, description="Share links for the list")
    is_public: bool = Field(default=False, description="Whether list is publicly discoverable")

    @field_validator('words')
    @classmethod
    def validate_words_unique(cls, v):
        seen = set()
        unique_words = []
        for word in v:
            word_tuple = (word.lemma, word.definition)
            if word_tuple not in seen:
                seen.add(word_tuple)
                unique_words.append(word)
        return unique_words

class UserData(BaseModel):
    user_id: str = Field(..., description="Firebase user ID")
    languages: Dict[LanguageType, List[VocabularyList]] = Field(default={}, description="User's vocabulary lists by language")
    shared_with_me: Dict[str, Dict[LanguageType, List[Any]]] = Field(default={}, description="Lists shared with this user (supports both str and Dict formats)")

class SaveSearchRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="User-given name for this search")
    app: Literal["LISTS", "STATS", "ORACLE"] = Field(..., description="Which app produced the result")
    language: LanguageType = Field(..., description="Latin or Greek")
    url: str = Field(..., description="Full relative result URL used to reload the search")

class UpdateProfileRequest(BaseModel):
    display_name: Optional[str] = Field(None, max_length=50, description="New display name")

class ListCreateRequest(BaseModel):
    list_name: str = Field(..., min_length=1, max_length=100, description="List name")
    language: LanguageType = Field(..., description="Language for the vocabulary list")
    words: List[List[str]] = Field(default=[], description="List of word pairs [lemma, definition]")
    shared: bool = Field(default=False, description="Whether this is a shared list operation")

    @field_validator('words')
    @classmethod
    def validate_word_format(cls, v):
        for word_pair in v:
            if not isinstance(word_pair, list) or len(word_pair) != 2:
                raise ValueError('Each word must be a list of exactly 2 strings [lemma, definition]')
            if not all(isinstance(item, str) and item.strip() for item in word_pair):
                raise ValueError('Word lemma and definition must be non-empty strings')
        return v

class ShareListRequest(BaseModel):
    list_name: str = Field(..., min_length=1, description="Name of list to share")
    language: LanguageType = Field(..., description="Language of the list")
    sharing_mode: ShareMode = Field(..., description="Sharing mode (copy or live)")

class AddSharedListRequest(BaseModel):
    share_link: str = Field(..., description="Share link or code")
    language: LanguageType = Field(..., description="Language of the shared list")
    mode: ShareMode = Field(default=ShareMode.COPY, description="How to add the shared list")
