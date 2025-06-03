
document.addEventListener('DOMContentLoaded', ()=> {

    const logoutBtn  =  document.getElementById("logout-btn")
    if (logoutBtn){
            logoutBtn.addEventListener('click',handleLogOut)
    }

    async  function handleLogOut(event){

        event.preventDefault()
        const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

        const response =  await  fetch('/api/logout/',{
            method:'POST',
            headers:{
                            "Content-Type": "application/json",
            'X-CSRFToken': csrfToken
            },
            credentials:"include"
        });


        const data  =  await  response.json()
        if (response.ok){
                    window.location.href = "/login/"; // or redirect to login page

        } else{
            alert('Error logging out for the user ')
        }


    }
})