
document.addEventListener('DOMContentLoaded', ()=> {

    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

    const tbody =  document.getElementById('appointments-body')

    fetch('/api/doctor-appointments/', {
        method:'GET',
        headers:{
            'X-CSRFToken': csrfToken

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
                const statusText = app.status === 1 ? "Accepted" : app.status === 2 ? "Rejected" : "Pending";
                const statusClass = app.status === 1 ? "status-accepted" : app.status === 2 ? "status-rejected" : "status-pending";
                const row  =  document.createElement('tr')
                row.innerHTML =  `
                <td>${app.name}</td>
                <td>${app.dob}</td>
                <td>${app.gender === 'M' ? 'Male' : app.gender === 'F' ? 'Female' : 'Other'}</td>
                <td>${app.phone_number}</td>
                <td>${new Date(app.scheduled_on).toLocaleString()}</td>
                <td>${app.venue}</td>
                    <td><span class="status ${statusClass}" id="status-${app.Application_id}">${statusText}</span></td>
                    <td>
                        <div class="action-buttons">
                            <button class="btn btn-approve" onclick="handleAction(${app.Application_id}, '1')">Approve</button>
                            <button class="btn btn-reject" onclick="handleAction(${app.Application_id}, '2')">Reject</button>
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

    window.handleAction =  function(id,action){
        const actiontext =  action === '1' ?  'approve':'reject'
        fetch(`/api/appointments/${id}/update-status/`,{
            method:'POST',
            headers:{
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body:JSON.stringify({status:action}),
            credentials:"same-origin"
        })
        .then(response => response.json())
        .then(result =>  {
            if(result.message){
                alert(result.message)
                const statusEl = document.getElementById(`status-${id}`);
                statusEl.textContent = action === '1' ? 'Accepted' : 'Rejected';
                statusEl.className = action === '1' ? 'status status-accepted' : 'status status-rejected';
            } else{
                alert(result.message ||  'something went wrong')
            }
        })
        .catch(err => {
            alert('Request failed.');
            console.log(err);
        })
    }
})