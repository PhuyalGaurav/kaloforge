async function downloadPDF(event, url, filename) {
    event.preventDefault();
    
    try {
        // Show loading state
        const button = event.target.closest('a');
        const originalText = button.innerHTML;
        button.innerHTML = '<i class="bi bi-arrow-clockwise"></i> Downloading...';
        button.disabled = true;

        // Fetch the PDF with proper headers
        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'Accept': 'application/pdf'
            }
        });

        if (!response.ok) throw new Error('Download failed');

        const blob = await response.blob();
        const blobUrl = window.URL.createObjectURL(blob);
        
        // Create download link
        const a = document.createElement('a');
        a.href = blobUrl;
        a.download = `resume_${filename}.pdf`;
        document.body.appendChild(a);
        a.click();
        
        // Cleanup
        window.URL.revokeObjectURL(blobUrl);
        document.body.removeChild(a);

        // Restore button state
        button.innerHTML = originalText;
        button.disabled = false;

    } catch (error) {
        console.error('Download failed:', error);
        // Fallback to direct link
        const a = document.createElement('a');
        a.href = url;
        a.download = `resume_${filename}.pdf`;
        a.target = '_blank';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
    }
}

function showResume(element) {
    const resumeId = element.tagName === 'SELECT' ? element.value : element.getAttribute('data-resume-id');
    if (!resumeId) return;
    
    // Show loading state
    const container = document.querySelector('.resume-pdf-container');
    container.innerHTML = `
        <div class="text-center mt-5">
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
            <p class="mt-3">Loading PDF...</p>
        </div>
    `;
    
    fetch(`/api/resume/${resumeId}/`)
        .then(response => {
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            return response.json();
        })
        .then(data => {
            if (!data.pdf_url) {
                throw new Error('PDF URL not available');
            }
            
            // Update PDF preview
            container.innerHTML = `
                <embed src="${data.pdf_url}" 
                       type="application/pdf" 
                       class="resume-pdf-preview"
                       data-resume-id="${resumeId}">
            `;
            
            // Update desktop action buttons
            const desktopButtons = document.querySelector('.d-none.d-lg-flex .btn-group');
            if (desktopButtons) {
                desktopButtons.innerHTML = `
                    <a href="${data.pdf_url}" 
                       class="btn btn-primary" 
                       download="resume_${data.data.name}.pdf"
                       onclick="downloadPDF(event, '${data.pdf_url}', '${data.data.name}')">
                        <i class="bi bi-download me-2"></i>Download PDF
                    </a>
                    <a href="${data.pdf_url}" 
                       class="btn btn-outline-primary" 
                       target="_blank">
                        <i class="bi bi-eye me-2"></i>View in Browser
                    </a>
                    <a href="/form?resume_id=${data.id}" 
                       class="btn btn-outline-secondary bg-light">
                        <i class="bi bi-pencil me-2"></i>Edit
                    </a>
                `;
            }

            // Update mobile action buttons
            const mobileButtons = document.querySelector('.d-lg-none.position-fixed');
            if (mobileButtons) {
                const createdDate = new Date(data.created_at).toLocaleDateString('en-US', {
                    month: 'short',
                    day: 'numeric',
                    year: 'numeric'
                });
                
                mobileButtons.innerHTML = `
                    <div class="d-flex justify-content-center gap-2">
                        <a href="${data.pdf_url}" 
                           class="btn btn-primary" 
                           style="width: 48px"
                           download="resume_${data.data.name}.pdf"
                           onclick="downloadPDF(event, '${data.pdf_url}', '${data.data.name}')">
                            <i class="bi bi-download"></i>
                        </a>
                        <a href="${data.pdf_url}" 
                           class="btn btn-outline-primary"
                           style="width: 48px"
                           target="_blank">
                            <i class="bi bi-eye"></i>
                        </a>
                        <a href="/form?resume_id=${data.id}" 
                           class="btn btn-outline-secondary bg-light"
                           style="width: 48px">
                            <i class="bi bi-pencil"></i>
                        </a>
                    </div>
                    <div class="text-center mt-2 small text-muted">
                        <span>${data.data.name}</span> •
                        <span>Created: ${createdDate}</span>
                    </div>
                `;
            }
            
            // Update UI states
            updateUIStates(resumeId);
        })
        .catch(error => {
            console.error('Error:', error);
            container.innerHTML = `
                <div class="text-center text-muted mt-5">
                    <p><i class="bi bi-exclamation-circle text-danger fs-1"></i></p>
                    <h5>Error Loading PDF</h5>
                    <p class="small text-danger">${error.message}</p>
                    <button class="btn btn-outline-primary btn-sm mt-3" 
                            onclick="showResume(document.querySelector('[data-resume-id=\'${resumeId}\']'))">
                        <i class="bi bi-arrow-clockwise me-2"></i>Try Again
                    </button>
                </div>
            `;
        });
}

function updateUIStates(resumeId) {
    // Update active states
    document.querySelectorAll('.resume-item a').forEach(a => {
        a.classList.toggle('active', a.getAttribute('data-resume-id') === resumeId);
    });
    
    // Update mobile dropdown
    const mobileSelect = document.querySelector('select');
    if (mobileSelect) mobileSelect.value = resumeId;
}

async function downloadPDF(event, url, filename) {
    event.preventDefault();
    
    try {
        // Show loading state
        const button = event.target.closest('a');
        const originalText = button.innerHTML;
        button.innerHTML = '<i class="bi bi-arrow-clockwise animation-spin"></i> Downloading...';
        button.disabled = true;

        // Fetch the PDF
        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'Accept': 'application/pdf'
            }
        });

        if (!response.ok) throw new Error('Download failed');

        const blob = await response.blob();
        const blobUrl = window.URL.createObjectURL(blob);
        
        // Trigger download
        const a = document.createElement('a');
        a.href = blobUrl;
        a.download = `resume_${filename}.pdf`;
        document.body.appendChild(a);
        a.click();
        
        // Cleanup
        window.URL.revokeObjectURL(blobUrl);
        document.body.removeChild(a);

        // Restore button state
        button.innerHTML = originalText;
        button.disabled = false;

    } catch (error) {
        console.error('Download failed:', error);
        // Fallback to direct download
        window.open(url, '_blank');
    }
}
