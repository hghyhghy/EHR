document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("login-form");
    if (form) {
        form.addEventListener("submit", handleLogin);
    }

});

async function handleLogin(event) {
    event.preventDefault();
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');


    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const recaptchaToken = grecaptcha.getResponse();
    if (!recaptchaToken) {
        alert("Please complete the reCAPTCHA.");
        return;
    }

    const response = await fetch("/api/login/", {
        method: 'POST',
        headers: {
            "Content-Type": "application/json",
            'X-CSRFToken':csrfToken
        },
        body: JSON.stringify({ email, password,recaptcha: recaptchaToken})
    });

    const data = await response.json();
    if (response.ok) {

        document.getElementById('login-form').style.display = "none"
        document.getElementById('otp-form').style.display ='flex'
        document.getElementById("otp-user-id").value = data.user_id; 
        alert('opt has been sent  kindly check  your email')

    } else {
        alert('login failed: ' + JSON.stringify(data));
    }
}
