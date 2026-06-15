/**
 * Lemmatization Workspace Dashboard
 * Handles project list display and creation
 */

// Global state
let ownedProjects = [];
let sharedProjects = [];

// Initialize on page load
$(document).ready(function() {
    loadProjects();
    initEventListeners();
});

/**
 * Initialize event listeners
 */
function initEventListeners() {
    // Create project button
    $('#create-project-btn').on('click', showCreateProjectModal);

    // Submit project form
    $('#submit-project-btn').on('click', handleCreateProject);

    // File input change
    $('#csv-file').on('change', function() {
        const fileName = $(this).val().split('\\').pop();
        $(this).siblings('.custom-file-label').html(fileName || 'Choose CSV file...');
    });

    // Form validation on Enter key
    $('#project-name, #project-description').on('keypress', function(e) {
        if (e.which === 13 && e.target.id === 'project-name') {
            e.preventDefault();
            $('#project-description').focus();
        }
    });
}

/**
 * Load all projects (owned and shared)
 */
async function loadProjects() {
    showLoading(true);

    try {
        const response = await fetch('/lemma-workspace/projects/list', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            },
            credentials: 'include'
        });

        if (!response.ok) {
            // Check if it's an authentication error
            if (response.status === 401) {
                window.location.href = '/account/signin';
                return;
            }
            throw new Error(`Failed to load projects: ${response.statusText}`);
        }

        const data = await response.json();

        // Ensure data has the expected structure
        if (!data || typeof data !== 'object') {
            throw new Error('Invalid response format from server');
        }

        ownedProjects = data.owned_projects || [];
        sharedProjects = data.shared_projects || [];

        renderProjects();
    } catch (error) {
        console.error('Error loading projects:', error);

        // Show error in a user-friendly way
        $('#loading-state').hide();
        $('#owned-projects-section, #shared-projects-section').show();
        $('#owned-projects-container').html(`
            <div style="grid-column: 1/-1; text-align:center; padding:40px; color:#ff6b6b;">
                <i class="fas fa-exclamation-triangle" style="font-size:3rem; margin-bottom:16px;"></i>
                <p style="font-size:1.1rem; margin-bottom:8px;">Failed to load projects</p>
                <p style="font-size:0.9rem; color:#ccc;">${escapeHtml(error.message)}</p>
                <button onclick="location.reload()" class="btn" style="margin-top:16px; background:#22b3b3; color:#fff; padding:10px 20px; border:none; border-radius:6px; cursor:pointer;">
                    <i class="fas fa-redo"></i> Try Again
                </button>
            </div>
        `);
        $('#shared-projects-container').empty();
    } finally {
        showLoading(false);
    }
}

/**
 * Render project cards
 */
function renderProjects() {
    // Render owned projects
    const ownedContainer = $('#owned-projects-container');
    const noOwnedProjects = $('#no-owned-projects');

    if (ownedProjects.length === 0) {
        ownedContainer.empty();
        noOwnedProjects.show();
    } else {
        noOwnedProjects.hide();
        ownedContainer.html(ownedProjects.map(project => renderProjectCard(project)).join(''));
    }

    // Render shared projects
    const sharedContainer = $('#shared-projects-container');
    const noSharedProjects = $('#no-shared-projects');

    if (sharedProjects.length === 0) {
        sharedContainer.empty();
        noSharedProjects.show();
    } else {
        noSharedProjects.hide();
        sharedContainer.html(sharedProjects.map(project => renderProjectCard(project)).join(''));
    }

    // Add click handlers to project cards
    $('.project-card').on('click', function() {
        const projectId = $(this).data('project-id');
        window.location.href = `/lemma-workspace/projects/${projectId}`;
    });
}

/**
 * Render a single project card
 */
function renderProjectCard(project) {
    const lastModified = project.last_modified
        ? formatRelativeTime(new Date(project.last_modified))
        : 'Never';

    const badge = project.is_owner
        ? '<span class="project-card-badge">Owner</span>'
        : `<span class="project-card-badge" style="background:#555;">${project.permission.replace('CAN_', '')}</span>`;

    const description = project.description
        ? `<div class="project-card-description">${escapeHtml(project.description)}</div>`
        : '';

    const ownerInfo = !project.is_owner && project.owner_name
        ? `<div class="project-card-meta-item">
             <i class="fas fa-user" style="color:#777;"></i>
             <span>${escapeHtml(project.owner_name)}</span>
           </div>`
        : '';

    return `
        <div class="project-card" data-project-id="${project.project_id}">
            <div class="project-card-header">
                <h4 class="project-card-title">${escapeHtml(project.project_name)}</h4>
                ${badge}
            </div>
            ${description}
            <div class="project-card-meta">
                <div class="project-card-meta-item">
                    <i class="fas fa-table" style="color:#22b3b3;"></i>
                    <span>${project.row_count} rows</span>
                </div>
                <div class="project-card-meta-item">
                    <i class="fas fa-clock" style="color:#777;"></i>
                    <span>${lastModified}</span>
                </div>
                ${ownerInfo}
            </div>
        </div>
    `;
}

/**
 * Show create project modal
 */
function showCreateProjectModal() {
    // Reset form
    $('#create-project-form')[0].reset();
    $('.custom-file-label').html('Choose CSV file...');
    $('#create-project-message').html('').removeClass('text-success text-danger');

    // Show modal
    $('#create-project-modal').modal('show');
}

/**
 * Handle project creation
 */
async function handleCreateProject() {
    const projectName = $('#project-name').val().trim();
    const description = $('#project-description').val().trim();
    const fileInput = $('#csv-file')[0];

    // Validation
    if (!projectName) {
        showMessage('create-project-message', 'Project name is required', 'danger');
        return;
    }

    if (!fileInput.files || fileInput.files.length === 0) {
        showMessage('create-project-message', 'Please select a CSV file', 'danger');
        return;
    }

    const file = fileInput.files[0];

    // Validate file extension
    if (!file.name.toLowerCase().endsWith('.csv')) {
        showMessage('create-project-message', 'Please select a valid CSV file', 'danger');
        return;
    }

    // Validate file size (50MB max)
    const maxSize = 50 * 1024 * 1024; // 50MB in bytes
    if (file.size > maxSize) {
        showMessage('create-project-message', 'File size exceeds 50MB limit', 'danger');
        return;
    }

    // Disable submit button
    const submitBtn = $('#submit-project-btn');
    submitBtn.prop('disabled', true).html('<i class="fas fa-spinner fa-spin"></i> Creating...');

    try {
        // Create FormData
        const formData = new FormData();
        formData.append('project_name', projectName);
        if (description) {
            formData.append('description', description);
        }
        formData.append('file', file);

        // Submit to server
        const response = await fetch('/lemma-workspace/projects/create', {
            method: 'POST',
            body: formData,
            credentials: 'include'
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || 'Failed to create project');
        }

        // Success
        showMessage('create-project-message', 'Project created successfully!', 'success');

        // Wait a moment then redirect
        setTimeout(() => {
            window.location.href = `/lemma-workspace/projects/${data.project_id}`;
        }, 1000);

    } catch (error) {
        console.error('Error creating project:', error);
        showMessage('create-project-message', error.message || 'Failed to create project', 'danger');
        submitBtn.prop('disabled', false).html('<i class="fas fa-upload"></i> Create Project');
    }
}

/**
 * Show/hide loading state
 */
function showLoading(show) {
    if (show) {
        $('#loading-state').show();
        $('#owned-projects-section, #shared-projects-section').hide();
    } else {
        $('#loading-state').hide();
        $('#owned-projects-section, #shared-projects-section').show();
    }
}

/**
 * Show error message
 */
function showError(message) {
    // Could be enhanced with a toast notification
    alert(message);
}

/**
 * Show message in specified element
 */
function showMessage(elementId, message, type) {
    const element = $(`#${elementId}`);
    element.html(`<div class="text-${type}">${escapeHtml(message)}</div>`);
}

/**
 * Format relative time (e.g., "2 hours ago")
 */
function formatRelativeTime(date) {
    const now = new Date();
    const diff = now - date;
    const seconds = Math.floor(diff / 1000);
    const minutes = Math.floor(seconds / 60);
    const hours = Math.floor(minutes / 60);
    const days = Math.floor(hours / 24);
    const months = Math.floor(days / 30);
    const years = Math.floor(days / 365);

    if (seconds < 60) return 'Just now';
    if (minutes < 60) return `${minutes} minute${minutes > 1 ? 's' : ''} ago`;
    if (hours < 24) return `${hours} hour${hours > 1 ? 's' : ''} ago`;
    if (days < 30) return `${days} day${days > 1 ? 's' : ''} ago`;
    if (months < 12) return `${months} month${months > 1 ? 's' : ''} ago`;
    return `${years} year${years > 1 ? 's' : ''} ago`;
}

/**
 * Escape HTML to prevent XSS
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
