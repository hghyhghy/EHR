

document.addEventListener("DOMContentLoaded",function(){

    const otpform =   document.getElementById('otp-form')
    if (otpform){
        otpform.addEventListener('submit',handleOTP)
    }
})

async  function handleOTP(event){

    event.preventDefault()

    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    const user_id  =  document.getElementById('otp-user-id').value
    const otp =  document.getElementById('otp-input').value

    const response  =  await  fetch("/api/verify-otp/",{
        method:"POST",
        headers:{
            "Content-Type": "application/json",
            'X-CSRFToken': csrfToken
        },

        body:JSON.stringify({user_id:user_id,otp:otp})
    });

    const data  = await  response.json()
    if (response.ok) {
        
        localStorage.setItem('access', data.access);
        localStorage.setItem('refresh', data.refresh);
        window.location.href = "/user_details/";
    } else {
        alert("OTP verification failed: " + (data.detail || JSON.stringify(data)));
    }
}