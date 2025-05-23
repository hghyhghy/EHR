

 document.addEventListener("DOMContentLoaded", ()=> {

    const form   =  document.getElementById('login-form')
    form.addEventListener("submit", async (e) => {
        e.preventDefault()

        const email  =  document.getElementById('email').value.trim()
        const  password =  document.getElementById('password').value.trim()

        try {
            
            const response =  await  fetch('/api/doctor-login/' , {
                method:"POST",
                headers: {
                    'Content-Type': 'application/json',
                },
                body:JSON.stringify({email,password})
            });

            const data  =  await  response.json()
            if (response.ok){
                localStorage.setItem('access', data.access);
                localStorage.setItem('refresh', data.refresh);
                window.location.href="/doctor_profile/"
            } else{
                alert('Login failed, Invalid credentials ')
            }
        } catch (error) {
            alert('Error while login')
            console.log(error)
        }
    })
})