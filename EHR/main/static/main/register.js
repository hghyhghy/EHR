
async function handeRegister(event) {

    event.preventDefault()
    const data = {

        username:document.getElementById('username').value(),
        email:document.getElementById('email').value(),
        dob:document.getElementById('dob').value(),
        password:document.getElementById('password').value(),
        gender:document.getElementById('gender').value(),
        phone_number:document.getElementById('phone_number').value(),
    }

    const response  =  await  fetch("/api/register/",
        {
            method:"POST",
            headers:{
                "Content-Type": "application/json"
            },
            body:JSON.stringify(data)

        }
    )

    const result =  await response.json()
    if (response.ok){
        alert('Registration successful')
        window.location.href =  "/login/"

    } else{
        alert('Registartion unseccessful'+JSON.stringify(result))

    }
    
}