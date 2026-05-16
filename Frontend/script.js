const API_URL = "http://localhost:5000";


// LOGIN
async function login() {

  const username =
    document.getElementById("username").value;

  const password =
    document.getElementById("password").value;

  const response = await fetch(
    `${API_URL}/login`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        username,
        password
      })
    }
  );

  const data = await response.json();

  console.log(data);

  if (data.success) {

    alert("Login Successful");

    localStorage.setItem(
      "user",
      JSON.stringify(data.user)
    );

    window.location.href = "chat.html";

  } else {
    alert(data.message);
  }
}


// SIGNUP
async function signup() {

  const username =
    document.getElementById("signupUsername").value;

  const password =
    document.getElementById("signupPassword").value;

  const nativeLanguage =
    document.getElementById("nativeLanguage").value;

  const learningLanguage =
    document.getElementById("learningLanguage").value;

  const response = await fetch(
    `${API_URL}/signup`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        username,
        password,
        nativeLanguage,
        learningLanguage
      })
    }
  );

  const data = await response.json();

  console.log(data);

  if (data.success) {

    alert("Signup Successful");

    window.location.href = "login.html";

  } else {
    alert(data.message);
  }
}