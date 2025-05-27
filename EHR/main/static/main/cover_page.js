// Wait for DOM to be ready
document.addEventListener('DOMContentLoaded', function() {
    
    // Background image transition
    const images = document.querySelectorAll('.bg-image');
    let currentImage = 0;

    function changeBackground() {
        // Check if images exist and have length
        if (images.length === 0) {
            console.warn('No elements with class .bg-image found');
            return;
        }
        
        // Remove active class from current image (if it exists)
        if (images[currentImage]) {
            images[currentImage].classList.remove('active');
        }
        
        currentImage = (currentImage + 1) % images.length;
        
        // Add active class to new current image
        if (images[currentImage]) {
            images[currentImage].classList.add('active');
        }
    }

    // Only start interval if images exist
    if (images.length > 0) {
        // Set first image as active initially
        images[0].classList.add('active');
        setInterval(changeBackground, 5000);
    }

    // Welcome message and main content toggle
    const welcome = document.querySelector('.welcome');
    const mainContent = document.querySelector('.main-content');
    const heading = document.querySelector('.ehr-heading');

    // Check if elements exist before manipulating them
    if (welcome && mainContent && heading) {
        setTimeout(() => {
            welcome.classList.add('hidden');
            setTimeout(() => {
                heading.classList.add('active');
                mainContent.classList.add('active');
            }, 1000); // Delay to allow welcome fade-out
        }, 3000); // Welcome message visible for 3 seconds
    } else {
        console.warn('Some required elements not found:', {
            welcome: !!welcome,
            mainContent: !!mainContent,
            heading: !!heading
        });
    }

    // Typed.js initialization with safety check
    const quoteElement = document.querySelector('.quote');
    if (quoteElement && typeof Typed !== 'undefined') {
        var typed = new Typed(".quote", {
            strings: [
                'The greatest wealth is health." – Virgil',
                '"Your body is a temple, but only if you treat it as one." - Astrid Alauda.',
                '"It is health that is real wealth and not pieces of gold and silver."-Mahatma Gandhi.'
            ],
            typeSpeed: 100,
            backSpeed: 100,
            backDelay: 1000,
            loop: true
        });
    } else {
        if (!quoteElement) console.warn('Element with class .quote not found');
        if (typeof Typed === 'undefined') console.warn('Typed.js library not loaded');
    }
    
});