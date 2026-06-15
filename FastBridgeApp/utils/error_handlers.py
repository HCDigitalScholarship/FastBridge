from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
import logging
from datetime import datetime
from typing import Dict, Any
import traceback

logger = logging.getLogger(__name__)
templates = Jinja2Templates(directory="templates")

class FastBridgeException(HTTPException):
    """Base exception class for FastBridge application"""

    def __init__(self, status_code: int, detail: str, error_code: str = None, context: Dict[str, Any] = None):
        super().__init__(status_code=status_code, detail=detail)
        self.error_code = error_code
        self.context = context or {}

class ValidationError(FastBridgeException):
    """Raised when input validation fails"""

    def __init__(self, detail: str, field: str = None):
        super().__init__(
            status_code=422,
            detail=detail,
            error_code="VALIDATION_ERROR",
            context={"field": field} if field else {}
        )

class AuthenticationError(FastBridgeException):
    """Raised when authentication fails"""

    def __init__(self, detail: str = "Authentication failed"):
        super().__init__(
            status_code=401,
            detail=detail,
            error_code="AUTH_ERROR"
        )

class AuthorizationError(FastBridgeException):
    """Raised when authorization fails"""

    def __init__(self, detail: str = "Access denied"):
        super().__init__(
            status_code=403,
            detail=detail,
            error_code="AUTHZ_ERROR"
        )

class ResourceNotFoundError(FastBridgeException):
    """Raised when a requested resource is not found"""

    def __init__(self, resource_type: str, resource_id: str = None):
        detail = f"{resource_type} not found"
        if resource_id:
            detail += f" (ID: {resource_id})"

        super().__init__(
            status_code=404,
            detail=detail,
            error_code="RESOURCE_NOT_FOUND",
            context={"resource_type": resource_type, "resource_id": resource_id}
        )

class DatabaseError(FastBridgeException):
    """Raised when database operations fail"""

    def __init__(self, detail: str = "Database operation failed", operation: str = None):
        super().__init__(
            status_code=500,
            detail=detail,
            error_code="DATABASE_ERROR",
            context={"operation": operation} if operation else {}
        )

class RateLimitError(FastBridgeException):
    """Raised when rate limit is exceeded"""

    def __init__(self, detail: str = "Rate limit exceeded"):
        super().__init__(
            status_code=429,
            detail=detail,
            error_code="RATE_LIMIT_EXCEEDED"
        )

class ExternalServiceError(FastBridgeException):
    """Raised when external service calls fail"""

    def __init__(self, service: str, detail: str = None):
        detail = detail or f"{service} service unavailable"
        super().__init__(
            status_code=503,
            detail=detail,
            error_code="EXTERNAL_SERVICE_ERROR",
            context={"service": service}
        )

def format_error_response(
    request: Request,
    exc: Exception,
    include_traceback: bool = False
) -> Dict[str, Any]:
    """Format error response with consistent structure"""

    error_response = {
        "error": {
            "timestamp": datetime.now().isoformat(),
            "path": str(request.url),
            "method": request.method,
            "message": "An error occurred"
        }
    }

    if isinstance(exc, FastBridgeException):
        error_response["error"].update({
            "message": exc.detail,
            "code": exc.error_code,
            "status_code": exc.status_code,
            "context": exc.context
        })
    elif isinstance(exc, HTTPException):
        error_response["error"].update({
            "message": exc.detail,
            "status_code": exc.status_code,
            "code": "HTTP_EXCEPTION"
        })
    else:
        # Generic error handling
        error_response["error"].update({
            "message": "Internal server error",
            "status_code": 500,
            "code": "INTERNAL_ERROR"
        })

    if include_traceback and not isinstance(exc, (FastBridgeException, HTTPException)):
        error_response["error"]["traceback"] = traceback.format_exc()

    return error_response

async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """Handle HTTP exceptions with consistent formatting"""

    # Log the error
    logger.error(
        f"HTTP Exception: {exc.status_code} - {exc.detail}",
        extra={
            "status_code": exc.status_code,
            "path": str(request.url),
            "method": request.method,
            "client_ip": request.client.host if request.client else "unknown"
        }
    )

    error_response = format_error_response(request, exc)
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response
    )

async def fastbridge_exception_handler(request: Request, exc: FastBridgeException) -> JSONResponse:
    """Handle custom FastBridge exceptions"""

    # Log the error with context
    logger.error(
        f"FastBridge Exception: {exc.error_code} - {exc.detail}",
        extra={
            "error_code": exc.error_code,
            "status_code": exc.status_code,
            "context": exc.context,
            "path": str(request.url),
            "method": request.method,
            "client_ip": request.client.host if request.client else "unknown"
        }
    )

    error_response = format_error_response(request, exc)
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response
    )

async def validation_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle Pydantic validation exceptions"""

    logger.warning(
        f"Validation error: {str(exc)}",
        extra={
            "path": str(request.url),
            "method": request.method,
            "client_ip": request.client.host if request.client else "unknown"
        }
    )

    # Extract field-specific errors from Pydantic ValidationError
    errors = []
    if hasattr(exc, 'errors'):
        for error in exc.errors():
            field_name = '.'.join(str(loc) for loc in error['loc'])
            errors.append({
                "field": field_name,
                "message": error['msg'],
                "type": error['type']
            })

    error_response = {
        "error": {
            "timestamp": datetime.now().isoformat(),
            "path": str(request.url),
            "method": request.method,
            "message": "Validation failed",
            "code": "VALIDATION_ERROR",
            "status_code": 422,
            "details": errors
        }
    }

    return JSONResponse(status_code=422, content=error_response)

async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle unexpected exceptions"""

    # Log the full error with traceback
    logger.error(
        f"Unhandled exception: {type(exc).__name__}: {str(exc)}",
        exc_info=True,
        extra={
            "path": str(request.url),
            "method": request.method,
            "client_ip": request.client.host if request.client else "unknown",
            "exception_type": type(exc).__name__
        }
    )

    # Don't expose internal error details in production
    error_response = format_error_response(request, exc, include_traceback=False)
    return JSONResponse(status_code=500, content=error_response)

# Error response templates for HTML pages
async def render_error_page(request: Request, status_code: int, message: str = None):
    """Render error page for browser requests"""

    default_messages = {
        400: "Bad Request",
        401: "Unauthorized",
        403: "Forbidden",
        404: "Page Not Found",
        500: "Internal Server Error",
        503: "Service Unavailable"
    }

    context = {
        "request": request,
        "status_code": status_code,
        "message": message or default_messages.get(status_code, "An error occurred")
    }

    return templates.TemplateResponse(
        "error.html",
        context,
        status_code=status_code
    )

def log_user_action(
    user_id: str,
    action: str,
    resource: str,
    success: bool = True,
    details: Dict[str, Any] = None,
    request: Request = None
):
    """Log user action for audit trail"""

    log_data = {
        "user_id": user_id,
        "action": action,
        "resource": resource,
        "success": success,
        "timestamp": datetime.now().isoformat(),
        "details": details or {}
    }

    if request:
        log_data.update({
            "ip_address": request.client.host if request.client else "unknown",
            "user_agent": request.headers.get("User-Agent", ""),
            "path": str(request.url),
            "method": request.method
        })

    if success:
        logger.info(f"User action: {action}", extra=log_data)
    else:
        logger.warning(f"Failed user action: {action}", extra=log_data)

    return log_data