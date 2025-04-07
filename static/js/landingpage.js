// Create particles for background animation
const particlesContainer = document.getElementById('particles');
const particleCount = 110;

for (let i = 0; i < particleCount; i++) {
    const particle = document.createElement('div');
    particle.classList.add('particle');
    
    // Random size between 5px and 20px
    const size = Math.random() * 15 + 5;
    particle.style.width = `${size}px`;
    particle.style.height = `${size}px`;
    
    // Random position
    particle.style.left = `${Math.random() * 100}%`;
    particle.style.top = `${Math.random() * 100}%`;
    
    // Random opacity
    particle.style.opacity = Math.random() * 0.5 + 0.1;
    
    // Random animation duration
    const duration = Math.random() * 20 + 10;
    particle.style.animationDuration = `${duration}s`;
    
    // Random animation delay
    const delay = Math.random() * 0;
    particle.style.animationDelay = `${delay}s`;
    
    particlesContainer.appendChild(particle);
}

// Add hover effect to logo
const logo = document.querySelector('.logo');
logo.addEventListener('mouseover', () => {
    logo.style.transform = 'scale(1.05)';
    logo.style.transition = 'transform 0.3s ease';
});

logo.addEventListener('mouseout', () => {
    logo.style.transform = 'scale(1)';
});

// Add smooth scrolling behavior
document.addEventListener('DOMContentLoaded', function() {
    // Enable smooth scrolling for the whole page
    document.documentElement.style.scrollBehavior = 'smooth';
    
    // Always scroll to top on page refresh
    if (history.scrollRestoration) {
        history.scrollRestoration = 'manual';
    }
    window.scrollTo(0, 0);
    
    // Handle contact form submission
    const contactForm = document.querySelector('.contact-form');
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const email = this.querySelector('input[type="email"]').value;
            const message = this.querySelector('textarea').value;
            
            if (!email || !message) {
                alert('Please fill in all fields');
                return;
            }
            
            // Simulate form submission
            const submitBtn = this.querySelector('.send-btn');
            submitBtn.textContent = 'Sending...';
            submitBtn.disabled = true;
            
            // Simulate API call with timeout
            setTimeout(() => {
                alert('Thank you for your message! We will get back to you soon.');
                this.reset();
                submitBtn.textContent = 'Send';
                submitBtn.disabled = false;
            }, 1500);
        });
    }
    
    // Footer section animations on scroll
    const footerSections = document.querySelectorAll('.footer-section');
    
    function checkScroll() {
        footerSections.forEach(section => {
            const sectionTop = section.getBoundingClientRect().top;
            const screenPosition = window.innerHeight / 1.2;
            
            if (sectionTop < screenPosition) {
                section.style.opacity = '1';
                section.style.transform = 'translateY(0)';
            }
        });
    }
    
    // Initial check
    checkScroll();
    
    // Check on scroll
    window.addEventListener('scroll', checkScroll);
});

// Force scroll to top on page refresh
window.onbeforeunload = function() {
    window.scrollTo(0, 0);
};
