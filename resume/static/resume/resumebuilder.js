let lastKnownScroll = 0;
let ticking = false;
const navbar = document.querySelector('.navbar');
const navbarHeight = navbar.offsetHeight;

function updateSidebar(scrollPos) {
    const sidebar = document.getElementById('sidebar');
    
    // Calculate the difference between navbar height and scroll position
    const difference = Math.max(0, navbarHeight - scrollPos);
    
    sidebar.style.position = 'fixed';
    sidebar.style.top = `${difference}px`;
    sidebar.style.height = `calc(100vh - ${difference}px)`;
    sidebar.style.transform = 'translateZ(0)';
    
    ticking = false;
}

window.addEventListener('scroll', function() {
    lastKnownScroll = window.scrollY;

    if (!ticking) {
        window.requestAnimationFrame(function() {
            updateSidebar(lastKnownScroll);
        });
        ticking = true;
    }
});

// Update on page load
document.addEventListener('DOMContentLoaded', function() {
    updateSidebar(window.scrollY);
});

// Update on resize
let resizeTimeout;
window.addEventListener('resize', function() {
    clearTimeout(resizeTimeout);
    resizeTimeout = setTimeout(function() {
        updateSidebar(window.scrollY);
    }, 66); // Debounce resize events
});

function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    sidebar.classList.toggle('active');
}

function showSection(sectionId) {
    document.querySelectorAll('.nav-link').forEach(link => link.classList.remove('active'));
    document.querySelector(`[href="#${sectionId}"]`).classList.add('active');
    
    const section = document.getElementById(sectionId);
    section.scrollIntoView({ behavior: 'smooth' });

    // Close sidebar on mobile after selection
    if (window.innerWidth <= 768) {
        toggleSidebar();
    }
}

// Add mobile toggle button to navbar
document.addEventListener('DOMContentLoaded', function() {
    if (window.innerWidth <= 768) {
        const navbar = document.querySelector('.navbar-nav');
        const toggleButton = document.createElement('button');
        toggleButton.className = 'btn btn-outline-light d-md-none ms-2';
        toggleButton.innerHTML = '<i class="fas fa-bars"></i>';
        toggleButton.onclick = toggleSidebar;
        navbar.prepend(toggleButton);
    }
});

// Add scroll behavior
window.addEventListener('scroll', function() {
    const sidebar = document.getElementById('sidebar');
    const scrollTop = window.scrollY;
    
    if (scrollTop > 56) {
        document.body.classList.add('scrolled');
    } else {
        document.body.classList.remove('scrolled');
        sidebar.style.top = (56 - scrollTop) + 'px';
    }
});

// Update the previewImage function in your JavaScript file
function previewImage(input) {
    const preview = document.getElementById('imagePreview');
    const placeholder = document.getElementById('previewPlaceholder');
    const container = document.querySelector('.image-preview-container');
    
    if (input.files && input.files[0]) {
        const reader = new FileReader();
        
        reader.onload = function(e) {
            preview.src = e.target.result;
            preview.classList.remove('d-none');
            placeholder.style.display = 'none';
            container.style.borderStyle = 'solid';
        }
        
        reader.readAsDataURL(input.files[0]);
    } else {
        preview.src = '#';
        preview.classList.add('d-none');
        placeholder.style.display = 'flex';
        container.style.borderStyle = 'dashed';
    }
}