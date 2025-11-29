// Health Economic Modeling Hub - JavaScript Utilities
// Enhances Dash application with client-side interactivity

console.log('Health Economic Modeling Hub - JavaScript Loaded');

// Wait for DOM to be ready
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM Ready - Initializing JavaScript utilities');
    
    // Initialize sidebar toggle
    initializeSidebarToggle();
    
    // Initialize tooltips
    initializeTooltips();
    
    // Add smooth scrolling
    enableSmoothScroll();
    
    // Add keyboard shortcuts
    setupKeyboardShortcuts();
    
    // Add loading indicators
    setupLoadingIndicators();
    
    // Add form validation helpers
    setupFormValidation();
});

/**
 * Initialize sidebar collapse/expand functionality
 */
function initializeSidebarToggle() {
    // This is handled by Dash callbacks, but we can add smooth transitions
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.attributeName === 'class') {
                const sidebar = document.querySelector('.app-sidebar');
                const mainContent = document.querySelector('.app-content');
                
                if (sidebar && mainContent) {
                    // Add smooth transition classes
                    sidebar.style.transition = 'width 0.3s ease';
                    mainContent.style.transition = 'margin-left 0.3s ease, width 0.3s ease';
                }
            }
        });
    });
    
    const sidebar = document.querySelector('.app-sidebar');
    if (sidebar) {
        observer.observe(sidebar, { attributes: true });
    }
    
    console.log('Sidebar toggle initialized');
}

/**
 * Initialize Bootstrap tooltips
 */
function initializeTooltips() {
    try {
        const tooltipTriggerList = [].slice.call(
            document.querySelectorAll('[data-bs-toggle="tooltip"]')
        );
        tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
        console.log('Tooltips initialized');
    } catch (error) {
        console.warn('Bootstrap tooltips not available:', error);
    }
}

/**
 * Enable smooth scrolling for anchor links
 */
function enableSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                e.preventDefault();
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    console.log('Smooth scrolling enabled');
}

/**
 * Setup keyboard shortcuts
 */
function setupKeyboardShortcuts() {
    document.addEventListener('keydown', function(e) {
        // Ctrl/Cmd + S to save (prevent default browser save)
        if ((e.ctrlKey || e.metaKey) && e.key === 's') {
            e.preventDefault();
            const saveButton = document.querySelector('[id*="save-button"]');
            if (saveButton) {
                saveButton.click();
                showNotification('Save triggered via keyboard shortcut', 'info');
            }
        }
        
        // Ctrl/Cmd + K for quick search
        if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
            e.preventDefault();
            const searchInput = document.querySelector('input[type="search"]');
            if (searchInput) {
                searchInput.focus();
            }
        }
        
        // Escape to close modals
        if (e.key === 'Escape') {
            const modals = document.querySelectorAll('.modal.show');
            modals.forEach(modal => {
                const closeBtn = modal.querySelector('[data-bs-dismiss="modal"]');
                if (closeBtn) closeBtn.click();
            });
        }
    });
    console.log('Keyboard shortcuts enabled');
}

/**
 * Setup loading indicators for AJAX requests
 */
function setupLoadingIndicators() {
    // Monitor for Dash callback execution
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.attributeName === 'data-dash-is-loading') {
                const isLoading = mutation.target.getAttribute('data-dash-is-loading') === 'true';
                if (isLoading) {
                    showLoadingOverlay();
                } else {
                    hideLoadingOverlay();
                }
            }
        });
    });
    
    // Observe the body for loading states
    observer.observe(document.body, {
        attributes: true,
        attributeFilter: ['data-dash-is-loading']
    });
    
    console.log('Loading indicators setup complete');
}

/**
 * Show loading overlay
 */
function showLoadingOverlay() {
    let overlay = document.getElementById('loading-overlay');
    if (!overlay) {
        overlay = document.createElement('div');
        overlay.id = 'loading-overlay';
        overlay.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.7);
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 9999;
        `;
        overlay.innerHTML = `
            <div style="text-align: center;">
                <div class="loading-spinner"></div>
                <p style="color: #dc2626; margin-top: 20px; font-size: 1.2rem;">Processing...</p>
            </div>
        `;
        document.body.appendChild(overlay);
    }
    overlay.style.display = 'flex';
}

/**
 * Hide loading overlay
 */
function hideLoadingOverlay() {
    const overlay = document.getElementById('loading-overlay');
    if (overlay) {
        overlay.style.display = 'none';
    }
}

/**
 * Setup form validation helpers
 */
function setupFormValidation() {
    // Add real-time validation for numeric inputs
    document.addEventListener('input', function(e) {
        if (e.target.type === 'number') {
            validateNumericInput(e.target);
        }
    });
    
    console.log('Form validation helpers enabled');
}

/**
 * Validate numeric input
 */
function validateNumericInput(input) {
    const value = parseFloat(input.value);
    const min = parseFloat(input.min);
    const max = parseFloat(input.max);
    
    let isValid = true;
    let message = '';
    
    if (isNaN(value)) {
        isValid = false;
        message = 'Please enter a valid number';
    } else if (!isNaN(min) && value < min) {
        isValid = false;
        message = `Value must be at least ${min}`;
    } else if (!isNaN(max) && value > max) {
        isValid = false;
        message = `Value must be at most ${max}`;
    }
    
    if (!isValid) {
        input.classList.add('is-invalid');
        showInputError(input, message);
    } else {
        input.classList.remove('is-invalid');
        removeInputError(input);
    }
}

/**
 * Show input error message
 */
function showInputError(input, message) {
    let errorDiv = input.nextElementSibling;
    if (!errorDiv || !errorDiv.classList.contains('invalid-feedback')) {
        errorDiv = document.createElement('div');
        errorDiv.className = 'invalid-feedback';
        input.parentNode.insertBefore(errorDiv, input.nextSibling);
    }
    errorDiv.textContent = message;
    errorDiv.style.display = 'block';
}

/**
 * Remove input error message
 */
function removeInputError(input) {
    const errorDiv = input.nextElementSibling;
    if (errorDiv && errorDiv.classList.contains('invalid-feedback')) {
        errorDiv.style.display = 'none';
    }
}

/**
 * Show notification toast
 */
function showNotification(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `alert alert-${type} notification-toast`;
    toast.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 10000;
        min-width: 250px;
        animation: slideIn 0.3s ease-out;
    `;
    toast.textContent = message;
    
    document.body.appendChild(toast);
    
    setTimeout(() => {
        toast.style.animation = 'slideOut 0.3s ease-out';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

/**
 * Export calculation results to CSV
 */
function exportToCSV(data, filename) {
    const csv = convertToCSV(data);
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    a.click();
    window.URL.revokeObjectURL(url);
}

/**
 * Convert data to CSV format
 */
function convertToCSV(data) {
    if (!data || !data.length) return '';
    
    const headers = Object.keys(data[0]);
    const csv = [
        headers.join(','),
        ...data.map(row => 
            headers.map(header => 
                JSON.stringify(row[header] || '')
            ).join(',')
        )
    ].join('\n');
    
    return csv;
}

/**
 * Format currency values
 */
function formatCurrency(value, currency = 'USD') {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: currency
    }).format(value);
}

/**
 * Format percentage values
 */
function formatPercentage(value, decimals = 2) {
    return (value * 100).toFixed(decimals) + '%';
}

/**
 * Debounce function for performance
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
 * Local storage helpers
 */
const storage = {
    set: function(key, value) {
        try {
            localStorage.setItem(key, JSON.stringify(value));
        } catch (e) {
            console.error('Error saving to localStorage:', e);
        }
    },
    get: function(key) {
        try {
            const item = localStorage.getItem(key);
            return item ? JSON.parse(item) : null;
        } catch (e) {
            console.error('Error reading from localStorage:', e);
            return null;
        }
    },
    remove: function(key) {
        try {
            localStorage.removeItem(key);
        } catch (e) {
            console.error('Error removing from localStorage:', e);
        }
    }
};

// Add animation keyframes
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// Export utilities for use in Dash callbacks
window.healthEconUtils = {
    exportToCSV,
    formatCurrency,
    formatPercentage,
    showNotification,
    storage,
    debounce
};

console.log('Health Economic Modeling Hub - JavaScript utilities ready');
