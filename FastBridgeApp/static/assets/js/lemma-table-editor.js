/**
 * Lemmatization Workspace Table Editor
 * Handles CSV data display with confidence-based row highlighting
 * Uses Clusterize.js for virtual scrolling with large datasets
 */

// Global state
let projectId = null;
let userId = null;
let username = null;
let userPermission = null;
let isOwner = false;
let allRows = [];
let filteredRows = [];
let columnNames = [];
let clusterize = null;
let suggestMode = false; // Suggest mode toggle

// Initialize on page load
$(document).ready(function() {
    initializeWorkspace();
    loadProjectData();
    initEventListeners();

    // Load suggestions count for badge (all users can create suggestions)
    loadSuggestionsCount();
});

/**
 * Initialize workspace from hidden inputs
 */
function initializeWorkspace() {
    projectId = $('#project-id').val();
    userId = $('#user-id').val();
    username = $('#username').val();
    userPermission = $('#user-permission').val();
    isOwner = $('#is-owner').val() === 'True';
}

/**
 * Initialize event listeners
 */
function initEventListeners() {
    // Export button
    $('#export-btn').on('click', handleExport);

    // Search functionality
    $('#table-search').on('input', debounce(handleSearch, 300));

    // Clear search button
    $('#clear-search-btn').on('click', clearSearch);

    // Share button (owner only)
    if (isOwner) {
        $('#share-btn').on('click', handleShare);
        $('#permissions-btn').on('click', handlePermissions);
    }

    // Suggest mode toggle
    $('#suggest-mode-toggle').on('click', toggleSuggestMode);

    // View history button
    $('#view-history-btn').on('click', showEditHistory);

    // Comment button
    $('#comments-btn').on('click', toggleCommentsPanel);

    // Suggestions button (only visible to edit/owners)
    $('#view-suggestions-btn').on('click', showSuggestionsModal);
}

/**
 * Load project data from server
 */
async function loadProjectData() {
    try {
        // Show loading
        $('#table-loading').show();

        // Fetch rows
        const response = await fetch(`/lemma-workspace/projects/${projectId}/rows?page_size=10000`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            },
            credentials: 'include'
        });

        if (!response.ok) {
            throw new Error(`Failed to load data: ${response.statusText}`);
        }

        const data = await response.json();
        allRows = data.rows || [];

        if (allRows.length === 0) {
            throw new Error('No data found in project');
        }

        // Extract column names from first row
        if (allRows[0] && allRows[0].data) {
            columnNames = Object.keys(allRows[0].data);
        }

        // Initialize table
        filteredRows = [...allRows];
        renderTable();

        // Update stats
        updateTableStats();

        // Hide loading
        $('#table-loading').hide();

    } catch (error) {
        console.error('Error loading project data:', error);
        $('#table-loading').html(`
            <div style="color:#ff6b6b; padding:40px;">
                <i class="fas fa-exclamation-triangle" style="font-size:3rem; margin-bottom:16px;"></i>
                <p style="font-size:1.1rem; margin-bottom:8px;">Failed to load project data</p>
                <p style="font-size:0.9rem; color:#ccc;">${escapeHtml(error.message)}</p>
                <button onclick="location.reload()" class="toolbar-btn" style="margin-top:16px;">
                    <i class="fas fa-redo"></i> Retry
                </button>
            </div>
        `);
    }
}

/**
 * Render table with Clusterize.js for virtual scrolling
 */
function renderTable() {
    // Render header with action column
    const headerHtml = columnNames.map(col => `<th>${escapeHtml(col)}</th>`).join('');
    const actionHeader = '<th style="width:50px; text-align:center;"><i class="fas fa-comment" title="Comments"></i></th>';
    $('#table-header').html(headerHtml + actionHeader);

    // Prepare rows for Clusterize
    const rowsHtml = filteredRows.map(row => renderTableRow(row));

    // Initialize or update Clusterize
    if (clusterize) {
        clusterize.update(rowsHtml);
    } else {
        clusterize = new Clusterize({
            rows: rowsHtml,
            scrollId: 'scrollArea',
            contentId: 'table-content',
            rows_in_block: 50,
            blocks_in_cluster: 2,
            tag: 'tr'
        });
    }

    // Update info
    $('#table-info').html(`Showing ${filteredRows.length} of ${allRows.length} rows`);

    // Add cell editing handlers if user can edit (either edit permission OR suggest mode is ON)
    const canEdit = userPermission === 'edit' || suggestMode;
    if (canEdit) {
        setTimeout(() => {
            attachCellEditHandlers();
        }, 100);
    }
}

/**
 * Render a single table row with confidence-based highlighting
 */
function renderTableRow(row) {
    const confidence = getRowConfidence(row);
    const bgColor = getConfidenceColor(confidence);
    const rowData = row.data || {};

    // Create cells (editable if user has edit permission OR if Suggest Mode is ON)
    const canEdit = userPermission === 'edit' || suggestMode;
    const cells = columnNames.map(col => {
        const value = rowData[col] || '';
        const editableAttr = canEdit ? 'contenteditable="true"' : '';
        const editableClass = canEdit ? 'editable-cell' : '';
        return `<td class="${editableClass}" data-field="${col}" ${editableAttr}>${escapeHtml(value)}</td>`;
    }).join('');

    // Add action column with comment button (all users can comment - view minimum)
    const actionCell = `
        <td style="text-align:center; width:50px; padding:8px;">
            <button class="row-comment-btn" onclick="addRowComment('${row.row_id}')"
                    title="Add comment to this row"
                    style="background:transparent; border:none; color:#22b3b3; cursor:pointer; font-size:1.1rem; padding:4px 8px; transition:color 0.2s;">
                <i class="fas fa-comment"></i>
            </button>
        </td>
    `;

    return `<tr data-row-id="${row.row_id}" data-confidence="${confidence}" style="background:${bgColor};">${cells}${actionCell}</tr>`;
}

/**
 * Calculate confidence-based background color
 * 0-50%: Red to Yellow gradient
 * 50-100%: Yellow to Green gradient
 */
function getConfidenceColor(confidence) {
    // Normalize to 0-1
    const normalized = Math.max(0, Math.min(100, confidence)) / 100;

    let r, g, b;

    if (normalized < 0.5) {
        // Red to Yellow: (255,0,0) → (255,255,0)
        const t = normalized * 2;
        r = 255;
        g = Math.floor(255 * t);
        b = 0;
    } else {
        // Yellow to Green: (255,255,0) → (0,255,0)
        const t = (normalized - 0.5) * 2;
        r = Math.floor(255 * (1 - t));
        g = 255;
        b = 0;
    }

    // Return with alpha for readability
    return `rgba(${r}, ${g}, ${b}, 0.15)`;
}

/**
 * Handle table search
 */
function handleSearch() {
    const query = $('#table-search').val().trim().toLowerCase();

    if (!query) {
        filteredRows = [...allRows];
        $('#clear-search-btn').hide();
    } else {
        // Filter rows by searching all column values
        filteredRows = allRows.filter(row => {
            const rowData = row.data || {};
            return Object.values(rowData).some(value =>
                String(value).toLowerCase().includes(query)
            );
        });
        $('#clear-search-btn').show();
    }

    renderTable();
    updateTableStats();
}

/**
 * Clear search
 */
function clearSearch() {
    $('#table-search').val('');
    filteredRows = [...allRows];
    $('#clear-search-btn').hide();
    renderTable();
    updateTableStats();
}

/**
 * Get confidence value safely (handles 0 vs undefined/null)
 */
function getRowConfidence(row) {
    return (row.confidence !== undefined && row.confidence !== null) ? row.confidence : 50.0;
}

/**
 * Update table statistics
 */
function updateTableStats() {
    if (filteredRows.length === 0) {
        $('#table-stats').html('No matching rows');
        return;
    }

    // Calculate average confidence
    const totalConfidence = filteredRows.reduce((sum, row) => sum + getRowConfidence(row), 0);
    const avgConfidence = (totalConfidence / filteredRows.length).toFixed(1);

    // Count by confidence range
    const lowCount = filteredRows.filter(row => getRowConfidence(row) < 40).length;
    const medCount = filteredRows.filter(row => {
        const conf = getRowConfidence(row);
        return conf >= 40 && conf < 70;
    }).length;
    const highCount = filteredRows.filter(row => getRowConfidence(row) >= 70).length;

    $('#table-stats').html(`
        Avg Confidence: ${avgConfidence}% |
        <span style="color:#ff6b6b;">Low: ${lowCount}</span> |
        <span style="color:#ffd93d;">Med: ${medCount}</span> |
        <span style="color:#6bcf7f;">High: ${highCount}</span>
    `);
}

/**
 * Handle export to CSV
 */
async function handleExport() {
    try {
        const btn = $('#export-btn');
        btn.prop('disabled', true).html('<i class="fas fa-spinner fa-spin"></i> Exporting...');

        window.location.href = `/lemma-workspace/projects/${projectId}/export`;

        // Re-enable button after a moment
        setTimeout(() => {
            btn.prop('disabled', false).html('<i class="fas fa-download"></i> Export');
        }, 2000);

    } catch (error) {
        console.error('Error exporting:', error);
        alert('Failed to export CSV. Please try again.');
        $('#export-btn').prop('disabled', false).html('<i class="fas fa-download"></i> Export');
    }
}

/**
 * Attach cell edit handlers using event delegation
 */
function attachCellEditHandlers() {
    // Use event delegation on the table container instead of individual cells
    // This ensures handlers work even when cells are re-rendered
    const tableContent = document.getElementById('table-content');

    if (!tableContent) {
        console.error('Table content element not found');
        return;
    }

    // Remove old listeners if they exist (prevent duplicates)
    if (tableContent.hasEditHandlers) {
        return;
    }
    tableContent.hasEditHandlers = true;

    // Focus event - store original value
    tableContent.addEventListener('focus', function(e) {
        if (e.target.classList.contains('editable-cell') && e.target.contentEditable === 'true') {
            e.target.dataset.originalValue = e.target.textContent;
        }
    }, true); // Use capture phase

    // Blur event - save if changed
    tableContent.addEventListener('blur', function(e) {
        if (e.target.classList.contains('editable-cell') && e.target.contentEditable === 'true') {
            const newValue = e.target.textContent.trim();
            const originalValue = e.target.dataset.originalValue || '';

            if (newValue !== originalValue) {
                const rowElement = e.target.closest('tr');
                if (!rowElement) {
                    console.error('Could not find parent row');
                    return;
                }
                const rowId = rowElement.dataset.rowId;
                const fieldName = e.target.dataset.field;

                saveCellEdit(rowId, fieldName, newValue, e.target);
            }
        }
    }, true); // Use capture phase

    // Keydown event - Enter to save, Escape to cancel
    tableContent.addEventListener('keydown', function(e) {
        if (e.target.classList.contains('editable-cell') && e.target.contentEditable === 'true') {
            if (e.key === 'Enter') {
                e.preventDefault();
                e.target.blur(); // Trigger save
            } else if (e.key === 'Escape') {
                e.preventDefault();
                e.target.textContent = e.target.dataset.originalValue || '';
                e.target.blur();
            }
        }
    }, true); // Use capture phase

}

/**
 * Save cell edit to server
 * If suggest mode is enabled, creates a suggestion instead of direct edit
 */
async function saveCellEdit(rowId, fieldName, newValue, cellElement) {
    try {
        // Show saving indicator
        cellElement.style.backgroundColor = '#4dabf7';

        let response, result;

        // view users MUST create suggestions (they can't do direct edits)
        // edit users can choose: if suggest mode is ON, create suggestion; otherwise, direct edit
        const mustUseSuggestions = userPermission !== 'edit' || suggestMode;

        if (mustUseSuggestions) {
            // Create suggestion instead of direct edit
            // Suggestions are ALWAYS pending, even for owners
            response = await fetch(`/lemma-workspace/projects/${projectId}/suggestions`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                credentials: 'include',
                body: JSON.stringify({
                    row_id: rowId,
                    changes: {
                        [fieldName]: newValue
                    },
                    comment: `Suggested change to ${fieldName}`
                })
            });

            if (!response.ok) {
                let errorMessage = 'Failed to create suggestion';
                try {
                    const error = await response.json();
                    errorMessage = error.detail || JSON.stringify(error) || errorMessage;
                } catch (e) {
                    errorMessage = `Server error (${response.status}): ${response.statusText}`;
                }
                console.error('Suggestion creation failed:', {
                    status: response.status,
                    message: errorMessage,
                    userPermission: userPermission,
                    suggestMode: suggestMode
                });
                throw new Error(errorMessage);
            }

            result = await response.json();

            // Suggestion is pending - revert display to original value
            cellElement.style.backgroundColor = '#ffd43b';

            // Show message with suggestion ID
            alert(`Suggestion created and pending review.\n\nView pending suggestions in the Suggestions panel to approve or reject.`);

            // Revert display to original value after brief delay
            setTimeout(() => {
                cellElement.textContent = cellElement.dataset.originalValue || '';
                cellElement.style.backgroundColor = ''; // Clear to inherit row background
            }, 1500);

            // Refresh suggestions count badge (all users can create suggestions)
            loadSuggestionsCount();

        } else {
            // Direct edit (original behavior)
            response = await fetch(`/lemma-workspace/projects/${projectId}/rows/${rowId}`, {
                method: 'PATCH',
                headers: {
                    'Content-Type': 'application/json'
                },
                credentials: 'include',
                body: JSON.stringify({
                    field: fieldName,
                    new_value: newValue
                })
            });

            if (!response.ok) {
                let errorMessage = 'Failed to save edit';
                try {
                    const error = await response.json();
                    errorMessage = error.detail || JSON.stringify(error) || errorMessage;
                } catch (e) {
                    errorMessage = `Server error: ${response.statusText}`;
                }
                throw new Error(errorMessage);
            }

            result = await response.json();

            // Use the server's new_value in case it was clamped/modified
            const actualNewValue = result.new_value || newValue;

            // Update local data
            const rowIndex = allRows.findIndex(r => r.row_id === rowId);
            if (rowIndex !== -1) {
                allRows[rowIndex].data[fieldName] = actualNewValue;
                allRows[rowIndex].last_modified = result.last_modified;
                allRows[rowIndex].last_modified_by = result.last_modified_by;

                // ONLY update row background if CONFIDENCE field was actually changed
                if (result.confidence !== undefined) {
                    allRows[rowIndex].confidence = result.confidence;

                    // Update the cell display with the clamped value
                    cellElement.textContent = actualNewValue;

                    // Update the row's background color
                    const rowElement = cellElement.closest('tr');
                    if (rowElement) {
                        const newBgColor = getConfidenceColor(result.confidence);
                        rowElement.style.background = newBgColor;
                        rowElement.dataset.confidence = result.confidence;
                    }
                }
            }

            // Show success indicator - clear after 1s so cell inherits row background
            cellElement.style.backgroundColor = '#51cf66';
            setTimeout(() => {
                cellElement.style.backgroundColor = ''; // Clear to inherit row background
            }, 1000);
        }

    } catch (error) {
        console.error('Error saving cell edit:', error);

        // Revert to original value
        cellElement.textContent = cellElement.dataset.originalValue || '';

        // Show error indicator - clear to inherit row background
        cellElement.style.backgroundColor = '#ff6b6b';
        setTimeout(() => {
            cellElement.style.backgroundColor = ''; // Clear to inherit row background
        }, 2000);

        alert(`Failed to save: ${error.message}`);
    }
}

/**
 * Handle share project
 */
function handleShare() {
    $('#shareModal').modal('show');
}

/**
 * Submit share form
 */
async function submitShare() {
    const email = $('#share-email').val().trim();
    const permission = $('#share-permission').val();

    if (!email) {
        alert('Please enter an email address.');
        return;
    }

    try {
        const btn = $('#share-submit-btn');
        btn.prop('disabled', true).html('<i class="fas fa-spinner fa-spin"></i> Sharing...');

        const response = await fetch(`/lemma-workspace/projects/${projectId}/permissions/grant`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            credentials: 'include',
            body: JSON.stringify({
                recipient_email: email,
                permission: permission
            })
        });

        if (!response.ok) {
            let errorMessage = 'Failed to share project';
            try {
                const error = await response.json();
                errorMessage = error.detail || errorMessage;
            } catch (parseError) {
                // Server returned HTML error page instead of JSON
                if (response.status === 404) {
                    errorMessage = `User with email "${email}" does not exist in the system. Please check the email address and try again.`;
                } else if (response.status === 500) {
                    errorMessage = 'Server error occurred. Please try again later.';
                } else {
                    errorMessage = `Server error: ${response.statusText || 'Unknown error'}`;
                }
            }
            throw new Error(errorMessage);
        }

        let result;
        try {
            result = await response.json();
        } catch (parseError) {
            // Response was OK but body is not valid JSON (possibly HTML error page)
            throw new Error(`User with email "${email}" does not exist in the system. Please check the email address and try again.`);
        }

        // Close modal and reset form
        $('#shareModal').modal('hide');
        $('#share-email').val('');
        $('#share-permission').val('view');

        const recipientName = result.recipient_name || email;
        alert(`Project shared successfully with ${recipientName} (${email})`);

    } catch (error) {
        console.error('Error sharing project:', error);
        alert(`Failed to share: ${error.message}`);
    } finally {
        $('#share-submit-btn').prop('disabled', false).html('Share');
    }
}

/**
 * Handle permissions management
 */
async function handlePermissions() {
    $('#permissionsModal').modal('show');
    await loadPermissions();
}

/**
 * Load current permissions
 */
async function loadPermissions() {
    try {
        $('#permissions-loading').show();
        $('#permissions-list').hide();

        const response = await fetch(`/lemma-workspace/projects/${projectId}/permissions/list`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            },
            credentials: 'include'
        });

        if (!response.ok) {
            throw new Error('Failed to load permissions');
        }

        const data = await response.json();
        const permissions = data.permissions || [];

        if (permissions.length === 0) {
            $('#permissions-list').html(`
                <div style="text-align:center; padding:40px; color:#888;">
                    <i class="fas fa-users" style="font-size:3rem; margin-bottom:16px;"></i>
                    <p>No collaborators yet. Use the Share button to invite others.</p>
                </div>
            `);
        } else {
            const permissionsHtml = permissions.map(p => `
                <div class="permission-item" style="display:flex; align-items:center; padding:12px; border-bottom:1px solid #444;">
                    <div style="flex:1;">
                        <div style="font-weight:500;">${escapeHtml(p.user_email || 'Unknown User')}</div>
                        <div style="font-size:0.85rem; color:#888;">Added ${new Date(p.granted_at).toLocaleDateString()}</div>
                    </div>
                    <div style="margin-left:16px;">
                        <select class="permission-select" data-user-id="${p.user_id}"
                                style="padding:6px 12px; background:#2a2a2a; color:#fff; border:1px solid #444; border-radius:4px;">
                            <option value="view" ${p.permission_level === 'view' ? 'selected' : ''}>View</option>
                            <option value="edit" ${p.permission_level === 'edit' ? 'selected' : ''}>Edit</option>
                        </select>
                    </div>
                    <button class="btn btn-sm btn-danger" onclick="revokePermission('${p.user_id}')"
                            style="margin-left:8px;">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            `).join('');

            $('#permissions-list').html(permissionsHtml);

            // Attach change handlers
            $('.permission-select').on('change', function() {
                const userId = $(this).data('user-id');
                const newPermission = $(this).val();
                modifyPermission(userId, newPermission);
            });
        }

        $('#permissions-loading').hide();
        $('#permissions-list').show();

    } catch (error) {
        console.error('Error loading permissions:', error);
        $('#permissions-loading').html(`
            <div style="color:#ff6b6b; padding:20px; text-align:center;">
                <i class="fas fa-exclamation-triangle"></i> Failed to load permissions
            </div>
        `);
    }
}

/**
 * Modify user permission
 */
async function modifyPermission(userId, newPermissionLevel) {
    try {
        const response = await fetch(`/lemma-workspace/projects/${projectId}/permissions/modify`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json'
            },
            credentials: 'include',
            body: JSON.stringify({
                recipient_id: userId,
                new_permission: newPermissionLevel
            })
        });

        if (!response.ok) {
            let errorMessage = 'Failed to modify permission';
            try {
                const error = await response.json();
                // Handle different error formats
                if (typeof error.detail === 'string') {
                    errorMessage = error.detail;
                } else if (Array.isArray(error.detail)) {
                    // Pydantic validation errors
                    errorMessage = error.detail.map(e => e.msg).join(', ');
                } else {
                    errorMessage = JSON.stringify(error.detail || error);
                }
            } catch (parseError) {
                errorMessage = `Server error: ${response.statusText}`;
            }
            throw new Error(errorMessage);
        }

        // Show success briefly
        const selectElement = $(`.permission-select[data-user-id="${userId}"]`);
        const originalBg = selectElement.css('background-color');
        selectElement.css('background-color', '#51cf66');
        setTimeout(() => {
            selectElement.css('background-color', originalBg);
        }, 1000);

    } catch (error) {
        console.error('Error modifying permission:', error);
        alert(`Failed to modify permission: ${error.message}`);
        // Reload permissions to reset UI
        await loadPermissions();
    }
}

/**
 * Revoke user permission
 */
async function revokePermission(userId) {
    if (!confirm('Are you sure you want to revoke access for this user?')) {
        return;
    }

    try {
        const response = await fetch(`/lemma-workspace/projects/${projectId}/permissions/revoke`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            },
            credentials: 'include',
            body: JSON.stringify({
                recipient_id: userId
            })
        });

        if (!response.ok) {
            let errorMessage = 'Failed to revoke permission';
            try {
                const error = await response.json();
                // Handle different error formats
                if (typeof error.detail === 'string') {
                    errorMessage = error.detail;
                } else if (Array.isArray(error.detail)) {
                    // Pydantic validation errors
                    errorMessage = error.detail.map(e => e.msg).join(', ');
                } else {
                    errorMessage = JSON.stringify(error.detail || error);
                }
            } catch (parseError) {
                errorMessage = `Server error: ${response.statusText}`;
            }
            throw new Error(errorMessage);
        }

        // Reload permissions list
        await loadPermissions();

    } catch (error) {
        console.error('Error revoking permission:', error);
        alert(`Failed to revoke permission: ${error.message}`);
    }
}

/**
 * Debounce function for search
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

/**
 * Escape HTML to prevent XSS
 */
function escapeHtml(text) {
    if (text === null || text === undefined) {
        return '';
    }
    const div = document.createElement('div');
    div.textContent = String(text);
    return div.innerHTML;
}

/**
 * Format file size
 */
function formatFileSize(bytes) {
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}

// ============================================================================
// Phase 4: Comments, Suggestions, and Edit History
// ============================================================================

/**
 * Toggle suggest mode on/off
 */
function toggleSuggestMode() {
    suggestMode = !suggestMode;
    const btn = $('#suggest-mode-toggle');

    if (suggestMode) {
        btn.addClass('active')
           .html('<i class="fas fa-pencil-alt"></i> Suggest Mode: ON')
           .css('background-color', '#ffd43b');
    } else {
        btn.removeClass('active')
           .html('<i class="fas fa-pencil-alt"></i> Suggest Mode: OFF')
           .css('background-color', '');
    }

    // Re-render table so cells become editable/non-editable based on suggest mode
    renderTable();
}

/**
 * Toggle comments panel visibility
 */
function toggleCommentsPanel() {
    const panel = $('#comments-panel');
    const isVisible = panel.is(':visible');

    if (isVisible) {
        panel.slideUp(300);
        $('#comments-btn').removeClass('active');
    } else {
        panel.slideDown(300);
        $('#comments-btn').addClass('active');
        loadAllComments();
    }
}

/**
 * Load all comments for the project (efficient - single API call)
 */
async function loadAllComments() {
    try {
        $('#comments-content').html('<div class="spinner-ring"></div><p>Loading comments...</p>');

        // Fetch all comments for project in one call (much more efficient!)
        const response = await fetch(
            `/lemma-workspace/projects/${projectId}/comments`,
            {
                method: 'GET',
                headers: { 'Content-Type': 'application/json' },
                credentials: 'include'
            }
        );

        if (!response.ok) {
            throw new Error('Failed to load comments');
        }

        const data = await response.json();
        const allComments = data.comments || [];

        // Add row info to each comment
        allComments.forEach(comment => {
            const row = allRows.find(r => r.row_id === comment.row_id);
            comment.row_data = row ? row.data : {};
        });

        // Render comments (already sorted by backend - most recent first)
        if (allComments.length === 0) {
            $('#comments-content').html('<p style="color:#888; text-align:center; padding:20px;">No comments yet</p>');
        } else {
            const html = allComments.map(comment => renderCommentCard(comment)).join('');
            $('#comments-content').html(html);
        }

    } catch (error) {
        console.error('Error loading comments:', error);
        $('#comments-content').html('<p style="color:#ff6b6b;">Failed to load comments</p>');
    }
}

/**
 * Render a single comment card
 */
function renderCommentCard(comment) {
    const createdAt = new Date(comment.created_at).toLocaleString();
    const canDelete = comment.user_id === userId || isOwner;

    // Build row context with TITLE, LOCATION, and SECTION
    const title = comment.row_data.TITLE || 'Unknown';
    const location = comment.row_data.LOCATION || '';
    const section = comment.row_data.SECTION || '';

    const rowPreview = `${title}${location ? ` [${location}` : ''}${section ? `, ${section}]` : (location ? ']' : '')}`;

    return `
        <div class="comment-card" data-comment-id="${comment.comment_id}">
            <div class="comment-header">
                <strong>${escapeHtml(comment.username)}</strong>
                <span class="comment-time">${createdAt}</span>
            </div>
            <div class="comment-row-preview">
                <i class="fas fa-link"></i> ${escapeHtml(rowPreview.substring(0, 80))}${rowPreview.length > 80 ? '...' : ''}
            </div>
            <div class="comment-text">${escapeHtml(comment.comment_text)}</div>
            ${canDelete ? `
                <button class="btn-delete-comment" onclick="deleteComment('${comment.comment_id}')">
                    <i class="fas fa-trash"></i> Delete
                </button>
            ` : ''}
        </div>
    `;
}

/**
 * Add comment to a row
 */
async function addRowComment(rowId) {
    const commentText = prompt('Enter your comment:');
    if (!commentText || !commentText.trim()) return;

    try {
        const response = await fetch(
            `/lemma-workspace/projects/${projectId}/rows/${rowId}/comments`,
            {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                credentials: 'include',
                body: JSON.stringify({
                    row_id: rowId,
                    comment_text: commentText.trim()
                })
            }
        );

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to add comment');
        }

        alert('Comment added successfully!');

        // Reload comments if panel is open
        if ($('#comments-panel').is(':visible')) {
            loadAllComments();
        }

    } catch (error) {
        console.error('Error adding comment:', error);
        alert(`Failed to add comment: ${error.message}`);
    }
}

/**
 * Delete a comment
 */
async function deleteComment(commentId) {
    if (!confirm('Are you sure you want to delete this comment?')) return;

    try {
        const response = await fetch(
            `/lemma-workspace/projects/${projectId}/comments/${commentId}`,
            {
                method: 'DELETE',
                headers: { 'Content-Type': 'application/json' },
                credentials: 'include'
            }
        );

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to delete comment');
        }

        // Remove from UI
        $(`.comment-card[data-comment-id="${commentId}"]`).fadeOut(300, function() {
            $(this).remove();
        });

    } catch (error) {
        console.error('Error deleting comment:', error);
        alert(`Failed to delete comment: ${error.message}`);
    }
}

/**
 * Show edit history modal
 */
async function showEditHistory() {
    try {
        $('#historyModal').modal('show');
        $('#history-loading').show();
        $('#history-list').hide();

        const response = await fetch(
            `/lemma-workspace/projects/${projectId}/history?limit=100`,
            {
                method: 'GET',
                headers: { 'Content-Type': 'application/json' },
                credentials: 'include'
            }
        );

        if (!response.ok) {
            throw new Error('Failed to load history');
        }

        const data = await response.json();
        const history = data.history || [];

        // Render history
        if (history.length === 0) {
            $('#history-list').html('<p style="color:#888; text-align:center; padding:20px;">No history yet</p>');
        } else {
            const html = history.map(entry => renderHistoryEntry(entry)).join('');
            $('#history-list').html(html);
        }

        $('#history-loading').hide();
        $('#history-list').show();

    } catch (error) {
        console.error('Error loading history:', error);
        $('#history-loading').html('<p style="color:#ff6b6b;">Failed to load history</p>');
    }
}

/**
 * Render a single history entry
 */
function renderHistoryEntry(entry) {
    const timestamp = new Date(entry.timestamp).toLocaleString();
    const actionIcons = {
        'edit': 'fa-edit',
        'comment': 'fa-comment',
        'suggest': 'fa-lightbulb',
        'accept_suggestion': 'fa-check',
        'reject_suggestion': 'fa-times',
        'grant_permission': 'fa-user-plus',
        'revoke_permission': 'fa-user-minus'
    };
    const icon = actionIcons[entry.action] || 'fa-info-circle';

    let changesSummary = '';
    if (entry.changes) {
        if (entry.action === 'edit' || entry.action === 'accept_suggestion') {
            const changes = Object.entries(entry.changes)
                .map(([field, change]) => {
                    if (change.from && change.to) {
                        return `${field}: "${change.from}" → "${change.to}"`;
                    }
                    return field;
                })
                .join(', ');
            changesSummary = changes;
        } else if (entry.action === 'comment') {
            changesSummary = entry.changes.comment_text || '';
        } else if (entry.action === 'grant_permission' || entry.action === 'revoke_permission') {
            changesSummary = `${entry.changes.recipient_email || 'User'}: ${entry.changes.permission || ''}`;
        }
    }

    return `
        <div class="history-entry">
            <div class="history-icon">
                <i class="fas ${icon}"></i>
            </div>
            <div class="history-details">
                <div class="history-header">
                    <strong>${escapeHtml(entry.username)}</strong>
                    <span class="history-action">${entry.action.replace('_', ' ')}</span>
                </div>
                <div class="history-time">${timestamp}</div>
                ${changesSummary ? `<div class="history-changes">${escapeHtml(changesSummary)}</div>` : ''}
            </div>
        </div>
    `;
}

/**
 * Show suggestions modal
 */
async function showSuggestionsModal() {
    try {
        $('#suggestionsModal').modal('show');
        $('#suggestions-loading').show();
        $('#suggestions-list').hide();

        await loadSuggestions();

    } catch (error) {
        console.error('Error showing suggestions:', error);
        $('#suggestions-loading').html('<p style="color:#ff6b6b;">Failed to load suggestions</p>');
    }
}

/**
 * Load pending suggestions for the project
 */
async function loadSuggestions() {
    try {
        const response = await fetch(
            `/lemma-workspace/projects/${projectId}/suggestions?status=pending`,
            {
                method: 'GET',
                headers: { 'Content-Type': 'application/json' },
                credentials: 'include'
            }
        );

        if (!response.ok) {
            throw new Error('Failed to load suggestions');
        }

        const data = await response.json();
        const suggestions = data.suggestions || [];

        // Update badge count
        updateSuggestionsBadge(suggestions.length);

        // Render suggestions
        if (suggestions.length === 0) {
            $('#suggestions-list').html(`
                <div style="text-align:center; padding:40px; color:#888;">
                    <i class="fas fa-lightbulb" style="font-size:3rem; margin-bottom:16px; opacity:0.3;"></i>
                    <p>No pending suggestions</p>
                </div>
            `);
        } else {
            const html = suggestions.map(suggestion => renderSuggestionCard(suggestion)).join('');
            $('#suggestions-list').html(html);
        }

        $('#suggestions-loading').hide();
        $('#suggestions-list').show();

    } catch (error) {
        console.error('Error loading suggestions:', error);
        $('#suggestions-loading').html('<p style="color:#ff6b6b;">Failed to load suggestions</p>');
    }
}

/**
 * Render a single suggestion card
 */
function renderSuggestionCard(suggestion) {
    const createdAt = new Date(suggestion.created_at).toLocaleString();

    // Get row context with TITLE, LOCATION, and SECTION
    const row = allRows.find(r => r.row_id === suggestion.row_id);
    let rowContext = 'Unknown row';
    if (row) {
        const title = row.data.TITLE || 'Unknown';
        const location = row.data.LOCATION || '';
        const section = row.data.SECTION || '';
        rowContext = `${title}${location ? ` [${location}` : ''}${section ? `, ${section}]` : (location ? ']' : '')}`;
    }

    // Build changes display
    const changesHtml = Object.entries(suggestion.changes).map(([field, change]) => {
        return `
            <div class="suggestion-change-item">
                <div class="suggestion-field-name">${escapeHtml(field)}</div>
                <div>
                    <span class="suggestion-value-from">${escapeHtml(change.from || '(empty)')}</span>
                    <i class="fas fa-arrow-right" style="color:#ffd43b; margin:0 8px;"></i>
                    <span class="suggestion-value-to">${escapeHtml(change.to || '(empty)')}</span>
                </div>
            </div>
        `;
    }).join('');

    return `
        <div class="suggestion-card" data-suggestion-id="${suggestion.suggestion_id}">
            <div class="suggestion-header">
                <div>
                    <span class="suggestion-author">
                        <i class="fas fa-user"></i> ${escapeHtml(suggestion.suggested_by_name)}
                    </span>
                </div>
                <span class="suggestion-time">${createdAt}</span>
            </div>

            <div class="suggestion-row-context">
                <i class="fas fa-link"></i> ${escapeHtml(rowContext.substring(0, 100))}${rowContext.length > 100 ? '...' : ''}
            </div>

            <div class="suggestion-changes">
                ${changesHtml}
            </div>

            ${suggestion.comment ? `
                <div class="suggestion-comment">
                    <i class="fas fa-quote-left"></i> ${escapeHtml(suggestion.comment)}
                </div>
            ` : ''}

            ${(userPermission === 'edit' || isOwner) ? `
                <div class="suggestion-actions">
                    <button class="btn-reject-suggestion" onclick="rejectSuggestion('${suggestion.suggestion_id}')">
                        <i class="fas fa-times"></i> Reject
                    </button>
                    <button class="btn-approve-suggestion" onclick="approveSuggestion('${suggestion.suggestion_id}')">
                        <i class="fas fa-check"></i> Approve
                    </button>
                </div>
            ` : `
                <div style="text-align:center; padding:8px; color:#888; font-size:0.85rem; font-style:italic;">
                    <i class="fas fa-clock"></i> Pending review by project owner
                </div>
            `}
        </div>
    `;
}

/**
 * Approve a suggestion
 */
async function approveSuggestion(suggestionId) {
    try {
        // Disable buttons
        const card = $(`.suggestion-card[data-suggestion-id="${suggestionId}"]`);
        card.find('button').prop('disabled', true);

        const response = await fetch(
            `/lemma-workspace/projects/${projectId}/suggestions/${suggestionId}/accept`,
            {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                credentials: 'include'
            }
        );

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to approve suggestion');
        }

        const result = await response.json();

        // Update local data with the applied changes
        const rowId = result.row_id;
        const rowIndex = allRows.findIndex(r => r.row_id === rowId);
        if (rowIndex !== -1 && result.applied_data) {
            allRows[rowIndex].data = result.applied_data;
            allRows[rowIndex].last_modified = result.last_modified;
            allRows[rowIndex].last_modified_by = result.last_modified_by;

            // If confidence was updated, update it too
            if (result.confidence !== undefined) {
                allRows[rowIndex].confidence = result.confidence;
            }
        }

        // Remove card from UI with animation
        card.css('background', 'rgba(81, 207, 102, 0.2)');
        setTimeout(() => {
            card.fadeOut(300, function() {
                $(this).remove();

                // Check if there are any suggestions left
                const remainingCount = $('#suggestions-list .suggestion-card').length;
                updateSuggestionsBadge(remainingCount);

                if (remainingCount === 0) {
                    $('#suggestions-list').html(`
                        <div style="text-align:center; padding:40px; color:#888;">
                            <i class="fas fa-lightbulb" style="font-size:3rem; margin-bottom:16px; opacity:0.3;"></i>
                            <p>No pending suggestions</p>
                        </div>
                    `);
                }
            });
        }, 500);

        // Refresh table to show updated data
        renderTable();

    } catch (error) {
        console.error('Error approving suggestion:', error);
        alert(`Failed to approve suggestion: ${error.message}`);

        // Re-enable buttons
        const card = $(`.suggestion-card[data-suggestion-id="${suggestionId}"]`);
        card.find('button').prop('disabled', false);
    }
}

/**
 * Reject a suggestion
 */
async function rejectSuggestion(suggestionId) {
    if (!confirm('Are you sure you want to reject this suggestion?')) {
        return;
    }

    try {
        // Disable buttons
        const card = $(`.suggestion-card[data-suggestion-id="${suggestionId}"]`);
        card.find('button').prop('disabled', true);

        const response = await fetch(
            `/lemma-workspace/projects/${projectId}/suggestions/${suggestionId}/reject`,
            {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                credentials: 'include'
            }
        );

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to reject suggestion');
        }

        // Remove card from UI with animation
        card.css('background', 'rgba(255, 107, 107, 0.2)');
        setTimeout(() => {
            card.fadeOut(300, function() {
                $(this).remove();

                // Check if there are any suggestions left
                const remainingCount = $('#suggestions-list .suggestion-card').length;
                updateSuggestionsBadge(remainingCount);

                if (remainingCount === 0) {
                    $('#suggestions-list').html(`
                        <div style="text-align:center; padding:40px; color:#888;">
                            <i class="fas fa-lightbulb" style="font-size:3rem; margin-bottom:16px; opacity:0.3;"></i>
                            <p>No pending suggestions</p>
                        </div>
                    `);
                }
            });
        }, 500);

    } catch (error) {
        console.error('Error rejecting suggestion:', error);
        alert(`Failed to reject suggestion: ${error.message}`);

        // Re-enable buttons
        const card = $(`.suggestion-card[data-suggestion-id="${suggestionId}"]`);
        card.find('button').prop('disabled', false);
    }
}

/**
 * Update suggestions count badge
 */
function updateSuggestionsBadge(count) {
    const badge = $('#suggestions-count-badge');
    if (count > 0) {
        badge.text(count).show();
    } else {
        badge.hide();
    }
}

/**
 * Load suggestions count on page load (lightweight check)
 */
async function loadSuggestionsCount() {
    try {
        const response = await fetch(
            `/lemma-workspace/projects/${projectId}/suggestions?status=pending`,
            {
                method: 'GET',
                headers: { 'Content-Type': 'application/json' },
                credentials: 'include'
            }
        );

        if (response.ok) {
            const data = await response.json();
            const count = (data.suggestions || []).length;
            updateSuggestionsBadge(count);
        }
    } catch (error) {
        console.error('Error loading suggestions count:', error);
        // Fail silently - badge just won't show
    }
}
