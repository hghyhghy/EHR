
document.addEventListener('DOMContentLoaded',async() =>  {
    const token  =  localStorage.getItem('access')

    const response =  await  fetch('/api/user-details/',{
        method:'GET',
        headers:{
                  "Authorization": `Bearer ${token}`,
         "Accept": "application/json"
        }
    });

    const data =  await  response.json()
    // rendering the profile page 

    const profile =  data.profile
    const profileCard =  document.getElementById('profile-card');
    profileCard.innerHTML =  
    `
    <div class="profile-card">

      <p><strong>Username:</strong> ${profile.username}</p>
      <p><strong>Email:</strong> ${profile.email}</p>
      <p><strong>DOB:</strong> ${profile.dob}</p>
      <p><strong>Gender:</strong> ${profile.gender}</p>
      <p><strong>Phone:</strong> ${profile.phone_number}</p>
    </div>
    `;

    document.getElementById('user-username').textContent = profile.username
    document.getElementById('user-email').textContent = profile.email


    // rendering the family table
    const tbody  = document.querySelector("#family-table tbody")
    data.family.forEach(member => {
        const row =  document.createElement('tr')
        row.innerHTML = `
        <td class="px-6 py-4">${member.username}</td>
        <td class="px-6 py-4">${member.email}</td>
        <td class="px-6 py-4">${member.dob || '-'}</td>
        <td class="px-6 py-4">${member.gender || '-'}</td>
        <td class="px-6 py-4">${member.phone_number || '-'}</td>
        <button class="delete-btn text-red-500 hover:underline" data-member-id = "${member.id}">
                    Delete 
        </button>
        `;
        tbody.appendChild(row)
    }); 
})

document.addEventListener('click', function(e){
    if (e.target.classList.contains('delete-btn')){
        const memberId =  e.target.getAttribute('data-member-id');
        if (confirm("Are you sure you want to delete this memeber")){
            fetch(`/delete-family-member/${memberId}/`, {
                method:'DELETE',
                headers:{
                    "Authorization": `Bearer ${localStorage.getItem("access")}`,
                    "Content-Type": "application/json"
                }
            })
            .then(res =>  res.json())
            .then(data =>  {
                if (data.message){
                    e.target.closest('tr').remove();
                    alert('Family member removed successfully')
                } else{
                    alert('Error removing the member')
                }
            })
            .catch(err =>  {
                console.error("Failed to delete member", err);
                alert("An error occurred.");
            })
        }
    }
})