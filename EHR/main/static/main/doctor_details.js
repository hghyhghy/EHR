document.addEventListener('DOMContentLoaded', () => {

    const doctorBody  =  document.getElementById('doctor-body')
    const searchInput  =  document.getElementById('doctor-search-input')
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
        `/api/search-doctors/?query=${encodeURIComponent(query)}`
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
    if (searchInput){
        let debounceTimeout  =  null
        searchInput.addEventListener('input',() => {
            const query   =  searchInput.value.trim()
            clearTimeout(debounceTimeout)
            debounceTimeout=setTimeout(() => {
                fetchDoctors(query)
            },100)
        })

        searchInput.addEventListener('input',() => {
            const query =  searchInput.value.trim()
            if (query === ""){
                fetchDoctors()
            }
        })
    }
})