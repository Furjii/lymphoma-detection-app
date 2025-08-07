document.addEventListener('DOMContentLoaded', function() {     
    const uploadArea = document.getElementById('upload-area');     
    const fileInput = document.getElementById('file-input');     
    const previewContainer = document.getElementById('preview-container');     
    const imagePreview = document.getElementById('image-preview');     
    const analyzeBtn = document.getElementById('analyze-btn'); 

    uploadArea.addEventListener('click', function() {       
        fileInput.click();     
    });           

    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {       
        uploadArea.addEventListener(eventName, preventDefaults, false);     
    });           

    function preventDefaults(e) {       
        e.preventDefault();       
        e.stopPropagation();     
    }           

    ['dragenter', 'dragover'].forEach(eventName => {       
        uploadArea.classList.add('active');     
    });           

    ['dragleave', 'drop'].forEach(eventName => {       
        uploadArea.classList.remove('active');     
    });           

    uploadArea.addEventListener('drop', handleDrop, false);           

    function handleDrop(e) {       
        const dt = e.dataTransfer;       
        const files = dt.files;              
        if (files.length) {         
            fileInput.files = files;         
            handleFiles(files);       
        }     
    }           

    fileInput.addEventListener('change', function() {       
        if (fileInput.files.length) {         
            handleFiles(fileInput.files);       
        }     
    });           

    function handleFiles(files) {       
        const file = files[0];              
        if (file && isValidFileType(file)) {         
            previewContainer.innerHTML = ''; // clear previous preview

            if (file.type === 'image/tiff' || file.name.endsWith('.tif') || file.name.endsWith('.tiff')) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    try {
                        const tiff = new Tiff({ buffer: e.target.result });
                        const canvas = tiff.toCanvas();
                        canvas.id = 'tiff-canvas';
                        canvas.className = 'rounded shadow-sm mb-2';
                        canvas.style.maxWidth = '200px';
                        canvas.style.maxHeight = '180px';
                        canvas.style.display = 'block';
                        canvas.style.margin = '0 auto';

                        previewContainer.appendChild(canvas);
                        previewContainer.classList.remove('d-none');
                        previewContainer.classList.add('fade-in');

                        analyzeBtn.disabled = false;
                        successFeedback();
                        console.log('TIFF preview created successfully');
                    } catch (err) {
                        console.error('Error parsing TIFF:', err);
                        alert('Could not preview the TIFF file.');
                        resetUploadArea();
                    }
                };
                reader.readAsArrayBuffer(file);
            } else {
                const reader = new FileReader();
                reader.onload = function(e) {
                    const newImage = document.createElement('img');
                    newImage.src = e.target.result;
                    newImage.id = 'image-preview';
                    newImage.className = 'img-fluid';
                    newImage.style.maxWidth = '200px';
                    newImage.style.maxHeight = '180px';
                    newImage.style.display = 'block';
                    newImage.style.margin = '0 auto';
                    newImage.style.borderRadius = '8px';
                    newImage.style.boxShadow = '0 4px 8px rgba(0,0,0,0.1)';
                    newImage.style.marginTop = '15px';

                    previewContainer.appendChild(newImage);
                    previewContainer.classList.remove('d-none');
                    previewContainer.classList.add('fade-in');

                    analyzeBtn.disabled = false;
                    successFeedback();
                    console.log('Image preview created successfully');
                };
                reader.readAsDataURL(file);
            }     
        } else {         
            alert('Please select a valid image file (JPG, JPEG, PNG, TIF).');
            resetUploadArea();       
        }     
    }           

    function isValidFileType(file) {       
        const validTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/tiff', 'image/tif'];       
        return validTypes.includes(file.type) || file.name.endsWith('.tif') || file.name.endsWith('.tiff');     
    }

    function successFeedback() {
        uploadArea.style.borderColor = '#28a745';
        uploadArea.style.backgroundColor = '#d4edda';
        const uploadContent = uploadArea.querySelector('p');
        if (uploadContent) {
            const originalText = uploadContent.textContent;
            uploadContent.innerHTML = '<i class="fas fa-check-circle text-success me-2"></i>Image uploaded successfully!';
            setTimeout(() => {
                uploadArea.style.borderColor = '';
                uploadArea.style.backgroundColor = '';
                uploadContent.textContent = originalText;
            }, 8000);
        }
    }

    function resetUploadArea() {
        previewContainer.classList.add('d-none');
        previewContainer.classList.remove('fade-in');
        previewContainer.innerHTML = '';
        analyzeBtn.disabled = true;
        fileInput.value = '';
        uploadArea.style.borderColor = '';
        uploadArea.style.backgroundColor = '';
    }

    const uploadForm = document.getElementById('upload-form');
    if (uploadForm) {
        uploadForm.addEventListener('submit', function(e) {
            if (!fileInput.files.length) {
                e.preventDefault();
                alert('Please select an image file first.');
                return;
            }
            analyzeBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Analyzing...';
            analyzeBtn.disabled = true;
        });
    }
});
