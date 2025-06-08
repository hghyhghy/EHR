// Global variables
let medicalRecords = [];
let allMedicalRecords = [];
let csrfToken = '';
let selectedCategory = null;
const pathParts = window.location.pathname.split('/');
const memberID = pathParts[pathParts.length - 2] || pathParts[pathParts.length - 1]; 

// Get CSRF token
function getCSRFToken() {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        const [name, value] = cookie.trim().split('=');
        if (name === 'csrftoken') {
            return value;
        }
    }
    return '';
}

// Initialize tokens and IDs
csrfToken = getCSRFToken();

// Utility functions
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

function showMessage(message, type = 'success') {
    const messagesDiv = document.getElementById('formMessages');
    messagesDiv.innerHTML = `<div class="${type}-message">${message}</div>`;
    setTimeout(() => {
        messagesDiv.innerHTML = '';
    }, 5000);
}

// API calls - Unified fetch function
async function fetchRecords(categoryName = null) {
    console.log("Fetching records - Member ID:", memberID, "Category:", categoryName);
    
    try { 
        // Build URL with optional category parameter
        let url = `/api/medical-records/${memberID}/`;
        if (categoryName && categoryName.toLowerCase() !== 'all') {
            url += `?category=${encodeURIComponent(categoryName)}`;
        }
        
        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            },
            credentials: 'same-origin'
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const result = await response.json();
        const records = result.records || [];
        
        // Update global variables based on whether it's filtered or not
        if (!categoryName || categoryName.toLowerCase() === 'all') {
            // This is a fetch all records call
            allMedicalRecords = [...records];
            medicalRecords = [...records];
            selectedCategory = null;
        } else {
            // This is a filtered call - don't update allMedicalRecords
            medicalRecords = [...records];
            selectedCategory = categoryName;
        }
        
        renderRecords();
        console.log(`Loaded ${records.length} records${categoryName ? ` for category: ${categoryName}` : ''}`);

    } catch (error) {
        console.error('Error fetching records:', error);
        document.getElementById('recordsContainer').innerHTML =
            '<div class="error-message">Failed to load medical records. Please try again.</div>';
    }
}

async function saveRecord(formData) {
    try {
        console.log("Saving record for member ID:", memberID);
        
        // Debug: Log form data entries
        for (let [key, value] of formData.entries()) {
            console.log(key, value);
        }
        
        const response = await fetch(`/api/add-medical-records/${memberID}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
            },
            body: formData,
            credentials: 'same-origin'
        });
        
        console.log('Response status:', response.status);
        console.log('Response headers:', response.headers);

        if (response.ok) {
            console.log("Success");
            const result = await response.json();
            console.log('Response result:', result);
            
            showMessage('Medical record added successfully!', 'success');
            setTimeout(() => {
                closeForm();
                // Refresh records - maintain current filter if active
                if (selectedCategory) {
                    fetchRecords(selectedCategory);
                } else {
                    fetchRecords(); // Fetch all records
                }
            }, 1000);
        } else {
            // Handle error response
            const errorResult = await response.json();
            console.error('Error response:', errorResult);
            showMessage(`Failed to save record: ${errorResult.error || 'Unknown error'}`, 'error');
        }

    } catch (error) {
        console.error('Error saving record:', error);
        showMessage('Failed to save record. Please try again.', 'error');
    }
}

// Rendering functions
function renderRecords() {
    const container = document.getElementById('recordsContainer');

    if (medicalRecords.length === 0) {
        const message = selectedCategory 
            ? `No medical records found for category "${selectedCategory}". Try selecting a different category or add new records.`
            : 'No medical records found. Click "Add New Medical Record" to get started.';
        container.innerHTML = `<div class="no-records">${message}</div>`;
        return;
    }

    container.innerHTML = medicalRecords.map(record => `
        <button class="accordion" onclick="toggleAccordion(this)">
            <div>
                <strong>Medical Record - ${formatDate(record.uploaded_on).split(',')[0]}</strong>
                <br>
                <small style="opacity: 0.8;">Category: ${record.category || 'Uncategorized'} | Uploaded: ${formatDate(record.uploaded_on)}</small>
            </div>
            
            <span class="accordion-icon">▼</span>
        </button>
        <div class="panel">
            <div class="record-details">
                <div class="detail-item">
                    <h4>Category</h4>
                    <p>${record.category || 'Uncategorized'}</p>
                </div>
                <div class="detail-item">
                    <h4>Files</h4>
                    <div class="file-links">
                        ${record.report_file ? `<a href="${record.report_file}" class="file-link" target="_blank">📄 Report</a>` : ''}
                        ${record.prescription_file ? `<a href="${record.prescription_file}" class="file-link" target="_blank">📋 Prescription</a>` : ''}
                        ${!record.report_file && !record.prescription_file ? '<p>No files uploaded</p>' : ''}
                    </div>
                </div>
                <div class="detail-item">
                    <h4>Upload Date</h4>
                    <p>${formatDate(record.uploaded_on)}</p>
                </div>
                <div class="detail-item">
                    <h4>Medicines</h4>
                    <p>${record.medicines_name || 'Not specified'}</p>
                </div>
                <div class="detail-item">
                    <h4>Prescribed Tests</h4>
                    <p>${record.prescribed_tests || 'Not specified'}</p>
                </div>
            </div>
        </div>
    `).join('');
}

function toggleAccordion(element) {
    const panel = element.nextElementSibling;

    const isActive = element.classList.contains('active');

    // Close all accordions and reset icons
    document.querySelectorAll('.accordion').forEach(acc => {
        acc.classList.remove('active');
        acc.nextElementSibling.classList.remove('active');
        const icon = acc.querySelector('.accordion-icon');
        if (icon) icon.textContent = '▼';
    });

    // Toggle the clicked accordion if it was not active
    if (!isActive) {
        element.classList.add('active');
        panel.classList.add('active');
        const icon = element.querySelector('.accordion-icon');
        if (icon) icon.textContent = '▲';  // Up arrow when open
    }
}

// Simplified category filtering
function filterByCategory(categoryName) {
    console.log("Filtering by category:", categoryName);
    
    // Update active button styling
    updateActiveButton(categoryName);
    
    // Fetch records with the selected category
    fetchRecords(categoryName);
}

// Helper function to update active button styling
function updateActiveButton(categoryName) {
    document.querySelectorAll('.category-btn').forEach(btn => {
        btn.classList.remove('active');
        if (btn.textContent === categoryName) {
            btn.classList.add('active');
        }
    });
}

// Form functions
function openForm() {
    document.getElementById('formOverlay').style.display = 'flex';
    document.body.style.overflow = 'hidden';
    document.getElementById('formMessages').innerHTML = '';
}

function closeForm() {
    document.getElementById('formOverlay').style.display = 'none';
    document.body.style.overflow = 'auto';
    document.getElementById('medicalRecordForm').reset();
    document.getElementById('formMessages').innerHTML = '';
}

// Form submission handler
async function handleFormSubmit(e) {
    e.preventDefault();

    const form = document.getElementById('medicalRecordForm');
    const formData = new FormData(form);
    const reportFile = formData.get('report_file');
    const selectedCategory = formData.get('medical_category');
    console.log('Selected category:', selectedCategory);
    const medicinesName = formData.get('medicines_name');
    // For prescription_file
    const prescriptionFile = document.getElementById('prescription_file');
    if (prescriptionFile) {
        formData.append('prescription_file', prescriptionFile);
    } else {
        formData.append('prescription_file', 'NULL'); // Send string "NULL"
    }

    // For prescribed_tests
    const prescribedTests = formData.get('prescribed_tests');

    if (prescribedTests) {
        formData.append('prescribed_tests', prescribedTests);
    } else {
        formData.append('prescribed_tests', 'NULL'); // Send string "NULL"
    }

    // Validate form
    if (!reportFile && !prescriptionFile) {
        showMessage('Please upload at least one file (report or prescription).', 'error');
        return;
    }

    if (!medicinesName && !prescribedTests) {
        showMessage('Please fill in at least medicines or prescribed tests.', 'error');
        return;
    }

    const saveButton = document.getElementById('saveButton');
    
    saveRecord(formData);
}

// Initialize the page
document.addEventListener('DOMContentLoaded', function () {
    console.log("DOM loaded, member ID:", memberID);
    
    loadCategories();
    loadCategoriesForForm() 
});

async function loadCategories() {
    try {
        const response = await fetch('/api/categories/');
        const data = await response.json();
        const container = document.querySelector('.category-buttons');

        // Add "All" button
        const allBtn = document.createElement('button');
        allBtn.textContent = 'All';
        allBtn.className = 'category-btn active'; // Start with "All" as active
        allBtn.onclick = () => filterByCategory("All");
        container.appendChild(allBtn);

        // Add category buttons
        data.forEach(category => {
            const btn = document.createElement('button');
            btn.className = 'category-btn';
            btn.textContent = category.name;
            btn.onclick = () => filterByCategory(category.name);
            container.appendChild(btn);
        });
        
        console.log("Categories loaded:", data);
        
        // Load all records initially
        fetchRecords();
        
    } catch (err) {
        console.error("Failed to load categories", err);
        // Still try to load records even if categories fail
        fetchRecords();
    }
}
async function loadCategoriesForForm() {
    console.log("Click detected")
    try {
        const response = await fetch('/api/categories/');
        const data = await response.json();
        console.log("Category for post", data);

        // Get the existing select element
        const selectElement = document.querySelector('.category-dropdown');

        // Clear any existing options first
        selectElement.innerHTML = '';

        // Add a default option with null value
        const defaultOption = document.createElement('option');
        defaultOption.value = '';  // Changed from '' to 'null'
        defaultOption.textContent = 'Select a category';
        selectElement.appendChild(defaultOption);

        // Add category options
        data.forEach(category => {
            const option = document.createElement('option');
            option.value = category.id;
            option.textContent = category.name;
            selectElement.appendChild(option);
        });

        // ADD THIS: Event listener to handle selection changes
        selectElement.addEventListener('change', function() {
            const selectedValue = this.value;
            // console.log('Selected category ID:', selectedValue);
            
            // Optional: Store selected value for debugging
            if (selectedValue) {
                console.log('Category selected:', selectedValue);
            } else {
                console.log('No category selected (default option)');
            }
        });

    }
    catch {
        alert("Not able to load categories!");
    }
}