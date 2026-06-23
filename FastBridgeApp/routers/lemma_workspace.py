"""
Lemmatization Workspace Router - Phases 1, 2, & 4

Handles collaborative CSV editing for lemmatized text with confidence-based highlighting.
Phase 1: project creation, CSV upload, dashboard, read-only viewing
Phase 2: cell editing, permissions management, sharing
Phase 4: comments, suggestions (with auto-approval), edit history
"""

from fastapi import APIRouter, Request, Depends, HTTPException, UploadFile, File, Form, Body
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from typing import Optional
from datetime import datetime
import uuid
from firebase_admin import auth as firebase_auth

from routers.firebase_auth import get_current_user_cookie
from mongo_connection import atlas_client
from models.lemma_models import (
    LemmaPermissionLevel,
    LemmaProject,
    LemmaRow,
    LemmaDataDocument,
    FileMetadata,
    CreateProjectRequest,
    ProjectListResponse,
    RowsResponse,
    EditAction,
    LemmaEditHistory,
    EditRowRequest,
    GrantPermissionRequest,
    ModifyPermissionRequest,
    RevokePermissionRequest,
    LemmaComment,
    LemmaSuggestion,
    SuggestionStatus,
    CreateCommentRequest,
    CreateSuggestionRequest
)
from utils.lemma_csv_parser import parse_csv_file, export_to_csv
from utils.collaboration import LemmaPermissionChecker


router = APIRouter()
templates = Jinja2Templates(directory="templates")


# ============================================================================
# Dashboard & Project Views
# ============================================================================

@router.get("/", response_class=HTMLResponse)
async def lemma_dashboard(request: Request, user=Depends(get_current_user_cookie)):
    """
    Render the lemmatization workspace dashboard.
    Shows user's projects and shared projects.
    """
    if not request.cookies.get("user_token"):
        raise HTTPException(status_code=401, detail="Not authorized")

    context = {
        "request": request,
        "username": user.get('name', 'Guest'),
        "email": user.get('email', 'No email provided'),
        "user_id": user.get('uid', None)
    }

    return templates.TemplateResponse("lemma_dashboard.html", context)


# ============================================================================
# Project Management
# ============================================================================

@router.get("/projects/list")
async def list_projects(user=Depends(get_current_user_cookie)):
    """
    Get list of user's owned and shared projects.
    """
    try:
        user_id = user.get("uid")
        storage = atlas_client.get_database("App-Storage")

        # Get user's workspace document
        workspace = storage.lemma_user_workspaces.find_one({"user_id": user_id})

        owned_projects = []
        shared_projects = []

        if workspace:
            # Get owned projects
            owned_project_ids = workspace.get("owned_projects", [])
            for project_id in owned_project_ids:
                try:
                    project = storage.lemma_projects.find_one(
                        {"project_id": project_id},
                        {"project_id": 1, "project_name": 1, "description": 1,
                         "created_at": 1, "last_modified": 1, "file_metadata": 1}
                    )
                    if project:
                        # Handle datetime fields - they might be datetime objects or strings
                        created_at = project.get("created_at")
                        if created_at and hasattr(created_at, 'isoformat'):
                            created_at = created_at.isoformat()
                        elif not isinstance(created_at, str):
                            created_at = None

                        last_modified = project.get("last_modified")
                        if last_modified and hasattr(last_modified, 'isoformat'):
                            last_modified = last_modified.isoformat()
                        elif not isinstance(last_modified, str):
                            last_modified = None

                        owned_projects.append({
                            "project_id": project.get("project_id"),
                            "project_name": project.get("project_name"),
                            "description": project.get("description"),
                            "row_count": project.get("file_metadata", {}).get("row_count", 0),
                            "created_at": created_at,
                            "last_modified": last_modified,
                            "is_owner": True
                        })
                except Exception as e:
                    print(f"Error loading owned project {project_id}: {e}")
                    continue

            # Get shared projects
            shared_with_me = workspace.get("shared_with_me", {})
            for owner_id, projects in shared_with_me.items():
                for proj_info in projects:
                    try:
                        project = storage.lemma_projects.find_one(
                            {"project_id": proj_info.get("project_id")},
                            {"project_id": 1, "project_name": 1, "description": 1,
                             "created_at": 1, "last_modified": 1, "file_metadata": 1, "owner_id": 1}
                        )
                        if project:
                            # Get owner info
                            owner = storage.user_profiles.find_one(
                                {"uid": project.get("owner_id")},
                                {"display_name": 1, "email": 1}
                            )
                            owner_name = owner.get("display_name") or owner.get("email") if owner else "Unknown"

                            # Handle datetime fields - they might be datetime objects or strings
                            created_at = project.get("created_at")
                            if created_at and hasattr(created_at, 'isoformat'):
                                created_at = created_at.isoformat()
                            elif not isinstance(created_at, str):
                                created_at = None

                            last_modified = project.get("last_modified")
                            if last_modified and hasattr(last_modified, 'isoformat'):
                                last_modified = last_modified.isoformat()
                            elif not isinstance(last_modified, str):
                                last_modified = None

                            shared_at = proj_info.get("shared_at")
                            if shared_at and hasattr(shared_at, 'isoformat'):
                                shared_at = shared_at.isoformat()
                            elif not isinstance(shared_at, str):
                                shared_at = None

                            shared_projects.append({
                                "project_id": project.get("project_id"),
                                "project_name": project.get("project_name"),
                                "description": project.get("description"),
                                "row_count": project.get("file_metadata", {}).get("row_count", 0),
                                "created_at": created_at,
                                "last_modified": last_modified,
                                "permission": proj_info.get("permission"),
                                "shared_at": shared_at,
                                "owner_name": owner_name,
                                "is_owner": False
                            })
                    except Exception as e:
                        print(f"Error loading shared project {proj_info.get('project_id')}: {e}")
                        continue

        return JSONResponse({
            "owned_projects": owned_projects,
            "shared_projects": shared_projects
        })

    except Exception as e:
        print(f"Error in list_projects: {e}")
        import traceback
        traceback.print_exc()
        # Always return valid JSON even on error
        return JSONResponse({
            "owned_projects": [],
            "shared_projects": [],
            "error": str(e)
        }, status_code=500)


@router.get("/projects/{project_id}", response_class=HTMLResponse)
async def lemma_workspace(
    request: Request,
    project_id: str,
    user=Depends(get_current_user_cookie)
):
    """
    Render the workspace view for a specific project.
    """
    if not request.cookies.get("user_token"):
        raise HTTPException(status_code=401, detail="Not authorized")

    user_id = user.get("uid")

    # Check if user has access to this project
    has_permission, permission_level = await LemmaPermissionChecker.check_project_permission(
        user_id, project_id, LemmaPermissionLevel.CAN_VIEW
    )

    if not has_permission:
        raise HTTPException(status_code=403, detail="You do not have access to this project")

    # Get project details
    storage = atlas_client.get_database("App-Storage")
    project = storage.lemma_projects.find_one({"project_id": project_id})

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Check if user is owner
    is_owner = user_id == project.get("owner_id")

    context = {
        "request": request,
        "username": user.get('name', 'Guest'),
        "email": user.get('email', ''),
        "user_id": user_id,
        "project_id": project_id,
        "project_name": project.get("project_name"),
        "is_owner": is_owner,
        "permission": permission_level.value if permission_level else "CAN_VIEW"
    }

    return templates.TemplateResponse("lemma_workspace.html", context)


@router.post("/projects/create")
async def create_project(
    project_name: str = Form(...),
    description: Optional[str] = Form(None),
    file: UploadFile = File(...),
    user=Depends(get_current_user_cookie)
):
    """
    Create a new lemmatization project with CSV upload.
    """
    user_id = user.get("uid")
    username = user.get("name", "Unknown User")
    storage = atlas_client.get_database("App-Storage")

    # Validate project name
    if not project_name or not project_name.strip():
        raise HTTPException(status_code=400, detail="Project name is required")

    project_name = project_name.strip()

    # Parse and validate CSV
    try:
        rows, column_names, metadata = await parse_csv_file(file)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing CSV: {str(e)}")

    # Generate project ID
    project_id = str(uuid.uuid4())

    # Create file metadata
    file_metadata = FileMetadata(
        original_filename=file.filename,
        row_count=metadata['row_count'],
        column_names=column_names
    )

    # Create project document
    project = LemmaProject(
        project_id=project_id,
        owner_id=user_id,
        project_name=project_name,
        description=description,
        file_metadata=file_metadata
    )

    # Insert project into database
    storage.lemma_projects.insert_one(project.model_dump(mode='json'))

    # Create data document with rows
    lemma_rows = []
    for idx, row_data in enumerate(rows):
        confidence = float(row_data.get('CONFIDENCE', 50.0))
        lemma_row = LemmaRow(
            row_index=idx,
            confidence=confidence,
            data=row_data,
            last_modified_by=user_id
        )
        lemma_rows.append(lemma_row.model_dump(mode='json'))

    data_document = {
        "project_id": project_id,
        "rows": lemma_rows
    }
    storage.lemma_data.insert_one(data_document)

    # Update user's workspace
    storage.lemma_user_workspaces.update_one(
        {"user_id": user_id},
        {
            "$push": {"owned_projects": project_id},
            "$setOnInsert": {"user_id": user_id, "shared_with_me": {}}
        },
        upsert=True
    )

    # Log project creation
    history_entry = LemmaEditHistory(
        project_id=project_id,
        row_id=None,
        user_id=user_id,
        username=username,
        action=EditAction.CREATE_PROJECT,
        changes={"project_name": project_name, "row_count": len(rows)}
    )
    storage.lemma_edit_history.insert_one(history_entry.model_dump(mode='json'))

    return JSONResponse({
        "success": True,
        "project_id": project_id,
        "project_name": project_name,
        "row_count": len(rows),
        "message": "Project created successfully"
    })


@router.delete("/projects/{project_id}")
async def delete_project(
    project_id: str,
    user=Depends(get_current_user_cookie)
):
    """
    Delete a project (owner only).
    """
    user_id = user.get("uid")
    username = user.get("name", "Unknown User")

    # Check if user is owner
    is_owner = await LemmaPermissionChecker.is_project_owner(user_id, project_id)
    if not is_owner:
        raise HTTPException(status_code=403, detail="Only the project owner can delete the project")

    storage = atlas_client.get_database("App-Storage")

    # Get project for logging
    project = storage.lemma_projects.find_one({"project_id": project_id})
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    project_name = project.get("project_name")

    # Delete project document
    storage.lemma_projects.delete_one({"project_id": project_id})

    # Delete data document
    storage.lemma_data.delete_one({"project_id": project_id})

    # Delete comments
    storage.lemma_comments.delete_many({"project_id": project_id})

    # Delete suggestions
    storage.lemma_suggestions.delete_many({"project_id": project_id})

    # Remove from owner's workspace
    storage.lemma_user_workspaces.update_one(
        {"user_id": user_id},
        {"$pull": {"owned_projects": project_id}}
    )

    # Remove from all shared users' workspaces
    storage.lemma_user_workspaces.update_many(
        {f"shared_with_me.{user_id}": {"$exists": True}},
        {"$pull": {f"shared_with_me.{user_id}": {"project_id": project_id}}}
    )

    # Log deletion
    history_entry = LemmaEditHistory(
        project_id=project_id,
        row_id=None,
        user_id=user_id,
        username=username,
        action=EditAction.DELETE_PROJECT,
        changes={"project_name": project_name}
    )
    storage.lemma_edit_history.insert_one(history_entry.model_dump(mode='json'))

    return JSONResponse({
        "success": True,
        "message": "Project deleted successfully"
    })


# ============================================================================
# Data Operations
# ============================================================================

@router.get("/projects/{project_id}/rows")
async def get_project_rows(
    project_id: str,
    page: int = 1,
    page_size: int = 100,
    user=Depends(get_current_user_cookie)
):
    """
    Get paginated rows for a project.
    """
    user_id = user.get("uid")

    # Check permission
    await LemmaPermissionChecker.require_permission(
        user_id, project_id, LemmaPermissionLevel.CAN_VIEW
    )

    storage = atlas_client.get_database("App-Storage")

    # Get data document
    data_doc = storage.lemma_data.find_one({"project_id": project_id})
    if not data_doc:
        raise HTTPException(status_code=404, detail="Project data not found")

    rows = data_doc.get("rows", [])
    total_rows = len(rows)

    # Calculate pagination
    total_pages = (total_rows + page_size - 1) // page_size if total_rows > 0 else 1
    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    paginated_rows = rows[start_idx:end_idx]

    # Convert datetime objects to strings for JSON serialization
    serialized_rows = []
    for row in paginated_rows:
        row_copy = row.copy()
        # Handle last_modified field
        if "last_modified" in row_copy and hasattr(row_copy["last_modified"], 'isoformat'):
            row_copy["last_modified"] = row_copy["last_modified"].isoformat()
        serialized_rows.append(row_copy)

    return JSONResponse({
        "rows": serialized_rows,
        "total_rows": total_rows,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages
    })


@router.get("/projects/{project_id}/export")
async def export_project(
    project_id: str,
    user=Depends(get_current_user_cookie)
):
    """
    Export project data to CSV file.
    """
    user_id = user.get("uid")

    # Check permission
    await LemmaPermissionChecker.require_permission(
        user_id, project_id, LemmaPermissionLevel.CAN_VIEW
    )

    storage = atlas_client.get_database("App-Storage")

    # Get project info
    project = storage.lemma_projects.find_one({"project_id": project_id})
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Get data
    data_doc = storage.lemma_data.find_one({"project_id": project_id})
    if not data_doc:
        raise HTTPException(status_code=404, detail="Project data not found")

    rows = data_doc.get("rows", [])
    column_names = project.get("file_metadata", {}).get("column_names", [])

    # Extract row data
    row_data_list = [row.get("data", {}) for row in rows]

    # Generate filename
    project_name = project.get("project_name", "project").replace(" ", "_")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{project_name}_export_{timestamp}.csv"

    # Export to CSV
    try:
        csv_path = await export_to_csv(row_data_list, column_names, filename)
        return FileResponse(
            path=csv_path,
            filename=filename,
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error exporting CSV: {str(e)}")


# ============================================================================
# Project Info
# ============================================================================

@router.get("/projects/{project_id}/info")
async def get_project_info(
    project_id: str,
    user=Depends(get_current_user_cookie)
):
    """
    Get detailed information about a project.
    """
    user_id = user.get("uid")

    # Check permission
    has_permission, permission_level = await LemmaPermissionChecker.check_project_permission(
        user_id, project_id, LemmaPermissionLevel.CAN_VIEW
    )

    if not has_permission:
        raise HTTPException(status_code=403, detail="You do not have access to this project")

    storage = atlas_client.get_database("App-Storage")

    # Get project
    project = storage.lemma_projects.find_one({"project_id": project_id})
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Check if user is owner
    is_owner = user_id == project.get("owner_id")

    # Get owner info
    owner = storage.user_profiles.find_one(
        {"uid": project.get("owner_id")},
        {"display_name": 1, "email": 1}
    )
    owner_name = owner.get("display_name") or owner.get("email") if owner else "Unknown"

    # Count collaborators
    permissions = project.get("permissions", {})
    collaborator_count = len(permissions)

    return JSONResponse({
        "project_id": project.get("project_id"),
        "project_name": project.get("project_name"),
        "description": project.get("description"),
        "owner_id": project.get("owner_id"),
        "owner_name": owner_name,
        "is_owner": is_owner,
        "user_permission": permission_level.value if permission_level else None,
        "created_at": project.get("created_at").isoformat() if project.get("created_at") else None,
        "last_modified": project.get("last_modified").isoformat() if project.get("last_modified") else None,
        "file_metadata": project.get("file_metadata"),
        "collaborator_count": collaborator_count
    })


# ============================================================================
# Phase 2: Cell Editing
# ============================================================================

@router.patch("/projects/{project_id}/rows/{row_id}")
async def edit_row_cell(
    project_id: str,
    row_id: str,
    edit_request: EditRowRequest,
    user=Depends(get_current_user_cookie)
):
    """
    Edit a single cell in a row (requires CAN_EDIT permission).
    """
    user_id = user.get("uid")
    username = user.get("name", "Unknown User")

    # Check permission
    await LemmaPermissionChecker.require_permission(
        user_id, project_id, LemmaPermissionLevel.CAN_EDIT
    )

    storage = atlas_client.get_database("App-Storage")

    # Get project data
    data_doc = storage.lemma_data.find_one({"project_id": project_id})
    if not data_doc:
        raise HTTPException(status_code=404, detail="Project data not found")

    # Find the specific row
    rows = data_doc.get("rows", [])
    row_index = None
    old_value = None

    for idx, row in enumerate(rows):
        if row.get("row_id") == row_id:
            row_index = idx
            old_value = row.get("data", {}).get(edit_request.field)
            break

    if row_index is None:
        raise HTTPException(status_code=404, detail="Row not found")

    # Validate field exists
    if edit_request.field not in rows[row_index].get("data", {}):
        raise HTTPException(status_code=400, detail=f"Field '{edit_request.field}' does not exist")

    # Update the cell value
    now = datetime.now()
    update_fields = {
        f"rows.$.data.{edit_request.field}": edit_request.new_value,
        "rows.$.last_modified": now,
        "rows.$.last_modified_by": user_id
    }

    # If editing CONFIDENCE field, also update the row-level confidence for highlighting
    if edit_request.field.upper() == "CONFIDENCE":
        try:
            confidence_value = float(edit_request.new_value)
            # Clamp confidence between 0 and 100
            confidence_value = max(0.0, min(100.0, confidence_value))
            # Update the display value in data to match the clamped value
            update_fields[f"rows.$.data.{edit_request.field}"] = str(confidence_value)
            update_fields["rows.$.confidence"] = confidence_value
        except (ValueError, TypeError):
            raise HTTPException(status_code=400, detail="CONFIDENCE must be a valid number")

    update_result = storage.lemma_data.update_one(
        {"project_id": project_id, "rows.row_id": row_id},
        {"$set": update_fields}
    )

    if update_result.modified_count == 0:
        raise HTTPException(status_code=500, detail="Failed to update row")

    # Update project last_modified
    storage.lemma_projects.update_one(
        {"project_id": project_id},
        {"$set": {"last_modified": now}}
    )

    # Log the edit
    history_entry = LemmaEditHistory(
        project_id=project_id,
        row_id=row_id,
        user_id=user_id,
        username=username,
        action=EditAction.EDIT,
        changes={
            "field": edit_request.field,
            "old_value": old_value,
            "new_value": edit_request.new_value
        }
    )
    storage.lemma_edit_history.insert_one(history_entry.model_dump(mode='json'))

    response_data = {
        "success": True,
        "message": "Cell updated successfully",
        "row_id": row_id,
        "field": edit_request.field,
        "new_value": edit_request.new_value,
        "last_modified": now.isoformat(),
        "last_modified_by": user_id
    }

    # Include updated confidence if CONFIDENCE field was edited
    if edit_request.field.upper() == "CONFIDENCE":
        response_data["confidence"] = confidence_value
        # Return the clamped value so the cell displays correctly
        response_data["new_value"] = str(confidence_value)

    return JSONResponse(response_data)


# ============================================================================
# Phase 2: Permission Management
# ============================================================================

@router.post("/projects/{project_id}/permissions/grant")
async def grant_permission(
    project_id: str,
    request: GrantPermissionRequest,
    user=Depends(get_current_user_cookie)
):
    """
    Grant permission to another user (owner only).
    """
    user_id = user.get("uid")
    username = user.get("name", "Unknown User")

    # Check if user is owner
    is_owner = await LemmaPermissionChecker.is_project_owner(user_id, project_id)
    if not is_owner:
        raise HTTPException(status_code=403, detail="Only the project owner can grant permissions")

    storage = atlas_client.get_database("App-Storage")

    # Get project
    project = storage.lemma_projects.find_one({"project_id": project_id})
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Resolve recipient email to user ID
    try:
        recipient_user = firebase_auth.get_user_by_email(request.recipient_email)
        recipient_id = recipient_user.uid
        recipient_name = recipient_user.display_name or recipient_user.email
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"User with email '{request.recipient_email}' not found")

    # Check if recipient is the owner
    if recipient_id == user_id:
        raise HTTPException(status_code=400, detail="Cannot grant permission to yourself (you're the owner)")

    # Check if permission already exists
    existing_permissions = project.get("permissions", {})
    if recipient_id in existing_permissions:
        raise HTTPException(
            status_code=400,
            detail=f"User already has {existing_permissions[recipient_id]['level']} permission"
        )

    # Grant permission
    now = datetime.now()
    permission_grant = {
        "level": request.permission.value,
        "granted_at": now,
        "granted_by": user_id
    }

    storage.lemma_projects.update_one(
        {"project_id": project_id},
        {"$set": {f"permissions.{recipient_id}": permission_grant}}
    )

    # Add to recipient's shared_with_me
    storage.lemma_user_workspaces.update_one(
        {"user_id": recipient_id},
        {
            "$push": {
                f"shared_with_me.{user_id}": {
                    "project_id": project_id,
                    "project_name": project.get("project_name"),
                    "permission": request.permission.value,
                    "shared_at": now
                }
            },
            "$setOnInsert": {"user_id": recipient_id, "owned_projects": []}
        },
        upsert=True
    )

    # Log the action
    history_entry = LemmaEditHistory(
        project_id=project_id,
        row_id=None,
        user_id=user_id,
        username=username,
        action=EditAction.GRANT_PERMISSION,
        changes={
            "recipient_id": recipient_id,
            "recipient_email": request.recipient_email,
            "permission": request.permission.value
        }
    )
    storage.lemma_edit_history.insert_one(history_entry.model_dump(mode='json'))

    return JSONResponse({
        "success": True,
        "message": f"Permission granted to {request.recipient_email}",
        "recipient_id": recipient_id,
        "recipient_name": recipient_name,
        "permission": request.permission.value
    })


@router.patch("/projects/{project_id}/permissions/modify")
async def modify_permission(
    project_id: str,
    request: ModifyPermissionRequest,
    user=Depends(get_current_user_cookie)
):
    """
    Modify an existing user's permission (owner only).
    """
    user_id = user.get("uid")
    username = user.get("name", "Unknown User")

    # Check if user is owner
    is_owner = await LemmaPermissionChecker.is_project_owner(user_id, project_id)
    if not is_owner:
        raise HTTPException(status_code=403, detail="Only the project owner can modify permissions")

    storage = atlas_client.get_database("App-Storage")

    # Get project
    project = storage.lemma_projects.find_one({"project_id": project_id})
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Check if permission exists
    existing_permissions = project.get("permissions", {})
    if request.recipient_id not in existing_permissions:
        raise HTTPException(status_code=404, detail="User does not have access to this project")

    old_permission = existing_permissions[request.recipient_id]["level"]

    # Update permission
    storage.lemma_projects.update_one(
        {"project_id": project_id},
        {"$set": {f"permissions.{request.recipient_id}.level": request.new_permission.value}}
    )

    # Update in recipient's shared_with_me
    storage.lemma_user_workspaces.update_one(
        {"user_id": request.recipient_id, f"shared_with_me.{user_id}.project_id": project_id},
        {"$set": {f"shared_with_me.{user_id}.$.permission": request.new_permission.value}}
    )

    # Log the action
    history_entry = LemmaEditHistory(
        project_id=project_id,
        row_id=None,
        user_id=user_id,
        username=username,
        action=EditAction.GRANT_PERMISSION,
        changes={
            "recipient_id": request.recipient_id,
            "old_permission": old_permission,
            "new_permission": request.new_permission.value
        }
    )
    storage.lemma_edit_history.insert_one(history_entry.model_dump(mode='json'))

    return JSONResponse({
        "success": True,
        "message": "Permission updated successfully",
        "recipient_id": request.recipient_id,
        "new_permission": request.new_permission.value
    })


@router.delete("/projects/{project_id}/permissions/revoke")
async def revoke_permission(
    project_id: str,
    request: RevokePermissionRequest,
    user=Depends(get_current_user_cookie)
):
    """
    Revoke a user's permission (owner only).
    """
    user_id = user.get("uid")
    username = user.get("name", "Unknown User")

    # Check if user is owner
    is_owner = await LemmaPermissionChecker.is_project_owner(user_id, project_id)
    if not is_owner:
        raise HTTPException(status_code=403, detail="Only the project owner can revoke permissions")

    storage = atlas_client.get_database("App-Storage")

    # Get project
    project = storage.lemma_projects.find_one({"project_id": project_id})
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Check if permission exists
    existing_permissions = project.get("permissions", {})
    if request.recipient_id not in existing_permissions:
        raise HTTPException(status_code=404, detail="User does not have access to this project")

    # Remove permission
    storage.lemma_projects.update_one(
        {"project_id": project_id},
        {"$unset": {f"permissions.{request.recipient_id}": ""}}
    )

    # Remove from recipient's shared_with_me
    storage.lemma_user_workspaces.update_one(
        {"user_id": request.recipient_id},
        {"$pull": {f"shared_with_me.{user_id}": {"project_id": project_id}}}
    )

    # Log the action
    history_entry = LemmaEditHistory(
        project_id=project_id,
        row_id=None,
        user_id=user_id,
        username=username,
        action=EditAction.REVOKE_PERMISSION,
        changes={
            "recipient_id": request.recipient_id,
            "revoked_permission": existing_permissions[request.recipient_id]["level"]
        }
    )
    storage.lemma_edit_history.insert_one(history_entry.model_dump(mode='json'))

    return JSONResponse({
        "success": True,
        "message": "Permission revoked successfully",
        "recipient_id": request.recipient_id
    })


@router.get("/projects/{project_id}/permissions/list")
async def list_permissions(
    project_id: str,
    user=Depends(get_current_user_cookie)
):
    """
    List all users with access to the project (owner only).
    """
    user_id = user.get("uid")

    # Check if user is owner
    is_owner = await LemmaPermissionChecker.is_project_owner(user_id, project_id)
    if not is_owner:
        raise HTTPException(status_code=403, detail="Only the project owner can view permissions")

    storage = atlas_client.get_database("App-Storage")

    # Get project
    project = storage.lemma_projects.find_one({"project_id": project_id})
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    permissions_data = []
    for recipient_id, perm_info in project.get("permissions", {}).items():
        # Get user info from Firebase
        try:
            user_info = firebase_auth.get_user(recipient_id)
            email = user_info.email
            display_name = user_info.display_name or email
        except:
            email = "Unknown"
            display_name = "Unknown User"

        permissions_data.append({
            "user_id": recipient_id,
            "email": email,
            "username": display_name,
            "permission": perm_info.get("level"),
            "granted_at": perm_info.get("granted_at").isoformat() if perm_info.get("granted_at") else None,
            "granted_by": perm_info.get("granted_by")
        })

    return JSONResponse({
        "permissions": permissions_data,
        "total": len(permissions_data)
    })


# ============================================================================
# Phase 4: Comments & Suggestions
# ============================================================================

@router.post("/projects/{project_id}/rows/{row_id}/comments")
async def add_comment(
    project_id: str,
    row_id: str,
    request: CreateCommentRequest,
    user=Depends(get_current_user_cookie)
):
    """
    Add a comment to a specific row.
    Requires CAN_VIEW permission minimum.
    """
    user_id = user.get("uid")
    username = user.get("name", "Unknown User")

    # Check permission (CAN_VIEW minimum)
    await LemmaPermissionChecker.require_permission(user_id, project_id, LemmaPermissionLevel.CAN_VIEW)

    storage = atlas_client.get_database("App-Storage")

    # Verify row exists
    data_doc = storage.lemma_data.find_one({"project_id": project_id})
    if not data_doc:
        raise HTTPException(status_code=404, detail="Project data not found")

    row_exists = any(row.get("row_id") == row_id for row in data_doc.get("rows", []))
    if not row_exists:
        raise HTTPException(status_code=404, detail="Row not found")

    # Create comment
    comment = LemmaComment(
        project_id=project_id,
        row_id=row_id,
        user_id=user_id,
        username=username,
        comment_text=request.comment_text
    )

    storage.lemma_comments.insert_one(comment.model_dump(mode='json'))

    # Log the action
    history_entry = LemmaEditHistory(
        project_id=project_id,
        row_id=row_id,
        user_id=user_id,
        username=username,
        action=EditAction.COMMENT,
        changes={"comment_text": request.comment_text}
    )
    storage.lemma_edit_history.insert_one(history_entry.model_dump(mode='json'))

    return JSONResponse({
        "success": True,
        "comment_id": comment.comment_id,
        "created_at": comment.created_at.isoformat(),
        "username": username
    })


@router.get("/projects/{project_id}/comments")
async def get_all_project_comments(
    project_id: str,
    user=Depends(get_current_user_cookie)
):
    """
    Get all comments for a project (all rows at once).
    Much more efficient than fetching per-row.
    Requires CAN_VIEW permission minimum.
    """
    user_id = user.get("uid")

    # Check permission
    await LemmaPermissionChecker.require_permission(user_id, project_id, LemmaPermissionLevel.CAN_VIEW)

    storage = atlas_client.get_database("App-Storage")

    # Get all comments for this project
    comments = list(storage.lemma_comments.find(
        {"project_id": project_id},
        sort=[("created_at", -1)]  # Most recent first
    ))

    # Serialize datetime fields
    serialized_comments = []
    for comment in comments:
        comment_copy = comment.copy()
        if "_id" in comment_copy:
            del comment_copy["_id"]
        if "created_at" in comment_copy and hasattr(comment_copy["created_at"], 'isoformat'):
            comment_copy["created_at"] = comment_copy["created_at"].isoformat()
        serialized_comments.append(comment_copy)

    return JSONResponse({
        "comments": serialized_comments,
        "total": len(serialized_comments)
    })


@router.get("/projects/{project_id}/rows/{row_id}/comments")
async def get_row_comments(
    project_id: str,
    row_id: str,
    user=Depends(get_current_user_cookie)
):
    """
    Get all comments for a specific row.
    Requires CAN_VIEW permission minimum.
    NOTE: Consider using GET /projects/{project_id}/comments to fetch all at once (more efficient).
    """
    user_id = user.get("uid")

    # Check permission
    await LemmaPermissionChecker.require_permission(user_id, project_id, LemmaPermissionLevel.CAN_VIEW)

    storage = atlas_client.get_database("App-Storage")

    # Get comments
    comments = list(storage.lemma_comments.find(
        {"project_id": project_id, "row_id": row_id},
        sort=[("created_at", 1)]
    ))

    # Serialize datetime fields
    serialized_comments = []
    for comment in comments:
        comment_copy = comment.copy()
        if "_id" in comment_copy:
            del comment_copy["_id"]
        if "created_at" in comment_copy and hasattr(comment_copy["created_at"], 'isoformat'):
            comment_copy["created_at"] = comment_copy["created_at"].isoformat()
        serialized_comments.append(comment_copy)

    return JSONResponse({
        "comments": serialized_comments,
        "total": len(serialized_comments)
    })


@router.delete("/projects/{project_id}/comments/{comment_id}")
async def delete_comment(
    project_id: str,
    comment_id: str,
    user=Depends(get_current_user_cookie)
):
    """
    Delete a comment.
    Only comment author or project owner can delete.
    """
    user_id = user.get("uid")

    # Check permission
    await LemmaPermissionChecker.require_permission(user_id, project_id, LemmaPermissionLevel.CAN_VIEW)

    storage = atlas_client.get_database("App-Storage")

    # Get comment
    comment = storage.lemma_comments.find_one({"comment_id": comment_id, "project_id": project_id})
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    # Check if user is comment author or project owner
    is_owner = await LemmaPermissionChecker.is_project_owner(user_id, project_id)
    is_author = comment.get("user_id") == user_id

    if not (is_owner or is_author):
        raise HTTPException(status_code=403, detail="Only comment author or project owner can delete comments")

    # Delete comment
    storage.lemma_comments.delete_one({"comment_id": comment_id})

    return JSONResponse({
        "success": True,
        "message": "Comment deleted successfully"
    })


@router.post("/projects/{project_id}/suggestions")
async def create_suggestion(
    project_id: str,
    request: CreateSuggestionRequest,
    user=Depends(get_current_user_cookie)
):
    """
    Create an edit suggestion.
    Suggestions are ALWAYS created as pending, even for owners/CAN_EDIT users.
    This allows users to review their own suggestions before applying them.
    """
    user_id = user.get("uid")
    username = user.get("name", "Unknown User")

    # Check permission (CAN_VIEW minimum)
    has_permission, actual_permission = await LemmaPermissionChecker.check_project_permission(
        user_id, project_id, LemmaPermissionLevel.CAN_VIEW
    )
    if not has_permission:
        raise HTTPException(status_code=403, detail="Insufficient permissions")

    storage = atlas_client.get_database("App-Storage")

    # Get row data
    data_doc = storage.lemma_data.find_one({"project_id": project_id})
    if not data_doc:
        raise HTTPException(status_code=404, detail="Project data not found")

    # Find the row
    target_row = None
    for row in data_doc.get("rows", []):
        if row.get("row_id") == request.row_id:
            target_row = row
            break

    if not target_row:
        raise HTTPException(status_code=404, detail="Row not found")

    # Build original data and changes
    original_data = target_row.get("data", {})
    changes_dict = {}
    suggested_data = original_data.copy()

    for field, new_value in request.changes.items():
        old_value = original_data.get(field, "")
        changes_dict[field] = {"from": old_value, "to": new_value}
        suggested_data[field] = new_value

    # Create pending suggestion (no auto-approval)
    suggestion = LemmaSuggestion(
        project_id=project_id,
        row_id=request.row_id,
        suggested_by=user_id,
        suggested_by_name=username,
        status=SuggestionStatus.PENDING,
        original_data=original_data,
        suggested_data=suggested_data,
        changes=changes_dict,
        comment=request.comment
    )

    storage.lemma_suggestions.insert_one(suggestion.model_dump(mode='json'))

    # Log the suggestion
    history_entry = LemmaEditHistory(
        project_id=project_id,
        row_id=request.row_id,
        user_id=user_id,
        username=username,
        action=EditAction.SUGGEST,
        changes=changes_dict
    )
    storage.lemma_edit_history.insert_one(history_entry.model_dump(mode='json'))

    return JSONResponse({
        "success": True,
        "auto_approved": False,
        "suggestion_id": suggestion.suggestion_id,
        "status": "pending",
        "message": "Suggestion created and pending review"
    })


@router.get("/projects/{project_id}/suggestions")
async def get_suggestions(
    project_id: str,
    status: Optional[str] = None,
    user=Depends(get_current_user_cookie)
):
    """
    Get all suggestions for a project.
    Optional filter by status (pending, accepted, rejected).
    Requires CAN_VIEW permission minimum.
    """
    user_id = user.get("uid")

    # Check permission
    await LemmaPermissionChecker.require_permission(user_id, project_id, LemmaPermissionLevel.CAN_VIEW)

    storage = atlas_client.get_database("App-Storage")

    # Build query
    query = {"project_id": project_id}
    if status:
        query["status"] = status

    # Get suggestions
    suggestions = list(storage.lemma_suggestions.find(query, sort=[("created_at", -1)]))

    # Serialize
    serialized_suggestions = []
    for suggestion in suggestions:
        suggestion_copy = suggestion.copy()
        if "_id" in suggestion_copy:
            del suggestion_copy["_id"]
        if "created_at" in suggestion_copy and hasattr(suggestion_copy["created_at"], 'isoformat'):
            suggestion_copy["created_at"] = suggestion_copy["created_at"].isoformat()
        serialized_suggestions.append(suggestion_copy)

    return JSONResponse({
        "suggestions": serialized_suggestions,
        "total": len(serialized_suggestions)
    })


@router.post("/projects/{project_id}/suggestions/{suggestion_id}/accept")
async def approve_suggestion(
    project_id: str,
    suggestion_id: str,
    user=Depends(get_current_user_cookie)
):
    """
    Approve and apply a pending suggestion.
    Only project owner or users with CAN_EDIT can approve.
    """
    user_id = user.get("uid")
    username = user.get("name", "Unknown User")

    # Check permission (CAN_EDIT required)
    await LemmaPermissionChecker.require_permission(user_id, project_id, LemmaPermissionLevel.CAN_EDIT)

    storage = atlas_client.get_database("App-Storage")

    # Get suggestion
    suggestion = storage.lemma_suggestions.find_one({
        "suggestion_id": suggestion_id,
        "project_id": project_id
    })
    if not suggestion:
        raise HTTPException(status_code=404, detail="Suggestion not found")

    if suggestion.get("status") != "pending":
        raise HTTPException(status_code=400, detail=f"Suggestion is already {suggestion.get('status')}")

    # Apply the suggested changes
    now = datetime.now()
    update_fields = {}
    confidence_value = None

    for field, new_value in suggestion.get("suggested_data", {}).items():
        update_fields[f"rows.$.data.{field}"] = new_value

        # Handle CONFIDENCE field
        if field.upper() == "CONFIDENCE":
            try:
                confidence_value = float(new_value)
                confidence_value = max(0.0, min(100.0, confidence_value))
                update_fields[f"rows.$.data.{field}"] = str(confidence_value)
                update_fields["rows.$.confidence"] = confidence_value
            except (ValueError, TypeError):
                pass

    update_fields["rows.$.last_modified"] = now
    update_fields["rows.$.last_modified_by"] = user_id

    # Apply to row
    storage.lemma_data.update_one(
        {"project_id": project_id, "rows.row_id": suggestion.get("row_id")},
        {"$set": update_fields}
    )

    # Update project
    storage.lemma_projects.update_one(
        {"project_id": project_id},
        {"$set": {"last_modified": now}}
    )

    # Update suggestion status
    storage.lemma_suggestions.update_one(
        {"suggestion_id": suggestion_id},
        {"$set": {"status": "accepted"}}
    )

    # Log the approval
    history_entry = LemmaEditHistory(
        project_id=project_id,
        row_id=suggestion.get("row_id"),
        user_id=user_id,
        username=username,
        action=EditAction.ACCEPT_SUGGESTION,
        changes=suggestion.get("changes")
    )
    storage.lemma_edit_history.insert_one(history_entry.model_dump(mode='json'))

    return JSONResponse({
        "success": True,
        "message": "Suggestion approved and applied",
        "row_id": suggestion.get("row_id"),
        "applied_data": suggestion.get("suggested_data"),
        "last_modified": now.isoformat(),
        "last_modified_by": user_id,
        "confidence": confidence_value
    })


@router.post("/projects/{project_id}/suggestions/{suggestion_id}/reject")
async def reject_suggestion(
    project_id: str,
    suggestion_id: str,
    user=Depends(get_current_user_cookie)
):
    """
    Reject a pending suggestion.
    Only project owner or users with CAN_EDIT can reject.
    """
    user_id = user.get("uid")
    username = user.get("name", "Unknown User")

    # Check permission (CAN_EDIT required)
    await LemmaPermissionChecker.require_permission(user_id, project_id, LemmaPermissionLevel.CAN_EDIT)

    storage = atlas_client.get_database("App-Storage")

    # Get suggestion
    suggestion = storage.lemma_suggestions.find_one({
        "suggestion_id": suggestion_id,
        "project_id": project_id
    })
    if not suggestion:
        raise HTTPException(status_code=404, detail="Suggestion not found")

    if suggestion.get("status") != "pending":
        raise HTTPException(status_code=400, detail=f"Suggestion is already {suggestion.get('status')}")

    # Update suggestion status
    storage.lemma_suggestions.update_one(
        {"suggestion_id": suggestion_id},
        {"$set": {"status": "rejected"}}
    )

    # Log the rejection
    history_entry = LemmaEditHistory(
        project_id=project_id,
        row_id=suggestion.get("row_id"),
        user_id=user_id,
        username=username,
        action=EditAction.REJECT_SUGGESTION,
        changes=suggestion.get("changes")
    )
    storage.lemma_edit_history.insert_one(history_entry.model_dump(mode='json'))

    return JSONResponse({
        "success": True,
        "message": "Suggestion rejected"
    })


@router.get("/projects/{project_id}/history")
async def get_edit_history(
    project_id: str,
    row_id: Optional[str] = None,
    action: Optional[str] = None,
    limit: int = 100,
    user=Depends(get_current_user_cookie)
):
    """
    Get edit history for a project.
    Optional filters: row_id, action type, limit.
    Requires CAN_VIEW permission minimum.
    """
    user_id = user.get("uid")

    # Check permission
    await LemmaPermissionChecker.require_permission(user_id, project_id, LemmaPermissionLevel.CAN_VIEW)

    storage = atlas_client.get_database("App-Storage")

    # Build query
    query = {"project_id": project_id}
    if row_id:
        query["row_id"] = row_id
    if action:
        query["action"] = action

    # Get history entries
    history_entries = list(storage.lemma_edit_history.find(
        query,
        sort=[("timestamp", -1)],
        limit=min(limit, 1000)  # Cap at 1000
    ))

    # Serialize
    serialized_history = []
    for entry in history_entries:
        entry_copy = entry.copy()
        if "_id" in entry_copy:
            del entry_copy["_id"]
        if "timestamp" in entry_copy and hasattr(entry_copy["timestamp"], 'isoformat'):
            entry_copy["timestamp"] = entry_copy["timestamp"].isoformat()
        serialized_history.append(entry_copy)

    return JSONResponse({
        "history": serialized_history,
        "total": len(serialized_history)
    })
