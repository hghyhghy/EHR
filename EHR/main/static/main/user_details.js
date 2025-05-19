
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
                <td>${member.username}</td>
                <td>${member.email}</td>
                <td>${member.dob}</td>
                <td>${member.gender}</td>
                <td>${member.phone_number}</td>
        `;
        tbody.appendChild(row)
    }); 
})