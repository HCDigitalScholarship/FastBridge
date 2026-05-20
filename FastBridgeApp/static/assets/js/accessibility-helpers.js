/**
 * Accessibility Helper Functions for FastBridge
 * WCAG 2.1 AA Compliance utilities
 */

const AccessibilityHelpers = {
  /**
   * Announce message to screen readers
   * WCAG 2.1 Success Criterion 4.1.3
   * @param {string} message - The message to announce
   * @param {string} type - 'polite' or 'assertive' (default: 'polite')
   * @param {number} timeout - Auto-clear timeout in ms (default: 5000, 0 = no auto-clear)
   */
  announce(message, type = 'polite', timeout = 5000) {
    const liveRegion = document.getElementById('aria-live-announcer');
    if (!liveRegion) {
      console.warn('ARIA live region not found');
      return;
    }

    liveRegion.setAttribute('aria-live', type);
    liveRegion.textContent = message;

    if (timeout > 0) {
      setTimeout(() => {
        liveRegion.textContent = '';
      }, timeout);
    }
  },

  /**
   * Trap focus within a modal dialog
   * WCAG 2.1 Success Criterion 2.4.3
   * @param {HTMLElement} element - The element to trap focus within
   * @returns {Function} Cleanup function to remove event listener
   */
  trapFocus(element) {
    const focusableElements = element.querySelectorAll(
      'a[href], button:not([disabled]), textarea, input:not([type="hidden"]):not([disabled]), select:not([disabled]), [tabindex]:not([tabindex="-1"])'
    );
    const firstFocusable = focusableElements[0];
    const lastFocusable = focusableElements[focusableElements.length - 1];

    const trapHandler = (e) => {
      if (e.key !== 'Tab') return;

      if (e.shiftKey) {
        if (document.activeElement === firstFocusable) {
          lastFocusable.focus();
          e.preventDefault();
        }
      } else {
        if (document.activeElement === lastFocusable) {
          firstFocusable.focus();
          e.preventDefault();
        }
      }
    };

    element.addEventListener('keydown', trapHandler);

    // Return cleanup function
    return () => element.removeEventListener('keydown', trapHandler);
  },

  /**
   * Manage modal focus and return focus on close
   * WCAG 2.1 Success Criterion 2.4.3
   */
  managedModal: {
    previousFocus: null,
    cleanupFn: null,

    /**
     * Open a modal with proper focus management
     * @param {HTMLElement} modalElement - The modal element
     */
    open(modalElement) {
      this.previousFocus = document.activeElement;

      // Find first focusable element in modal
      const focusableElements = modalElement.querySelectorAll(
        'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
      );

      if (focusableElements.length > 0) {
        // Small delay to ensure modal is visible
        setTimeout(() => {
          focusableElements[0].focus();
        }, 100);
      }

      // Set up focus trap
      this.cleanupFn = AccessibilityHelpers.trapFocus(modalElement);
    },

    /**
     * Close the modal and restore focus
     */
    close() {
      if (this.cleanupFn) {
        this.cleanupFn();
        this.cleanupFn = null;
      }

      if (this.previousFocus && this.previousFocus.focus) {
        this.previousFocus.focus();
        this.previousFocus = null;
      }
    }
  },

  /**
   * Create accessible button with proper ARIA attributes
   * @param {Object} options - Button configuration
   * @param {string} options.text - Button text content
   * @param {string} options.ariaLabel - ARIA label (required for icon-only buttons)
   * @param {string} options.icon - Icon HTML (FontAwesome, etc.)
   * @param {Function} options.onClick - Click handler
   * @param {string} options.className - CSS classes
   * @param {string} options.id - Button ID
   * @returns {HTMLButtonElement} The created button element
   */
  createButton(options) {
    const {
      text,
      ariaLabel,
      icon,
      onClick,
      className = '',
      id = ''
    } = options;

    const button = document.createElement('button');
    button.className = className;
    if (id) button.id = id;
    button.setAttribute('type', 'button');

    if (icon && !text) {
      // Icon-only button needs aria-label
      if (!ariaLabel) {
        console.warn('Icon-only button created without aria-label');
      }
      button.setAttribute('aria-label', ariaLabel || 'Button');
      button.innerHTML = icon;
      // Mark icon as decorative
      const iconElement = button.querySelector('i, svg');
      if (iconElement) {
        iconElement.setAttribute('aria-hidden', 'true');
      }
    } else if (icon && text) {
      // Icon with text
      button.innerHTML = `${icon} <span>${text}</span>`;
      if (ariaLabel) {
        button.setAttribute('aria-label', ariaLabel);
      }
      // Mark icon as decorative
      const iconElement = button.querySelector('i, svg');
      if (iconElement) {
        iconElement.setAttribute('aria-hidden', 'true');
      }
    } else {
      button.textContent = text;
    }

    if (onClick) {
      button.addEventListener('click', onClick);
    }

    return button;
  },

  /**
   * Show field validation error with ARIA
   * @param {HTMLInputElement} inputElement - The input element
   * @param {string} errorMessage - The error message to display
   */
  showFieldError(inputElement, errorMessage) {
    inputElement.setAttribute('aria-invalid', 'true');

    const errorId = inputElement.getAttribute('aria-describedby');
    if (errorId) {
      const errorElement = document.getElementById(errorId);
      if (errorElement) {
        errorElement.textContent = errorMessage;
      }
    }

    // Announce error
    this.announce(errorMessage, 'assertive');
  },

  /**
   * Clear field validation error
   * @param {HTMLInputElement} inputElement - The input element
   */
  clearFieldError(inputElement) {
    inputElement.setAttribute('aria-invalid', 'false');

    const errorId = inputElement.getAttribute('aria-describedby');
    if (errorId) {
      const errorElement = document.getElementById(errorId);
      if (errorElement) {
        errorElement.textContent = '';
      }
    }
  },

  /**
   * Set loading state with ARIA
   * @param {HTMLElement} container - Container element
   * @param {boolean} isLoading - Loading state
   * @param {string} message - Optional loading message
   */
  setLoadingState(container, isLoading, message = 'Loading...') {
    if (isLoading) {
      container.setAttribute('aria-busy', 'true');
      if (message) {
        this.announce(message, 'polite');
      }
    } else {
      container.setAttribute('aria-busy', 'false');
    }
  },

  /**
   * Update tab selection state with ARIA
   * @param {HTMLElement} selectedTab - The tab button that was selected
   * @param {NodeList|Array} allTabs - All tab buttons
   * @param {HTMLElement} selectedPanel - The panel to show
   * @param {NodeList|Array} allPanels - All tab panels
   */
  updateTabSelection(selectedTab, allTabs, selectedPanel, allPanels) {
    // Update tab buttons
    allTabs.forEach(tab => {
      const isSelected = tab === selectedTab;
      tab.setAttribute('aria-selected', isSelected);
      tab.setAttribute('tabindex', isSelected ? '0' : '-1');
    });

    // Update panels
    allPanels.forEach(panel => {
      const isVisible = panel === selectedPanel;
      panel.setAttribute('aria-hidden', !isVisible);
      if (isVisible) {
        panel.style.display = 'block';
      } else {
        panel.style.display = 'none';
      }
    });

    // Announce tab change
    const tabName = selectedTab.textContent.trim();
    this.announce(`${tabName} tab selected`, 'polite');
  },

  /**
   * Setup keyboard navigation for tab controls
   * @param {HTMLElement} tablist - The tablist container
   */
  setupTabKeyboardNav(tablist) {
    const tabs = Array.from(tablist.querySelectorAll('[role="tab"]'));

    tabs.forEach((tab, index) => {
      tab.addEventListener('keydown', function(e) {
        let newIndex = -1;

        // Arrow key navigation
        if (e.key === 'ArrowRight' || e.key === 'ArrowDown') {
          e.preventDefault();
          newIndex = (index + 1) % tabs.length;
        } else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') {
          e.preventDefault();
          newIndex = (index - 1 + tabs.length) % tabs.length;
        } else if (e.key === 'Home') {
          e.preventDefault();
          newIndex = 0;
        } else if (e.key === 'End') {
          e.preventDefault();
          newIndex = tabs.length - 1;
        }

        if (newIndex !== -1) {
          tabs[newIndex].focus();
          tabs[newIndex].click();
        }
      });
    });
  }
};

// Make globally available
window.AccessibilityHelpers = AccessibilityHelpers;
