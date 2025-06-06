

document.addEventListener('DOMContentLoaded',() => {
    const categorySelect  =  document.getElementById('category')

    function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === name + "=") {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrfToken = getCookie("csrftoken");


    fetch('/api/categories/', {
        method:"GET",

    })
    .then(res =>  res.json())
    .then(data =>  {
        data.forEach(category => {
            const option  =  document.createElement('option')
            option.value =  category.id
            option.textContent= category.name
            categorySelect.appendChild(option)
        });
    })
    .then(err =>  {
        console.log(err)
        alert('Error loading the category')
    })

    const form    = document.getElementById('doctor-register-form')
    form.addEventListener("submit", async(e) =>  {
        e.preventDefault()
        const formData= {
            username:document.getElementById('username').value,
            email:document.getElementById('email').value,
            gender:document.getElementById('gender').value,
            dob:document.getElementById('dob').value,
            degree:document.getElementById('degree').value,
            category:document.getElementById('category').value,
            password:document.getElementById('password').value,
            phone_number:document.getElementById('phone_number').value,

        };

        try {
            const response =  await  fetch(`/api/doctor-register/`, {
                method:"POST",
                headers: {
                    "Content-Type": "application/json",
                     "X-CSRFToken": csrfToken
                },
                body:JSON.stringify(formData)
            });
            console.log(formData)
            const result =  await  response.json()
            if (response.ok){
                window.location.href="/doctor_login/"
            } else{
                alert('Registration unsucessfult')
            }
        } catch (error) {
            console.error("Registration error:", err);
            alert("Something went wrong.");
        }
    })
}) 