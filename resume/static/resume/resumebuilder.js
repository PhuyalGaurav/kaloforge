let lastKnownScroll = 0;
let ticking = false;
const navbar = document.querySelector('.navbar');
const navbarHeight = navbar.offsetHeight;

function updateSidebar(scrollPos) {
    const sidebar = document.getElementById('sidebar');
    
    // Mobile behavior
    if (window.innerWidth <= 768) {
        sidebar.style.position = 'fixed';
        sidebar.style.top = 'auto';
        sidebar.style.bottom = '0';
        sidebar.style.height = '85vh';
        return;
    }
    
    // Desktop behavior remains the same
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

// Add toggle functionality
function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    if (window.innerWidth <= 768) {
        if (sidebar.style.transform === 'translateY(0px)') {
            sidebar.style.transform = 'translateY(100%)';
            toggleBtn.classList.remove('active');
            overlay.classList.remove('active');
        } else {
            sidebar.style.transform = 'translateY(0)';
            toggleBtn.classList.add('active');
            overlay.classList.add('active');
        }
    } else {
        if (sidebar.style.transform === 'translateX(0px)') {
            sidebar.style.transform = 'translateX(-100%)';
            toggleBtn.classList.remove('active');
            overlay.classList.remove('active');
        } else {
            sidebar.style.transform = 'translateX(0)';
            toggleBtn.classList.add('active');
            overlay.classList.add('active');
        }
    }
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

// Close sidebar when clicking overlay
document.addEventListener('DOMContentLoaded', function() {
    const overlay = document.createElement('div');
    overlay.className = 'sidebar-overlay';
    document.body.appendChild(overlay);

    overlay.addEventListener('click', function() {
        toggleSidebar();
    });

    // Close sidebar when clicking nav links on mobile
    const navLinks = document.querySelectorAll('#sidebar .nav-link');
    navLinks.forEach(link => {
        link.addEventListener('click', function() {
            if (window.innerWidth <= 768) {
                toggleSidebar();
            }
        });
    });
});

// Update the previewImage function
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
document.addEventListener('DOMContentLoaded', function() {
    const sidebar = document.getElementById('sidebar');
    const toggleBtn = document.createElement('button');
    
    // Initialize toggle button
    toggleBtn.className = 'sidebar-toggle';
    toggleBtn.innerHTML = '<i class="fas fa-chevron-right"></i>';
    document.body.appendChild(toggleBtn);

    // Create overlay
    const overlay = document.createElement('div');
    overlay.className = 'sidebar-overlay';
    document.body.appendChild(overlay);

    // Toggle function
    function toggleSidebar() {
        if (window.innerWidth <= 768) {
            if (sidebar.style.transform === 'translateY(0px)') {
                sidebar.style.transform = 'translateY(100%)';
                toggleBtn.classList.remove('active');
                overlay.classList.remove('active');
            } else {
                sidebar.style.transform = 'translateY(0)';
                toggleBtn.classList.add('active');
                overlay.classList.add('active');
            }
        } else {
            if (sidebar.style.transform === 'translateX(0px)') {
                sidebar.style.transform = 'translateX(-100%)';
                toggleBtn.classList.remove('active');
                overlay.classList.remove('active');
            } else {
                sidebar.style.transform = 'translateX(0)';
                toggleBtn.classList.add('active');
                overlay.classList.add('active');
            }
        }
    }

    // Initial state setup for mobile
    function setupMobileState() {
        if (window.innerWidth <= 768) {
            sidebar.style.transform = 'translateX(-100%)';
            toggleBtn.classList.remove('active');
            overlay.classList.remove('active');
        } else {
            sidebar.style.transform = 'translateX(0)';
            toggleBtn.classList.remove('active');
            overlay.classList.remove('active');
        }
    }

    // Event listeners
    toggleBtn.addEventListener('click', toggleSidebar);
    overlay.addEventListener('click', toggleSidebar);

    // Close sidebar when clicking nav links on mobile
    const navLinks = document.querySelectorAll('#sidebar .nav-link');
    navLinks.forEach(link => {
        link.addEventListener('click', function() {
            if (window.innerWidth <= 768) {
                toggleSidebar();
            }
        });
    });

    // Run setup immediately
    setupMobileState();

    // Run setup on resize
    window.addEventListener('resize', setupMobileState);

    // Update sidebar position on scroll
    window.addEventListener('scroll', function() {
        const scrollTop = window.scrollY;
        if (scrollTop <= 56) {
            sidebar.style.top = (56 - scrollTop) + 'px';
        }
    });

    const resumeForm = document.getElementById('resumeForm');
    resumeForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Create and show the confirmation modal
        const modal = document.createElement('div');
        modal.className = 'confirmation-modal';
        // Update just the buttons part of the modal template
        modal.innerHTML = `
            <div class="confirmation-content">
                <h4 class="mb-3"><i class="fas fa-question-circle me-2"></i>Confirm Submission</h4>
                <p class="mb-3">Are you sure you want to generate your resume?</p>
                <div class="confirmation-buttons">
                    <button class="btn btn-outline-secondary btn-sm d-inline-flex align-items-center justify-content-center" id="cancelSubmit">Cancel</button>
                    <button class="btn btn-dark btn-sm d-inline-flex align-items-center justify-content-center" id="confirmSubmit">
                        <span class="normal-state d-inline-flex align-items-center">
                            <i class="fas fa-check me-2"></i>Generate
                        </span>
                        <span class="loading-state d-none d-inline-flex align-items-center">
                            <i class="fas fa-circle-notch fa-spin me-2"></i>Generating...
                        </span>
                    </button>
                </div>
            </div>
        `;
        
        document.body.appendChild(modal);
        
        // Add event listeners for the buttons
        document.getElementById('cancelSubmit').onclick = function() {
            modal.remove();
        };
        
        document.getElementById('confirmSubmit').onclick = function() {
            const btn = this;
            const normalState = btn.querySelector('.normal-state');
            const loadingState = btn.querySelector('.loading-state');
            
            // Show loading state
            normalState.classList.add('d-none');
            loadingState.classList.remove('d-none');
            btn.disabled = true;
            
            // Add loading overlay
            const loadingOverlay = document.createElement('div');
            loadingOverlay.className = 'loading-overlay';
            loadingOverlay.innerHTML = `
                <div class="loading-content">
                    <i class="fas fa-circle-notch fa-spin fa-2x mb-3"></i>
                    <p>Generating Your Resume 💀</p>
                </div>
            `;
            document.body.appendChild(loadingOverlay);
            
            // Submit the form
            resumeForm.submit();
        };
    });
});

function selectTemplate(templateId) {
    // Remove selected class from all options
    document.querySelectorAll('.template-option').forEach(option => {
        option.classList.remove('selected');
    });
    
    // Add selected class to clicked option
    const selectedOption = document.querySelector(`[onclick="selectTemplate('${templateId}')"]`);
    selectedOption.classList.add('selected');
    
    // Check the radio button
    document.querySelector(`#${templateId}Template`).checked = true;
}