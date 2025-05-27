document.addEventListener('DOMContentLoaded', () => {

    const doctorBody  =  document.getElementById('doctor-body')
    const searchInput  =  document.getElementById('doctor-search-input')
    const searchButton  =  document.getElementById('doctor-search-btn')
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');


  
    function  renderDoctors(doctors){
        doctorBody.innerHTML = ""
        if (doctors.length  === 0){
            doctorBody.innerHTML = "<p>No doctors found for the selected category.</p>"
            return 
        }

        doctors.forEach(doctor => {
                const row   =  document.createElement('div')
                row.className = 'doctor-row'
                row.innerHTML = `
                                <div class="doctor-username">${doctor.username} ⚕️</div> 
                <div class="main-category-degree">
                    <div class="doctor-degree">${doctor.degree} In</div>
                    <div class="doctor-category">${doctor.category}</div>
                </div>
                <div class="doctor-phone_number"> <span>Contact At:</span> ${doctor.phone_number}</div>
                <button class="book-appointment-btn"  data-doctor-id  = ${doctor.id}>Request Appointment</button>
                `;
                doctorBody.appendChild(row)
        });

        const bookbuttons  =  document.querySelectorAll('.book-appointment-btn')
        bookbuttons.forEach(button => {
            button.addEventListener('click' , () => {
                const doctor_id  =  button.getAttribute('data-doctor-id')
                if (doctor_id){
                    window.location.href = `/book-appointment/${doctor_id}/`
                } else{
                    alert('Doctor id is not found')
                }
            })
        })
    }

    function  fetchDoctors(query = ""){
        const url =  query ? 
        `/api/search-doctors/?category=${encodeURIComponent(query)}`
        :
        `/api/all-doctors`;

        fetch(url , {
            method:'GET',
            headers:{
                  'X-CSRFToken': csrfToken
            }
        })
        .then(response => response.json())
        .then(renderDoctors)
        .catch(err =>  {
            alert('alert fetching/searching doctors')
            console.log(err);
            
        })
    }

    fetchDoctors()
    if (searchButton && searchInput){
        searchButton.addEventListener('click',() => {
            const query   =  searchInput.value.trim()
            fetchDoctors(query)
        })

        searchInput.addEventListener('input',() => {
            const query =  searchInput.value.trim()
            if (query === ""){
                fetchDoctors()
            }
        })
    }














































































    //   fetch('/api/all-doctors/',{
    //     method:'GET',
    //     headers:{
    //         'Authorization':`Bearer ${token}`
    //     }
    // })
    // .then(response  =>  response.json())
    // .then(data => {
        
    //     doctorBody.innerHTML = ""
    //     data.forEach((doctor,index) => {
            
    //         const  row  =  document.createElement('div')
    //         row.className='doctor-row'
    //         row.innerHTML = `
    //             <div class ="doctor-username">${doctor.username} ⚕️</div> 
    //             <div class= "main-category-degree">
    //                                 <div class ="doctor-degree">${doctor.degree} In</div>
    //                                 <div class ="doctor-category">${doctor.category}</div>
    //             </div>


    //             <div class ="doctor-phone_number"> <span>  Contact At : </span> ${doctor.phone_number}</div>

    //             <button class="book-appointment-btn">
    //                 Request Appointment
    //             </button>
    //         `

    //         doctorBody.appendChild(row)
    //     });
    // })
    // .catch(error => {
    //     alert('Error getting doctor details')
    //     console.log(error);
        
    // })
})