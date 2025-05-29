
document.addEventListener('DOMContentLoaded',()=>{

    const logoutBtn =  document.getElementById('logout-btn')
    if  (logoutBtn){
        logoutBtn.addEventListener('click',handleDoctorLogout)
    }

    async  function  handleDoctorLogout(event){
        event.preventDefault()
        const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

        const response  =  await  fetch('/api/doctor-logout/',{
            
            method:'POST',
            headers:{
            "Content-Type": "application/json",
            'X-CSRFToken': csrfToken
            },
            credentials:"include"
        });

        const result  =  await  response.json()
        if (response.ok){
            window.location.href = '/'
        } else{
            alert('Error logouting the doctor')
        }
    }
})