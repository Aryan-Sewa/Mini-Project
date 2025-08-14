document.querySelectorAll(".donate-btn").forEach(button => {
    button.addEventListener("click", function () {
        const authLink = document.getElementById("auth-link");

        if (authLink) {
            window.location.href = "/signin";
        } else {
            window.location.href = "/user";
        }
    });
});
