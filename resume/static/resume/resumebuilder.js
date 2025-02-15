 // Function to show the corresponding section
 function showSection(sectionId) {
    // Hide all sections
    const sections = document.querySelectorAll('.card');
    sections.forEach(section => {
        section.style.display = 'none';
    });

    // Show the clicked section
    const activeSection = document.getElementById(sectionId);
    if (activeSection) {
        activeSection.style.display = 'block';
    }

    // Highlight the active link in sidebar
    const links = document.querySelectorAll('.nav-link');
    links.forEach(link => {
        link.classList.remove('active');
    });

    const activeLink = document.querySelector(`a[href="#${sectionId}"]`);
    if (activeLink) {
        activeLink.classList.add('active');
    }
}

// Initially show the basic-info section
document.addEventListener('DOMContentLoaded', () => {
    showSection('basic-info');
});