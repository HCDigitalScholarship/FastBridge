/**
 * Bootstrap Modal Accessibility Enhancements
 * Automatically enhances all Bootstrap modals with WCAG 2.1 AA compliance
 */
(function() {
  'use strict';

  // Track previously focused element
  let previousFocus = null;
  let focusTrapCleanup = null;

  /**
   * Initialize accessibility enhancements when DOM is ready
   */
  function initModalAccessibility() {
    // Find all Bootstrap modals
    const modals = document.querySelectorAll('.modal');

    modals.forEach(modal => {
      enhanceModal(modal);
    });
  }

  /**
   * Enhance a single modal with ARIA attributes and event handlers
   * @param {HTMLElement} modal - The modal element
   */
  function enhanceModal(modal) {
    // Add ARIA attributes if not already present
    if (!modal.hasAttribute('role')) {
      modal.setAttribute('role', 'dialog');
    }
    if (!modal.hasAttribute('aria-modal')) {
      modal.setAttribute('aria-modal', 'true');
    }

    // Find modal title and link it
    const modalTitle = modal.querySelector('.modal-title');
    if (modalTitle) {
      if (!modalTitle.id) {
        // Generate unique ID for title
        modalTitle.id = `modal-title-${Math.random().toString(36).substr(2, 9)}`;
      }
      if (!modal.hasAttribute('aria-labelledby')) {
        modal.setAttribute('aria-labelledby', modalTitle.id);
      }
    }

    // Set up event handlers using jQuery (Bootstrap 4 uses jQuery)
    $(modal).on('show.bs.modal', function(e) {
      handleModalShow(modal);
    });

    $(modal).on('shown.bs.modal', function(e) {
      handleModalShown(modal);
    });

    $(modal).on('hide.bs.modal', function(e) {
      handleModalHide(modal);
    });

    $(modal).on('hidden.bs.modal', function(e) {
      handleModalHidden(modal);
    });
  }

  /**
   * Handle modal show event (before animation)
   * @param {HTMLElement} modal - The modal element
   */
  function handleModalShow(modal) {
    // Store previously focused element
    previousFocus = document.activeElement;
  }

  /**
   * Handle modal shown event (after animation complete)
   * @param {HTMLElement} modal - The modal element
   */
  function handleModalShown(modal) {
    // Find first focusable element in modal
    const focusableElements = modal.querySelectorAll(
      'button:not([disabled]), [href], input:not([disabled]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])'
    );

    // Focus first element, preferring the close button or first input
    let elementToFocus = focusableElements[0];

    // Try to find a better element to focus
    const closeButton = modal.querySelector('[data-dismiss="modal"]');
    const firstInput = modal.querySelector('input:not([type="hidden"]), textarea, select');

    if (firstInput) {
      elementToFocus = firstInput;
    } else if (closeButton) {
      elementToFocus = closeButton;
    }

    if (elementToFocus) {
      elementToFocus.focus();
    }

    // Set up focus trap
    if (window.AccessibilityHelpers && window.AccessibilityHelpers.trapFocus) {
      focusTrapCleanup = window.AccessibilityHelpers.trapFocus(modal);
    } else {
      // Fallback focus trap implementation
      focusTrapCleanup = setupBasicFocusTrap(modal);
    }

    // Add Escape key handler
    modal.addEventListener('keydown', handleEscapeKey);
  }

  /**
   * Handle modal hide event (before animation, before aria-hidden is set)
   * @param {HTMLElement} modal - The modal element
   */
  function handleModalHide(modal) {
    // Blur any focused element inside the modal to prevent aria-hidden warning
    const activeElement = document.activeElement;
    if (activeElement && modal.contains(activeElement)) {
      activeElement.blur();
    }
  }

  /**
   * Handle modal hidden event
   * @param {HTMLElement} modal - The modal element
   */
  function handleModalHidden(modal) {
    // Clean up focus trap
    if (focusTrapCleanup) {
      focusTrapCleanup();
      focusTrapCleanup = null;
    }

    // Remove Escape key handler
    modal.removeEventListener('keydown', handleEscapeKey);

    // Return focus to previously focused element
    if (previousFocus && previousFocus.focus) {
      // Small delay to ensure modal is fully hidden
      setTimeout(() => {
        // Check again that element still exists and can receive focus
        if (previousFocus && document.body.contains(previousFocus) && previousFocus.focus) {
          try {
            previousFocus.focus();
          } catch (e) {
            // Element no longer focusable, ignore
            console.debug('Could not restore focus to previous element:', e);
          }
        }
      }, 50);
    }
    previousFocus = null;

    // Announce modal closed
    if (window.AccessibilityHelpers && window.AccessibilityHelpers.announce) {
      window.AccessibilityHelpers.announce('Dialog closed', 'polite');
    }
  }

  /**
   * Handle Escape key press
   * @param {KeyboardEvent} e - The keyboard event
   */
  function handleEscapeKey(e) {
    if (e.key === 'Escape') {
      const closeButton = e.currentTarget.querySelector('[data-dismiss="modal"]');
      if (closeButton) {
        closeButton.click();
      }
    }
  }

  /**
   * Basic focus trap implementation (fallback)
   * @param {HTMLElement} element - The element to trap focus within
   * @returns {Function} Cleanup function
   */
  function setupBasicFocusTrap(element) {
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

    return () => element.removeEventListener('keydown', trapHandler);
  }

  // Initialize when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initModalAccessibility);
  } else {
    initModalAccessibility();
  }

  // Also watch for dynamically added modals
  if (window.MutationObserver) {
    const observer = new MutationObserver(function(mutations) {
      mutations.forEach(function(mutation) {
        mutation.addedNodes.forEach(function(node) {
          if (node.nodeType === 1 && node.classList && node.classList.contains('modal')) {
            enhanceModal(node);
          }
        });
      });
    });

    // Start observing after DOM is ready
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', function() {
        observer.observe(document.body, { childList: true, subtree: true });
      });
    } else {
      observer.observe(document.body, { childList: true, subtree: true });
    }
  }
})();
