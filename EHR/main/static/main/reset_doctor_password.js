document.addEventListener('DOMContentLoaded', function () {
    const verifyBtn = document.getElementById('verifyEmailBtn');
    const resetForm = document.getElementById('resetPasswordForm');
    const emailInput = document.getElementById('email');
    const passwordInput = document.getElementById('password');
    const passwordSection = document.getElementById('passwordSection');
    const messageDiv = document.getElementById('message');

    // Auto-fill email from URL
    const params = new URLSearchParams(window.location.search);
    const emailFromQuery = params.get('email');
    if (emailFromQuery) {
        emailInput.value = emailFromQuery;
        verifyEmail(emailFromQuery);
    }

    verifyBtn.addEventListener('click', function () {
        const email = emailInput.value;
        if (!email) {
            messageDiv.innerText = 'Please enter the email';
            return;
        }
        verifyEmail(email);
    });

function verifyEmail(email) {
    fetch('/api/verify-doctor-email/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: email })
    })
    .then(res => res.json())
    .then(data => {
        if (data.message == "Email verified. Proceed to reset.") {
            messageDiv.innerText = data.message;
            passwordInput.disabled = false;
            passwordSection.style.display = 'block';
        } else {
            messageDiv.innerText = 'Email verification failed';
            passwordInput.disabled = true;

        }
    })
    .catch(err => {
        messageDiv.innerText = 'Server error';
            passwordInput.disabled = true;

    });
}

    resetForm.addEventListener('submit', function (e) {
        e.preventDefault();
        const email = emailInput.value;
        const password = passwordInput.value;

        fetch('/api/reset-doctor-password/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email: email, password:password })
        })
        .then(res => res.json())
        .then(data => {
            if (data.message) {
                messageDiv.innerText = data.message;
                window.location.href= '/doctor_login/'
            } else {
                messageDiv.innerText = 'Error resetting the password';
            }
        })
        .catch(() => {
            messageDiv.innerText = "Internal error";
        });
    });
});
