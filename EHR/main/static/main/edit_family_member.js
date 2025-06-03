console.log("Edit member JS loaded");

document.addEventListener('DOMContentLoaded', function () {
    const pathUrls = window.location.pathname.split("/").filter(part => part);
    const member_id = pathUrls[pathUrls.length - 1];
    if (!member_id) {
        PNotify.error({ text: 'No member ID found.' });
        return;
    }

    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    const form = document.getElementById("edit_family_member_form");

    fetch(`/api/get-family-details/${member_id}/`, {
        method: 'GET',
        headers: {
            'X-CSRFToken': csrfToken
        }
    })
    .then(response => response.json())
    .then(data => {
        const profile = data.profile;
        if (profile && profile.username) {
            document.getElementById('username').value = profile.username;
            document.getElementById('email').value = profile.email;
            document.getElementById('gender').value = profile.gender;
            document.getElementById('dob').value = profile.dob;
            document.getElementById('phone_number').value = profile.phone_number;

            document.getElementById("name_to_show").textContent = profile.username;
            document.getElementById("name_to_show").style.color = "violet";

        } else {
            PNotify.error({ text: 'Failed to get user details.' });
        }
    })
    .catch(err => {
        console.error('Error loading details:', err);
        PNotify.error({ text: 'Error loading user details.' });
    });

    form.addEventListener("submit", function (event) {
        event.preventDefault();
        const updatedData = {
            username: document.getElementById('username').value,
            email: document.getElementById('email').value,
            gender: document.getElementById('gender').value,
            dob: document.getElementById('dob').value,
            password: document.getElementById('password').value,
            phone_number: document.getElementById('phone_number').value,
        };

        fetch(`/api/edit_family_member/${member_id}/`, {
            method: 'PUT',
            headers: {
                "Content-Type": "application/json",
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify(updatedData)
        }).then(res => {
            if (res.ok) {
                PNotify.success({ 
                    text: 'Details updated successfully!',
                    delay:3000,
                    styling: 'brighttheme' });
                
            } else {
                PNotify.error({ text: 'Error updating details.' });
            }
        }).catch(err => {
            console.error('Error editing the family member:', err);
            PNotify.error({ text: 'Failed to update family member.' });
        });
    });
});
