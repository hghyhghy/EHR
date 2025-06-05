let nextPage = null;
let prevPage = null;

async function loadFamilyMembers(url = '/api/user-details/') {
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

    const response = await fetch(url, {
        method: 'GET',
        headers: {
            "Accept": "application/json",
            'X-CSRFToken': csrfToken
        }
    });

    const data = await response.json();
    const profile =  data.results.profile
    const family =  data.results.family

    // Set profile username
    if (profile) {
        document.getElementById('user-username').textContent = profile.username;
    }

    // Render family members
    const familyBody = document.getElementById('family-body');
    familyBody.innerHTML = ''; // clear old rows

    family.forEach((member, index) => {
        const row = document.createElement('div');
        row.className = 'family-row';
        row.setAttribute('data-member-id', member.uuid);
        row.setAttribute('data-user-id', member.user_id);

        row.innerHTML = `
            <div class='family-cell2'>${index + 1}</div>
            <div class="family-cell">${member.username}</div>
            <div class="family-cell">${member.email}</div>
            <div class="family-cell">${member.dob || '-'}</div>
            <div class="family-cell">${member.gender || '-'}</div>
            <div class="family-cell">
                <div class="button-group">
                    <i class='bx bx-trash delete-btn' role='button' tabindex="0" data-member-id="${member.uuid}"></i>
                    <i class='bx bx-edit edit-btn' role='button' tabindex="0" data-member-id="${member.uuid}"></i>
                    <i class='bx bx-file-report record-btn' role='button' tabindex="0" data-user-id="${member.user_id}"></i>
                </div>
            </div>
        `;

        familyBody.appendChild(row);
    });

    // Update pagination links
    nextPage = data.next;
    prevPage = data.previous;

    renderPaginationControls();
}

function renderPaginationControls() {
    let controls = document.getElementById('pagination-controls');

    if (!controls) {
        controls = document.createElement('div');
        
        controls.id = 'pagination-controls';
        controls.style.marginTop = '1rem';
        controls.style.display = 'flex';
        controls.style.justifyContent = 'center';
        controls.style.gap = '10px';
        document.querySelector('.family-container').appendChild(controls);
    }

    controls.innerHTML = '';

    if (prevPage) {
        const prevBtn = document.createElement('button');
        prevBtn.textContent = 'Previous';
        prevBtn.className='pagination-btn'
        prevBtn.onclick = () => loadFamilyMembers(prevPage);
        controls.appendChild(prevBtn);
    }

    if (nextPage) {
        const nextBtn = document.createElement('button');
        nextBtn.textContent = 'Next';
        nextBtn.className='pagination-btn'
        nextBtn.onclick = () => loadFamilyMembers(nextPage);
        controls.appendChild(nextBtn);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    loadFamilyMembers();
});

document.addEventListener('click', function (e) {
    const deleteBtn = e.target.closest('.delete-btn');
    if (deleteBtn) {
        const memberId = deleteBtn.getAttribute('data-member-id');
        const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

        if (confirm("Are you sure you want to delete this member?")) {
            fetch(`/delete-family-member/${memberId}/`, {
                method: 'DELETE',
                headers: {
                    "Content-Type": "application/json",
                    'X-CSRFToken': csrfToken
                }
            })
                .then(res => res.json())
                .then(data => {
                    if (data.message) {
                        document.querySelector(`.family-row[data-member-id="${memberId}"]`).remove();
                        alert('Family member removed successfully');
                    } else {
                        alert('Error removing the member');
                    }
                })
                .catch(err => {
                    console.error("Failed to delete member", err);
                    alert("An error occurred.");
                });
        }
        return;
    }

    const editBtn = e.target.closest('.edit-btn');
    if (editBtn) {
        const memberId = editBtn.getAttribute('data-member-id');
        if (!memberId) {
            alert('Member ID not found!');
            return;
        }
        window.location.href = `/edit_family_member/${memberId}/`;
    }

    const recordBtn = e.target.closest('.record-btn');
    if (recordBtn) {
        const memberId = recordBtn.getAttribute('data-user-id');
        
        if (!memberId) {
            alert('Member ID not found!');
            return;
        }
        window.location.href = `/medical_records/${memberId}/`;
    }
});

   

