console.log("🔥 MAIN.JS LOADED");

let allDoctors = [];

// ------------------ Helpers ------------------
const qs = (id) => document.getElementById(id);

const mobileMenuBtn = qs("mobile-menu-btn");
const navLinks = document.querySelector(".nav-links");

mobileMenuBtn?.addEventListener("click", () => {
  navLinks?.classList.toggle("show");
});

document.querySelectorAll(".nav-links a").forEach((link) => {
  link.addEventListener("click", () => {
    navLinks?.classList.remove("show");
  });
});

const token = () => localStorage.getItem("access");
const authHeader = () => {
  const t = token();
  return t ? { Authorization: `Bearer ${t}` } : {};
};

// =====================================================
// LOGIN
// =====================================================
qs("login-form")?.addEventListener("submit", async (e) => {
  e.preventDefault();

  const username = qs("username").value.trim();
  const password = qs("password").value.trim();

  const res = await fetch("/api/token/", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password }),
  });

  const data = await res.json();

  if (data.access) {
    localStorage.setItem("access", data.access);
    localStorage.setItem("username", username);
    updateNavUser();
    window.location.href = "/";
  } else {
    qs("login-feedback").innerText = "❌ Invalid username or password";
  }
});

// =====================================================
// SIGNUP
// =====================================================
qs("signup-form")?.addEventListener("submit", async (e) => {
  e.preventDefault();

  const username = qs("su-username").value;
  const email = qs("su-email").value;
  const password = qs("su-password").value;
  const roleField = qs("role");
  const role = roleField ? roleField.value : "patient";

  const res = await fetch("/api/register/", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, email, password, role }),
  });

  if (!res.ok) {
    const err = await res.json();
    qs("signup-feedback").innerText = "❌ " + (err.error || "Signup failed");
    return;
  }

  const loginRes = await fetch("/api/token/", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password }),
  });

  const loginData = await loginRes.json();

  if (loginData.access) {
    localStorage.setItem("access", loginData.access);
    localStorage.setItem("username", username);
    updateNavUser();
    window.location.href = "/";
  } else {
    window.location.href = "/login/";
  }
});

// =====================================================
// NAVBAR
// =====================================================
function updateNavUser() {
  const user = localStorage.getItem("username");
  const userSpan = qs("nav-username");
  const loginLink = qs("nav-login-link");
  const logoutLink = qs("nav-logout-link");

  if (!userSpan || !loginLink || !logoutLink) return;

  if (user) {
    userSpan.textContent = `Hi, ${user} 👋`;
    userSpan.style.display = "inline-block";
    logoutLink.style.display = "inline-block";
    loginLink.style.display = "none";
  } else {
    userSpan.textContent = "";
    userSpan.style.display = "none";
    logoutLink.style.display = "none";
    loginLink.style.display = "inline-block";
  }
}

updateNavUser();

// LOGOUT
window.logout = () => {
  localStorage.removeItem("access");
  localStorage.removeItem("username");
  updateNavUser();
  window.location.href = "/login/";
};

// =====================================================
// LOAD DOCTORS
// =====================================================
async function loadDoctors(listId = "doctors-list", dropdownId = "doctor-select") {
  const container = qs(listId);
  if (!container) return;

  const res = await fetch("/api/doctors/");
  allDoctors = await res.json();

  populateSpecializations(allDoctors);
  renderDoctors(allDoctors, listId);

  const dropdown = qs(dropdownId);
  if (dropdown) {
    dropdown.innerHTML = "";

    allDoctors.forEach((doc) => {
      const opt = document.createElement("option");
      opt.value = doc.user.id;
      opt.innerText = `Dr. ${doc.user.username} (${doc.specialization})`;
      dropdown.appendChild(opt);
    });
  }
}

// =====================================================
// RENDER DOCTORS
// =====================================================
function renderDoctors(doctors, listId) {
  const container = qs(listId);
  if (!container) return;

  container.innerHTML = "";

  doctors.forEach((doc) => {
    const card = document.createElement("div");
    card.className = "doctor-card";

    card.innerHTML = `
      <img src="/static/core/img/doctorprofile.png" class="doc-img">

      <h3>Dr. ${doc.user.username}</h3>

      <p class="muted">Specialization: ${doc.specialization}</p>

      <p class="muted">Experience: ${doc.experience_years} years</p>

      <p class="muted">
        🕒 Available: ${doc.available_from.slice(0, 5)} - ${doc.available_to.slice(0, 5)}
      </p>

      ${doc.bio ? `<p class="muted">${doc.bio}</p>` : ""}

      ${
        token()
          ? `<button class="btn open-booking" data-id="${doc.user.id}">Book Appointment</button>`
          : `<a href="/login/" class="btn">Login to Book</a>`
      }
    `;

    container.appendChild(card);
  });

  activateBookingButtons();
}

// =====================================================
// POPULATE SPECIALIZATION DROPDOWN
// =====================================================
function populateSpecializations(doctors) {
  const select = qs("filter-special");
  if (!select) return;

  const specs = [...new Set(doctors.map((d) => d.specialization))];

  select.innerHTML = `<option value="">All Specializations</option>`;

  specs.forEach((spec) => {
    const option = document.createElement("option");
    option.value = spec.toLowerCase();
    option.textContent = spec;
    select.appendChild(option);
  });
}

// =====================================================
// SEARCH + FILTER
// =====================================================
const searchInput = qs("search-doctor");
const specializationFilter = qs("filter-special");

function applyFilters() {
  let filtered = [...allDoctors];

  const searchValue = searchInput?.value.toLowerCase() || "";
  const specValue = specializationFilter?.value.toLowerCase() || "";

  if (searchValue) {
    filtered = filtered.filter(
      (doc) =>
        doc.user.username.toLowerCase().includes(searchValue) ||
        doc.specialization.toLowerCase().includes(searchValue)
    );
  }

  if (specValue) {
    filtered = filtered.filter(
      (doc) => doc.specialization.toLowerCase() === specValue
    );
  }

  renderDoctors(filtered, "doctors-list-full");
}

searchInput?.addEventListener("input", applyFilters);
specializationFilter?.addEventListener("change", applyFilters);

// =====================================================
// BOOKING MODAL
// =====================================================
const modal = qs("booking-modal");
const modalClose = qs("modal-close");
const bookingForm = qs("booking-form");

function activateBookingButtons() {
  document.querySelectorAll(".open-booking").forEach((btn) => {
    btn.addEventListener("click", () => {
      if (!token()) {
        window.location.href = "/login/";
        return;
      }

      modal?.classList.remove("hidden");

      qs("doctor-id-hidden").value = btn.dataset.id;
      qs("doctor-select").value = btn.dataset.id;
      qs("booking-feedback").innerText = "";
    });
  });
}

modalClose?.addEventListener("click", () => modal?.classList.add("hidden"));
modal?.addEventListener("click", (e) => {
  if (e.target === modal) modal.classList.add("hidden");
});

// =====================================================
// BOOKING SUBMIT
// =====================================================
bookingForm?.addEventListener("submit", async (e) => {
  e.preventDefault();

  const doctor_id = parseInt(qs("doctor-id-hidden").value, 10);
  let date = qs("appt-date").value;
  const time = qs("appt-time").value;
  const feedback = qs("booking-feedback");

  if (!doctor_id || !date || !time) {
    feedback.innerText = "❌ Please fill all fields.";
    return;
  }

  if (/^\d{2}-\d{2}-\d{4}$/.test(date)) {
    const [dd, mm, yyyy] = date.split("-");
    date = `${yyyy}-${mm}-${dd}`;
  }

  const res = await fetch("/api/appointments/book/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      ...authHeader(),
    },
    body: JSON.stringify({ doctor_id, date, time }),
  });

  if (res.ok) {
    feedback.innerText = "✅ Appointment booked!";
    setTimeout(() => modal?.classList.add("hidden"), 1200);
  } else {
    const err = await res.json().catch(() => ({}));
    feedback.innerText =
      "❌ Booking failed: " +
      (err.detail || err.error || JSON.stringify(err) || "Unknown error");
  }
});

// =====================================================
// APPOINTMENTS LIST
// =====================================================
async function loadAppointments() {
  const container = qs("appointments-list");
  if (!container) return;

  const res = await fetch("/api/appointments/", {
    headers: authHeader(),
  });

  if (!res.ok) {
    container.innerHTML = `<p class="muted">Please login to view appointments.</p>`;
    return;
  }

  const appointments = await res.json();
  container.innerHTML = "";

  appointments.forEach((ap) => {
    const card = document.createElement("div");
    card.className = "doctor-card";

    let statusHtml = "";
    let actionHtml = "";

    if (ap.status === "pending") {
      statusHtml = `<p class="muted">Status: Pending</p>`;
      actionHtml = `<button class="btn cancel" onclick="cancelAppt(${ap.id})">Cancel</button>`;
    } else if (ap.status === "completed") {
      statusHtml = `<p class="muted">Status: Completed</p>`;
    } else if (ap.status === "cancelled") {
      statusHtml = `<p class="muted">Status: Cancelled</p>`;
    } else {
      statusHtml = `<p class="muted">Status: ${ap.status}</p>`;
    }

    card.innerHTML = `
      <h3>Dr. ${ap.doctor?.user?.username}</h3>
      <p class="muted">${ap.doctor?.specialization}</p>
      <p>Date: ${ap.date}</p>
      <p>Time: ${ap.time}</p>
      ${statusHtml}
      ${actionHtml}
    `;

    container.appendChild(card);
  });
}

window.cancelAppt = async (id) => {
  await fetch(`/api/appointments/${id}/cancel/`, {
    method: "POST",
    headers: authHeader(),
  });

  location.reload();
};

// =====================================================
// PAGE ROUTER
// =====================================================
const path = window.location.pathname;

if (path === "/") loadDoctors("doctors-list", "doctor-select");
if (path.startsWith("/doctors")) loadDoctors("doctors-list-full", "doctor-select");
if (path.startsWith("/appointments")) loadAppointments();