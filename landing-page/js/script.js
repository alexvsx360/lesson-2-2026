const form = document.getElementById("signupForm");
if (form) {
  form.addEventListener("submit", function (event) {
    event.preventDefault();
    const nameInput = document.getElementById("fullName");
    const emailInput = document.getElementById("email");
    const name = nameInput ? nameInput.value.trim() : "";
    const email = emailInput ? emailInput.value.trim() : "";
    if (!name || !email) {
      alert("נא למלא שם ואימייל — בהמשך נלמד לבדוק את זה בצורה מקצועית יותר.");
      return;
    }
    alert("תודה " + name + "! בשיעורי JavaScript נחבר שליחה אמיתית.");
  });
}
