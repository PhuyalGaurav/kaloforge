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
