
document.addEventListener('DOMContentLoaded', ()=> {

    const token  =  localStorage.getItem('access')
    const tbody =  document.getElementById('appointments-body')

    fetch('/api/doctor-appointments/', {
        method:'GET',
        headers:{
                        'Authorization': `Bearer ${token}`,

        }
    })  
    .then(response => response.json())
    .then(data =>  {
        if (data.length  === 0){
            tbody.innerHTML = '<tr><td colspan="8">No appointments found.</td></tr>';;
            return
        }

        data.forEach((app,index) => {
                const doctor_name  =  document.getElementById('doctor-name')
                doctor_name.textContent =  app.Appointed_doctor
                const doctor_degree  =  document.getElementById('doctor-degree')
                doctor_degree.textContent =  app.Degree               
                const doctor_category  =  document.getElementById('doctor-category')
                doctor_category.textContent =  app.category
                const row  =  document.createElement('tr')
                row.innerHTML =  `
                <td>${app.name}</td>
                <td>${app.dob}</td>
                <td>${app.gender === 'M' ? 'Male' : app.gender === 'F' ? 'Female' : 'Other'}</td>
                <td>${app.phone_number}</td>
                <td>${new Date(app.scheduled_on).toLocaleString()}</td>
                <td>${app.venue}</td>
                <td><span class="status status-pending">Pending</span></td>
                    <td>
                        <div class="action-buttons">
                            <button class="btn btn-approve" onclick="handleAction(${index}, 'approve')">Approve</button>
                            <button class="btn btn-reject" onclick="handleAction(${index}, 'reject')">Reject</button>
                        </div>
                    </td>

                
                `;

                tbody.appendChild(row)
        })
    })
    .catch(error => {
        alert('error getting listed appointment')
        console.log(error);
        
    })
})