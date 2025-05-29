console.log("Edit member JS loaded");

document.addEventListener('DOMContentLoaded',function(){


    const pathUrls = window.location.pathname.split("/")
    const member_id =  pathUrls[pathUrls.length -2]

    if (!member_id){
        alert('No member id is found')
        return
    }
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

    // const token  =  localStorage.getItem('access')
    const form  =  document.getElementById("edit_family_member_form")
    fetch(`/api/get-family-details/${member_id}`,{
        method:'GET',
        headers:{
                        'X-CSRFToken': csrfToken

        }
    })
    .then(response =>  response.json())
    .then(data =>  {
        const profile =  data.profile
        if (profile &&  profile.username){
            document.getElementById('username').value =  profile.username;
            document.getElementById('email').value =  profile.email;
            document.getElementById('gender').value =  profile.gender;
            document.getElementById('dob').value =  profile.dob;
            // document.getElementById('password').value =  profile.password;
            document.getElementById('phone_number').value =  profile.phone_number;

            document.getElementById("name_to_show").textContent =  profile.username
            document.getElementById("name_to_show").style.color ="blue"

        } else{
            alert('Failed to get the user details ')
        }
    })
    .catch(err =>  console.log('error loading details ',err))

    form.addEventListener("submit", function(event){
            event.preventDefault()
            const updatedData={
                username:document.getElementById('username').value,
                email:document.getElementById('email').value,
                gender:document.getElementById('gender').value,
                dob:document.getElementById('dob').value,
                password:document.getElementById('password').value,
                phone_number:document.getElementById('phone_number').value,

            };
            console.log(updatedData.password);
            
            fetch(`/api/edit_family_member/${member_id}/`,{
                method:'PUT',
                headers:{
                "Content-Type": "application/json",
                'X-CSRFToken': csrfToken
                },
                body:JSON.stringify(updatedData)
            }).then(res =>  {
                if (res.ok){
                    window.location.href = "/user_details/"
                } else{
                    alert("Error updating the details")
                }
            }).catch(err =>  console.log('Error editing the family member',err)) 
        
    })
})