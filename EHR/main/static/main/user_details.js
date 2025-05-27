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
    const profile1  = data.family
    if (data.profile){

        document.getElementById('user-username').textContent = profile.username  
    }  else if(data.family){
        document.getElementById('user-username').textContent =  profile1.username;

    }
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
            <div class="family-cell" style="margin-left:2rem">${member.dob || '-'}</div>
            <div class="family-cell">${member.gender || '-'}</div>
            <div class="family-cell">
                <div class="button-group">
                    <i class='bx  bx-trash delete-btn' role = 'button' tabindex="0" data-member-id="${member.id}"></i>
                    <i class='bx  bx-edit edit-btn' role = 'button' tabindex="0" data-member-id="${member.id}"></i>
                </div>
            </div>

        `;

        familyBody.appendChild(row);
    });
    // end
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
