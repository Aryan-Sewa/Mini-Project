fetch('/current_user')
  .then(res => res.json())
  .then(user => {
    if (user.name) {
      document.getElementById('auth-link').innerHTML = `
        <img src="${user.profile_pic}" alt="Profile" 
             style="width:30px; height:30px; border-radius:50%; margin-right:5px;">
        <span>${user.name}</span>
        <a href="/logout" style="margin-left:10px;">Logout</a>
      `;
    }
  });