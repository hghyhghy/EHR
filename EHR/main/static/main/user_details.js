document.addEventListener('DOMContentLoaded', async () => {
    const token = localStorage.getItem('access');

    const response = await fetch('/api/user-details/', {
        method: 'GET',
        headers: {
            "Authorization": `Bearer ${token}`,
            "Accept": "application/json"
        }
    });

    const data = await response.json();

    // Render user profile
    const profile = data.profile;
    document.getElementById('user-username').textContent = profile.username;
    // Add more fields if needed...

    // Render family members in flex layout
    const familyBody = document.getElementById('family-body');
    familyBody.innerHTML = ''; // clear placeholder

    data.family.forEach((member,index) => {
        const row = document.createElement('div');
        row.className = 'family-row';
        row.setAttribute('data-member-id', member.id); // useful for deletion

        row.innerHTML = `
            <div class="family-cell">${index + 1}</div> 
            <div class="family-cell">${member.username}</div>
            <div class="family-cell">${member.email}</div>
            <div class="family-cell" style="margin-left:3rem">${member.dob || '-'}</div>
            <div class="family-cell" style="margin-left:2rem">${member.gender || '-'}</div>
            <div class="family-cell">
                <div class="button-group">
                    <button class="delete-btn" data-member-id="${member.id}">Delete</button>
                    <button class="edit-btn" data-member-id="${member.id}">Edit</button>
                </div>
            </div>

        `;

        familyBody.appendChild(row);
    });
});

document.addEventListener('click', function (e) {
    if (e.target.classList.contains('delete-btn')) {
        const memberId = e.target.getAttribute('data-member-id');
        if (confirm("Are you sure you want to delete this member?")) {
            fetch(`/delete-family-member/${memberId}/`, {
                method: 'DELETE',
                headers: {
                    "Authorization": `Bearer ${localStorage.getItem("access")}`,
                    "Content-Type": "application/json"
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
    }

    if (e.target.classList.contains('edit-btn')){
        const memberId =  e.target.getAttribute('data-member-id')
        window.location.href = `/edit_family_member/${memberId}`
    }
});
