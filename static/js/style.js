document.addEventListener("DOMContentLoaded", () => {
    const sidebar = document.getElementById("sidebar");
    const sidebarToggle = document.getElementById("sidebarToggle");
    const sidebarClose = document.getElementById("sidebarClose");

    // Toggle Sidebar
    sidebarToggle.addEventListener("click", () => {
        sidebar.classList.add("open");
        document.body.insertAdjacentHTML(
            "beforeend",
            '<div class="sidebar-overlay active" id="sidebarOverlay"></div>'
        );
    });

    // Close Sidebar
    sidebarClose.addEventListener("click", closeSidebar);
    document.body.addEventListener("click", (event) => {
        if (event.target.classList.contains("sidebar-overlay")) {
            closeSidebar();
        }
    });

    function closeSidebar() {
        sidebar.classList.remove("open");
        const overlay = document.getElementById("sidebarOverlay");
        if (overlay) overlay.remove();
    }
});



const navbar = document.getElementById('navbar');
window.addEventListener('scroll', () => {
    if (window.scrollY > 50) {
        navbar.classList.add('navbar-scroll');
        navbar.classList.remove('bg-transparent');
    } else {
        navbar.classList.remove('navbar-scroll');
        navbar.classList.add('bg-transparent');
    }
});

// Animation on scroll
AOS.init({
    duration: 1200, // Animation duration
    once: true // Whether animation should happen only once while scrolling
});

function countdown() {
    const eventDate = new Date('2024-12-30T20:00:00').getTime(); // Set your event date
    const now = new Date().getTime();
    const timeLeft = eventDate - now;

    const days = Math.floor(timeLeft / (1000 * 60 * 60 * 24));
    const hours = Math.floor((timeLeft % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    const minutes = Math.floor((timeLeft % (1000 * 60 * 60)) / (1000 * 60));
    const seconds = Math.floor((timeLeft % (1000 * 60)) / 1000);

    document.getElementById('days').innerHTML = days < 10 ? '0' + days : days;
    document.getElementById('hours').innerHTML = hours < 10 ? '0' + hours : hours;
    document.getElementById('minutes').innerHTML = minutes < 10 ? '0' + minutes : minutes;
    document.getElementById('seconds').innerHTML = seconds < 10 ? '0' + seconds : seconds;

    if (timeLeft < 0) {
        clearInterval(timerInterval);
        document.getElementById('countdown').innerHTML = '<h2>Event Started!</h2>';
    }
}

const timerInterval = setInterval(countdown, 1000);

// Scroll-to-Top Button Logic
const scrollToTopBtn = document.getElementById("scrollToTopBtn");

// Show button when scrolling down
window.addEventListener("scroll", () => {
    if (window.scrollY > 200) {
        scrollToTopBtn.style.display = "flex";
    } else {
        scrollToTopBtn.style.display = "none";
    }
});

// Scroll to top when button is clicked
scrollToTopBtn.addEventListener("click", () => {
    window.scrollTo({
        top: 0,
        behavior: "smooth",
    });
});

// JavaScript to simulate live score updates
const scoreList = document.getElementById('score-list');
const notification = document.getElementById('notification');
let overs = 18.4;

setInterval(() => {
    overs += 0.1;
    if (overs >= 20) {
        overs = 20.0;
        scoreList.innerHTML = `
            <li><strong>Team A:</strong> 175/7 (20 overs)</li>
            <li><strong>Team B:</strong> 50/2 (7 overs)</li>
            <li><strong>Match Status:</strong> Team B chasing</li>
        `;
        notification.innerText = "Live updates finished.";
        return;
    }

    scoreList.innerHTML = `
        <li><strong>Team A:</strong> ${Math.floor(150 + (overs - 18.4) * 10)}/5 (${overs.toFixed(1)} overs)</li>
        <li><strong>Team B:</strong> Yet to bat</li>
        <li><strong>Match Status:</strong> Team A batting</li>
    `;
}, 3000);

// scroll
// Smooth scrolling for anchor links
document.querySelectorAll('a[href^="#about"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();

        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});

// services list
const servicesContainer = document.querySelector('.services-container');
const navPrev = document.querySelector('.nav-prev');
const navNext = document.querySelector('.nav-next');
let scrollPosition = 0;
const scrollAmount = 240; // width of the card + margin

navNext.addEventListener('click', () => {
    scrollPosition += scrollAmount;
    animateScroll();
});

navPrev.addEventListener('click', () => {
    scrollPosition -= scrollAmount;
    animateScroll();
});

function animateScroll() {
    servicesContainer.style.transition = "transform 0.3s ease-in-out";
    servicesContainer.style.transform = `translateX(-${scrollPosition}px)`;

    if (scrollPosition >= servicesContainer.scrollWidth / 2) {
        scrollPosition = 0;
        servicesContainer.style.transition = "none";
        servicesContainer.style.transform = `translateX(0px)`;
    }
}