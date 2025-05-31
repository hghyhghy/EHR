
document.addEventListener('DOMContentLoaded',()=> {

    const  appointFrom   =  document.getElementById('appointmentForm')
    if (appointFrom){
        appointFrom.addEventListener('submit',handleBookAppointment)
    }




async  function handleBookAppointment(event){

    event.preventDefault()
    const form =  event.target
    const formdata  =  new FormData(form)


        const pathUrls = window.location.pathname.split("/").filter(part => part); 
        const doctorId = pathUrls[pathUrls.length - 1];
        if (!doctorId){
            alert('Doctor id is not found')
        }

        const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

        const url = `/api/request-appointment/${doctorId}/`;
        try {
            const response  =  await  fetch(url,{
                method:'POST',
                body:formdata,
                headers:{
                    'X-CSRFToken': csrfToken
                }
            })

            const data  =  await  response.json()
            const messageDiv  =  document.getElementById('responseMessage')
            if (response.ok){
                messageDiv.style.color = 'green';
                messageDiv.textContent = data.message;
                form.reset()
            } else{
                messageDiv.style.color = 'red';
                messageDiv.textContent = data.message || 'Failed to book appointment';
            }
        } catch (error) {
            
            console.log('Error  Booking  the appointment with the doctor ');
            const messageDiv = document.getElementById('responseMessage');
            messageDiv.style.color = 'red';
            messageDiv.textContent = 'Something went wrong. Please try again later.';
            
        }
}
    




})