console.log("add_family.js loaded");

document.addEventListener("DOMContentLoaded",function(){
    const form  =  document.getElementById("add_family_member")
    if (form){
        form.addEventListener('submit',handleAddFamilyMember)
    }
})


const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

console.log("Sending token:", token);

async function  handleAddFamilyMember(event) {
    
    event.preventDefault()
    const data = {
        username:document.getElementById('username').value,
        email:document.getElementById('email').value,
        gender:document.getElementById('gender').value,
        password:document.getElementById('password').value,
        dob:document.getElementById('dob').value,
        phone_number:document.getElementById('phone_number').value,

    }

    try {
        
        const response =  await  fetch('/api/add-family-members/',{
            method:'POST',
            headers:{
                "Content-Type": "application/json",
                'X-CSRFToken': csrfToken
            },
            body:JSON.stringify(data)
        });

        const  result =  await  response.json()
        if (response.ok){
            window.location.href= "/user_details/"
        } else{
            alert('Error adding  the family members ')
        }
    } catch (error) {
            console.error('Request failed',error)
            alert(error)
    }
}