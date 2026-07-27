"""
CSV parser for Lemmatization Workspace with security sanitization.

Handles CSV file parsing, validation, and export with protection against:
- XSS (Cross-Site Scripting)
- CSV Injection
- Various encoding issues
- Malformed data
"""

import csv
import io
import re
import tempfile
from typing import Tuple, List, Dict, Optional
from fastapi import UploadFile, HTTPException
from datetime import datetime
import uuid
import chardet
from html import escape


# Constants
MAX_FILE_SIZE_MB = 50
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024
REQUIRED_COLUMNS = {'TITLE', 'LOCATION', 'SECTION', 'RUNNINGCOUNT', 'TEXT'}
OPTIONAL_COLUMNS = {'CONFIDENCE'}


def sanitize_csv_value(value: str) -> str:
    """
    Sanitize a single CSV cell value to prevent XSS and CSV injection.

    Security measures:
    1. CSV Injection Prevention: Prefix formulas with single quote
    2. XSS Prevention: Remove HTML tags and escape special characters
    3. Null byte removal
    4. Line break normalization

    Args:
        value: Raw cell value from CSV

    Returns:
        Sanitized value safe for storage and display
    """
    if not value or not isinstance(value, str):
        return ""

    # Remove null bytes (can cause issues with storage)
    value = value.replace('\x00', '')

    # CSV Injection Prevention
    # Formulas starting with =, +, -, @, or | could be dangerous
    if value and value[0] in ['=', '+', '-', '@', '|']:
        value = "'" + value

    # Tab characters (potential CSV injection vector)
    if value.startswith('\t'):
        value = "'" + value

    # XSS Prevention: Remove HTML tags
    value = re.sub(r'<[^>]+>', '', value)

    # Escape special HTML characters
    value = escape(value)

    # Normalize line breaks (replace with space)
    value = value.replace('\r\n', ' ').replace('\r', ' ').replace('\n', ' ')

    # Remove excessive whitespace
    value = ' '.join(value.split())

    return value.strip()


def detect_encoding(file_content: bytes) -> str:
    """
    Detect the encoding of CSV file content.

    Args:
        file_content: Raw bytes from uploaded file

    Returns:
        Detected encoding string
    """
    # Try UTF-8 with BOM first
    if file_content.startswith(b'\xef\xbb\xbf'):
        return 'utf-8-sig'

    # Use chardet for detection
    result = chardet.detect(file_content)
    encoding = result.get('encoding', 'utf-8')

    # Fallback to utf-8 if detection fails
    if not encoding:
        encoding = 'utf-8'

    return encoding


def validate_csv_structure(columns: List[str]) -> Tuple[bool, Optional[str]]:
    """
    Validate that CSV has all required columns.

    Args:
        columns: List of column names from CSV header

    Returns:
        Tuple of (is_valid, error_message)
    """
    # Normalize column names (strip whitespace, uppercase)
    normalized_columns = {col.strip().upper() for col in columns}

    # Check for required columns
    missing_columns = REQUIRED_COLUMNS - normalized_columns

    if missing_columns:
        return False, f"Missing required columns: {', '.join(missing_columns)}"

    # Check for duplicate columns
    if len(columns) != len(set(col.strip().upper() for col in columns)):
        return False, "CSV contains duplicate column names"

    return True, None


async def parse_csv_file(file: UploadFile) -> Tuple[List[Dict[str, str]], List[str], Dict[str, any]]:
    """
    Parse uploaded CSV file with validation and sanitization.

    Args:
        file: Uploaded CSV file

    Returns:
        Tuple of (rows, column_names, metadata)
        - rows: List of dicts with sanitized cell values
        - column_names: List of column names
        - metadata: Dict with parsing info (row_count, has_confidence, etc.)

    Raises:
        HTTPException: If file is invalid or parsing fails
    """
    # Validate file extension
    if not file.filename.lower().endswith('.csv'):
        raise HTTPException(
            status_code=400,
            detail="Only CSV files are allowed. Please upload a .csv file."
        )

    # Read file content
    file_content = await file.read()
    file_size = len(file_content)

    # Validate file size
    if file_size > MAX_FILE_SIZE_BYTES:
        raise HTTPException(
            status_code=400,
            detail=f"File size exceeds {MAX_FILE_SIZE_MB}MB limit. Please upload a smaller file."
        )

    if file_size == 0:
        raise HTTPException(
            status_code=400,
            detail="File is empty. Please upload a valid CSV file."
        )

    # Detect encoding
    try:
        encoding = detect_encoding(file_content)
        text_content = file_content.decode(encoding)
    except UnicodeDecodeError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Unable to decode file. Please ensure it's a valid CSV with UTF-8 encoding. Error: {str(e)}"
        )

    # Detect delimiter using csv.Sniffer
    try:
        sample = text_content[:4096]  # Use first 4KB for detection
        sniffer = csv.Sniffer()
        delimiter = sniffer.sniff(sample).delimiter
    except csv.Error:
        # Default to comma if detection fails
        delimiter = ','

    # Parse CSV
    try:
        csv_reader = csv.DictReader(io.StringIO(text_content), delimiter=delimiter)

        # Get column names
        column_names = csv_reader.fieldnames
        if not column_names:
            raise HTTPException(
                status_code=400,
                detail="CSV file has no columns. Please upload a valid CSV with headers."
            )

        # Validate structure
        is_valid, error_msg = validate_csv_structure(column_names)
        if not is_valid:
            raise HTTPException(status_code=400, detail=error_msg)

        # Normalize column names
        original_column_names = column_names
        normalized_column_map = {col: col.strip().upper() for col in column_names}

        # Check if CONFIDENCE column exists
        has_confidence = 'CONFIDENCE' in normalized_column_map.values()

        # Parse and sanitize rows
        rows = []
        for row_index, row in enumerate(csv_reader):
            # Skip empty rows
            if not any(row.values()):
                continue

            # Normalize and sanitize row data
            normalized_row = {}
            for original_col, value in row.items():
                normalized_col = normalized_column_map[original_col]
                sanitized_value = sanitize_csv_value(value) if value else ""
                normalized_row[normalized_col] = sanitized_value

            # Add default confidence if missing
            if not has_confidence:
                normalized_row['CONFIDENCE'] = "50.0"

            # Validate confidence value
            try:
                confidence = float(normalized_row.get('CONFIDENCE', '50.0'))
                if not (0 <= confidence <= 100):
                    normalized_row['CONFIDENCE'] = "50.0"  # Default if out of range
                else:
                    normalized_row['CONFIDENCE'] = str(confidence)
            except ValueError:
                normalized_row['CONFIDENCE'] = "50.0"  # Default if invalid

            rows.append(normalized_row)

        if not rows:
            raise HTTPException(
                status_code=400,
                detail="CSV file contains no data rows. Please upload a file with data."
            )

        # Prepare metadata
        metadata = {
            'row_count': len(rows),
            'column_count': len(column_names),
            'has_confidence': has_confidence,
            'encoding': encoding,
            'delimiter': delimiter,
            'file_size_bytes': file_size
        }

        # Get final column names (normalized)
        final_column_names = list(normalized_column_map.values())
        if not has_confidence:
            final_column_names.append('CONFIDENCE')

        return rows, final_column_names, metadata

    except csv.Error as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error parsing CSV file: {str(e)}. Please ensure it's a valid CSV format."
        )
    except Exception as e:
        # Catch any other unexpected errors
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error parsing CSV: {str(e)}"
        )


async def export_to_csv(rows: List[Dict[str, str]], column_names: List[str], filename: str = None) -> str:
    """
    Export project data back to CSV format.

    Args:
        rows: List of row data dicts
        column_names: List of column names
        filename: Optional filename (default: auto-generated)

    Returns:
        Path to created CSV file
    """
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"lemmatization_export_{timestamp}.csv"

    # Create temporary file
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=column_names)
        writer.writeheader()

        for row in rows:
            # Only write columns that exist in column_names
            filtered_row = {col: row.get(col, '') for col in column_names}
            writer.writerow(filtered_row)

        return f.name


def validate_column_name(column_name: str, available_columns: List[str]) -> bool:
    """
    Validate that a column name exists in the available columns.

    Args:
        column_name: Column name to validate
        available_columns: List of valid column names

    Returns:
        True if valid, False otherwise
    """
    return column_name.upper() in [col.upper() for col in available_columns]


def format_file_size(size_bytes: int) -> str:
    """
    Format file size in human-readable format.

    Args:
        size_bytes: File size in bytes

    Returns:
        Formatted string (e.g., "1.5 MB")
    """
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    else:
        return f"{size_bytes / (1024 * 1024):.1f} MB"
