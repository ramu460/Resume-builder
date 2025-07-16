// resume_form.js (Updated)

// This file now primarily handles the initial setup and event listeners
// The core formset logic (addFormset, removeForm, resetForm, resetField)
// is moved or enhanced within the script tag of _formset.html for better scope management
// and direct access to prefix and index.

// The functions in the _formset.html script tag are globally available.

// Toggle section visibility (can remain here or be moved to _formset.html if preferred)
function toggleSection(sectionId) {
    const section = document.getElementById(sectionId);
    // Assuming you have a chevron or indicator to rotate
    // const chevron = document.getElementById(sectionId.replace('-content', '-chevron'));

    if (section) {
        const formsContainer = section.querySelector('.space-y-4'); // Assuming this is inside the collapsible part
         if (formsContainer) {
            if (formsContainer.style.display === 'none' || formsContainer.style.display === '') {
                formsContainer.style.display = 'block';
                // if (chevron) chevron.classList.remove('rotate-180');
            } else {
                formsContainer.style.display = 'none';
                // if (chevron) chevron.classList.add('rotate-180');
            }
         }
    }
}


// Initialize everything when the DOM is ready
window.addEventListener('DOMContentLoaded', function () {
    // Initialize formsetCounters if not already done by _formset.html scripts
    window.formsetCounters = window.formsetCounters || {};

    const formsets = ['education', 'experience', 'skill', 'project', 'certification'];

    formsets.forEach(prefix => {
        const totalForms = document.getElementById(`id_${prefix}-TOTAL_FORMS`);
        if (totalForms && window.formsetCounters[prefix] === undefined) {
             // If _formset.html script hasn't set it, initialize here
             window.formsetCounters[prefix] = parseInt(totalForms.value);
        } else if (!totalForms) {
             console.error(`TOTAL_FORMS input not found for prefix: ${prefix}. Formset initialization may fail.`);
             window.formsetCounters[prefix] = 0; // Default to 0 if not found
        }


        // Add event listeners to initial remove buttons (those rendered by Django)
        const container = document.getElementById(`${prefix}-forms-container`);
        if (container) {
            container.querySelectorAll('.formset-form').forEach((form, index) => {
                // Ensure the remove button has the correct onclick attribute initially
                const removeBtn = form.querySelector('button[onclick^="removeForm"]');
                if (removeBtn) {
                     // Update the onclick attribute if it's not already correct
                     if (!removeBtn.getAttribute('onclick').includes(`, ${index})`)) {
                         removeBtn.setAttribute('onclick', `removeForm(this, '${prefix}', ${index})`);
                     }
                     // No need to add a separate click listener, the onclick attribute handles it.
                }
            });
        }

        // Add event listeners to section headers for toggling (if you have them)
        // Example: Assuming a button or div triggers the toggle
        const toggleButton = document.querySelector(`[data-toggle-section="#${prefix}"]`);
        if (toggleButton) {
            toggleButton.addEventListener('click', function() {
                toggleSection(prefix); // Use the prefix directly if the section ID matches
            });
        }
    });

    // Example of how you might handle initial section state (e.g., collapsed)
    formsets.forEach(prefix => {
        // Assuming your collapsible content is inside a div with class 'space-y-4'
        const formsContainer = document.getElementById(prefix)?.querySelector('.space-y-4');
        if (formsContainer) {
             // You might want to keep sections collapsed by default
             // formsContainer.style.display = 'none';
        }
    });
});

// Expose globally (already done in _formset.html script now)
// window.addFormset = addFormset;
// window.removeForm = removeForm;
// window.resetFormset = resetFormset;
// window.toggleSection = toggleSection; // Keep this if it's used outside the formset script
document.addEventListener('DOMContentLoaded', function() {
    const countrySelect = document.getElementById('id_country');
    const stateSelect = document.getElementById('id_state');

    async function loadStates(countryCode) {
        if (!countryCode) {
            stateSelect.innerHTML = '<option value="">Select country first</option>';
            stateSelect.disabled = true;
            return;
        }

        stateSelect.innerHTML = '<option value="">Loading states...</option>';
        stateSelect.disabled = true;

        try {
            const response = await fetch(`/resumes/api/states/${countryCode}/`);
            if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);

            const states = await response.json();
            stateSelect.innerHTML = '<option value="">Select State</option>';
            states.forEach(state => {
                const option = new Option(state.name, state.code);
                stateSelect.add(option);
            });
            
            // Restore saved state if editing
            const savedState = "{{ resume_form.state.value|default:'' }}";
            if (savedState) {
                stateSelect.value = savedState;
            }
            
            stateSelect.disabled = false;
        } catch (error) {
            console.error('Failed to load states:', error);
            stateSelect.innerHTML = '<option value="">Error loading states</option>';
            stateSelect.disabled = true;
        }
    }

    if (countrySelect) {
        countrySelect.addEventListener('change', () => loadStates(countrySelect.value));
        
        // Load states on initial page load if country is selected
        if (countrySelect.value) {
            loadStates(countrySelect.value);
        }
    }
});