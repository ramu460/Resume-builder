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
//state.js
// Toggle custom state input visibility
document.addEventListener('DOMContentLoaded', function () {
    const countrySelect = document.getElementById('id_country');
    const stateSelect = document.getElementById('id_state');

    const countryStateData = {
        countries: [
            { code: "US", name: "United States" },
            { code: "CA", name: "Canada" },
            { code: "GB", name: "United Kingdom" },
            { code: "AU", name: "Australia" },
            { code: "IN", name: "India" }
        ],
        states: {
            'US': [
                { code: "CA", name: "California" },
                { code: "TX", name: "Texas" },
                { code: "NY", name: "New York" }
                // Add more if needed
            ],
            'CA': [
                { code: "ON", name: "Ontario" },
                { code: "QC", name: "Quebec" },
                { code: "BC", name: "British Columbia" }
                // Add more if needed
            ],
            'IN': [
                { code: "AP", name: "Andhra Pradesh" },
                { code: "AR", name: "Arunachal Pradesh" },
                { code: "AS", name: "Assam" },
                { code: "BR", name: "Bihar" },
                { code: "CT", name: "Chhattisgarh" },
                { code: "GA", name: "Goa" },
                { code: "GJ", name: "Gujarat" },
                { code: "HR", name: "Haryana" },
                { code: "HP", name: "Himachal Pradesh" },
                { code: "JH", name: "Jharkhand" },
                { code: "KA", name: "Karnataka" },
                { code: "KL", name: "Kerala" },
                { code: "MP", name: "Madhya Pradesh" },
                { code: "MH", name: "Maharashtra" },
                { code: "MN", name: "Manipur" },
                { code: "ML", name: "Meghalaya" },
                { code: "MZ", name: "Mizoram" },
                { code: "NL", name: "Nagaland" },
                { code: "OD", name: "Odisha" },
                { code: "PB", name: "Punjab" },
                { code: "RJ", name: "Rajasthan" },
                { code: "SK", name: "Sikkim" },
                { code: "TN", name: "Tamil Nadu" },
                { code: "TG", name: "Telangana" },
                { code: "TR", name: "Tripura" },
                { code: "UP", name: "Uttar Pradesh" },
                { code: "UT", name: "Uttarakhand" },
                { code: "WB", name: "West Bengal" },
                // Union Territories
                { code: "AN", name: "Andaman and Nicobar Islands" },
                { code: "CH", name: "Chandigarh" },
                { code: "DN", name: "Dadra and Nagar Haveli and Daman and Diu" },
                { code: "DL", name: "Delhi" },
                { code: "JK", name: "Jammu and Kashmir" },
                { code: "LA", name: "Ladakh" },
                { code: "LD", name: "Lakshadweep" },
                { code: "PY", name: "Puducherry" }
            ],
            'AU': [
                { code: "NSW", name: "New South Wales" },
                { code: "VIC", name: "Victoria" },
                { code: "QLD", name: "Queensland" }
                // Add more if needed
            ],
            'GB': [
                { code: "ENG", name: "England" },
                { code: "SCT", name: "Scotland" },
                { code: "WLS", name: "Wales" },
                { code: "NIR", name: "Northern Ireland" }
            ]
        }
    };

    countryStateData.countries.forEach(country => {
        const option = document.createElement('option');
        option.value = country.code;
        option.textContent = country.name;

        if (country.code === "{{ form.country.value|default:'' }}") {
            option.selected = true;
        }

        countrySelect.appendChild(option);
    });

    countrySelect.addEventListener('change', function () {
        stateSelect.disabled = !this.value;
        stateSelect.innerHTML = '<option value="">Select a state</option>';

        if (this.value && countryStateData.states[this.value]) {
            countryStateData.states[this.value].forEach(state => {
                const option = document.createElement('option');
                option.value = state.code;
                option.textContent = state.name;

                if (state.code === "{{ form.state.value|default:'' }}") {
                    option.selected = true;
                }

                stateSelect.appendChild(option);
            });
        }
    });

    if (countrySelect.value) {
        countrySelect.dispatchEvent(new Event('change'));
    }
});
