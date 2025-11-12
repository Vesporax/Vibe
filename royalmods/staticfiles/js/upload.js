// Mod Upload Form JavaScript

document.addEventListener('DOMContentLoaded', function() {
    initializeImagePreview();
});

function initializeImagePreview() {
    const imageInput = document.getElementById('id_images');
    const previewContainer = document.getElementById('image-preview');
    
    if (!imageInput || !previewContainer) return;
    
    let selectedFiles = [];

    imageInput.addEventListener('change', function(e) {
        const files = Array.from(e.target.files);
        
        // Limit to 6 images
        if (files.length > 6) {
            alert('You can only upload up to 6 images. The first 6 images will be used.');
            selectedFiles = files.slice(0, 6);
        } else {
            selectedFiles = files;
        }

        // Clear previous previews
        previewContainer.innerHTML = '';

        // Display previews
        selectedFiles.forEach((file, index) => {
            if (file.type.startsWith('image/')) {
                createImagePreview(file, index, previewContainer);
            }
        });

        // Update file input with limited files
        if (files.length > 6) {
            updateFileInput(imageInput, selectedFiles);
        }
    });
}

function createImagePreview(file, index, container) {
    const reader = new FileReader();
    
    reader.onload = function(e) {
        const previewDiv = document.createElement('div');
        previewDiv.className = 'image-preview';
        
        const img = document.createElement('img');
        img.src = e.target.result;
        img.alt = `Preview ${index + 1}`;
        
        const numberLabel = document.createElement('span');
        numberLabel.className = 'image-number';
        numberLabel.textContent = index === 0 ? 'Main' : `#${index + 1}`;
        
        previewDiv.appendChild(img);
        previewDiv.appendChild(numberLabel);
        container.appendChild(previewDiv);
    };
    
    reader.readAsDataURL(file);
}

function updateFileInput(input, files) {
    // Create a new FileList with limited files
    const dt = new DataTransfer();
    files.forEach(file => dt.items.add(file));
    input.files = dt.files;
}