document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("register-form");
    if (form) {
        form.addEventListener("submit", handleRegister);
    }
});

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

async function handleRegister(event) {
    event.preventDefault();

    const password = document.getElementById("password").value;

    // Updated password policy checks
    const lengthCheck = password.length >= 5;
    const uppercaseCheck = /[A-Z]/.test(password);
    const numberCheck = /\d/.test(password);
    const specialCharCheck = /[!@#$%^&*(),.?":{}|<>]/.test(password);

    if (!lengthCheck || !uppercaseCheck || !numberCheck || !specialCharCheck) {
        alert("Password must be at least 5 characters and include an uppercase letter, a number, and a special character.");
        return;
    }

    const data = {
        username: document.getElementById("username").value,
        email: document.getElementById("email").value,
        dob: document.getElementById("dob").value,
        password: password,
        gender: document.getElementById("gender").value,
        phone_number: document.getElementById("phone_number").value,
    };

    const response = await fetch("/api/register/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken
        },
        body: JSON.stringify(data)
    });

    const result = await response.json();
    if (response.ok) {
        window.location.href = "/";
    } else {
        alert("Registration unsuccessful: " + JSON.stringify(result));
    }
}
