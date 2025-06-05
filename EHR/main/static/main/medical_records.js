// Global variables
let medicalRecords = [];
let csrfToken = '';
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

// API calls
async function fetchRecords() {
    console.log("Function loaded! Member ID:", memberID);
    try { 
        const response = await fetch(`/api/medical-records/${memberID}/`, {
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
        medicalRecords = result.records || [];
        renderRecords();

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
            const result = await response.json(); // Changed from response.text() to response.json()
            console.log('Response result:', result);
            
            showMessage('Medical record added successfully!', 'success');
            setTimeout(() => {
                closeForm();
                fetchRecords(); // Refresh the records
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

async function deleteRecord(recordId) {
    if (!confirm('Are you sure you want to delete this medical record?')) {
        return;
    }

    try {
        const response = await fetch(`/api/medical-records/delete/${recordId}/`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            },
            credentials: 'same-origin'
        });

        const result = await response.json();

        if (response.ok) {
            // Remove record from local array
            medicalRecords = medicalRecords.filter(record => record.id !== recordId);
            renderRecords();
            showMessage('Record deleted successfully!', 'success');
        } else {
            throw new Error(result.error || 'Failed to delete record');
        }

    } catch (error) {
        console.error('Error deleting record:', error);
        alert('Failed to delete record. Please try again.');
    }
}

// Rendering functions
function renderRecords() {
    const container = document.getElementById('recordsContainer');

    if (medicalRecords.length === 0) {
        container.innerHTML = '<div class="no-records">No medical records found. Click "Add New Medical Record" to get started.</div>';
        return;
    }

    container.innerHTML = medicalRecords.map(record => `
        <button class="accordion" onclick="toggleAccordion(this)">
            <div>
                <strong>Medical Record - ${formatDate(record.uploaded_on).split(',')[0]}</strong>
                <br>
                <small style="opacity: 0.8;">Uploaded: ${formatDate(record.uploaded_on)}</small>
            </div>
            <button class="delete-btn" onclick="event.stopPropagation(); deleteRecord(${record.id})">
                Delete
            </button>
            <span class="accordion-icon">▼</span>
        </button>
        <div class="panel">
            <div class="record-details">
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

    // Close all other accordions
    document.querySelectorAll('.accordion').forEach(acc => {
        if (acc !== element) {
            acc.classList.remove('active');
            acc.nextElementSibling.classList.remove('active');
        }
    });

    // Toggle current accordion
    element.classList.toggle('active');
    panel.classList.toggle('active');
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
    
    const medicinesName = formData.get('medicines_name');
   // For prescription_file
    const prescriptionFile = document.getElementById('prescription_file');
    if (prescriptionFile) {
        formData.append('prescription_file', prescriptionFile);
    } else {
        formData.append('prescription_file', 'NULL'); // Send string "NULL"
    }

    // For prescribed_tests
    const prescribedTests = document.getElementById('prescribed_tests');
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
    fetchRecords();
});