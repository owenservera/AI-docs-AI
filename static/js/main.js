class DocumentationAgent {
    constructor() {
        this.currentCrawlId = null;
        this.statusInterval = null;
        this.startTime = null;
        this.fileStructure = null;
        
        this.initializeElements();
        this.bindEvents();
        this.initializeAnimations();
    }
    
    initializeElements() {
        // Input elements
        this.urlInput = document.getElementById('url-input');
        this.maxDepthSlider = document.getElementById('max-depth');
        this.rateLimitSlider = document.getElementById('rate-limit');
        this.depthValue = document.getElementById('depth-value');
        this.rateValue = document.getElementById('rate-value');
        
        // Checkboxes
        this.includeImages = document.getElementById('include-images');
        this.includeCss = document.getElementById('include-css');
        this.includeJs = document.getElementById('include-js');
        this.includeFonts = document.getElementById('include-fonts');
        
        // Buttons
        this.startButton = document.getElementById('start-crawl');
        this.stopButton = document.getElementById('stop-crawl');
        this.advancedToggle = document.getElementById('advanced-toggle');
        this.refreshFilesButton = document.getElementById('refresh-files');
        this.downloadZipButton = document.getElementById('download-zip');
        
        // Panels
        this.advancedPanel = document.getElementById('advanced-panel');
        this.toggleIcon = document.getElementById('toggle-icon');
        
        // Status elements
        this.statusSection = document.getElementById('status-section');
        this.fileBrowserSection = document.getElementById('file-browser-section');
        this.errorSection = document.getElementById('error-section');
        
        // Status displays
        this.crawlStatus = document.getElementById('crawl-status');
        this.pagesFound = document.getElementById('pages-found');
        this.pagesDownloaded = document.getElementById('pages-downloaded');
        this.elapsedTime = document.getElementById('elapsed-time');
        this.progressPercentage = document.getElementById('progress-percentage');
        this.progressFill = document.getElementById('progress-fill');
        this.currentPage = document.getElementById('current-page');
        
        // File browser
        this.fileSearch = document.getElementById('file-search');
        this.fileTree = document.getElementById('file-tree');
        this.errorLog = document.getElementById('error-log');
        
        // Loading overlay
        this.loadingOverlay = document.getElementById('loading-overlay');
    }
    
    bindEvents() {
        // URL input validation
        this.urlInput.addEventListener('input', this.validateUrl.bind(this));
        
        // Advanced options toggle
        this.advancedToggle.addEventListener('click', this.toggleAdvancedOptions.bind(this));
        
        // Slider updates
        this.maxDepthSlider.addEventListener('input', (e) => {
            this.depthValue.textContent = e.target.value;
        });
        
        this.rateLimitSlider.addEventListener('input', (e) => {
            this.rateValue.textContent = parseFloat(e.target.value).toFixed(1);
        });
        
        // Control buttons
        this.startButton.addEventListener('click', this.startCrawl.bind(this));
        this.stopButton.addEventListener('click', this.stopCrawl.bind(this));
        this.refreshFilesButton.addEventListener('click', this.refreshFiles.bind(this));
        this.downloadZipButton.addEventListener('click', this.downloadZip.bind(this));
        
        // File search
        this.fileSearch.addEventListener('input', this.searchFiles.bind(this));
        
        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            if (e.ctrlKey && e.key === 'Enter') {
                this.startCrawl();
            }
        });
    }
    
    initializeAnimations() {
        // Animate main title
        const typed = new Typed('#main-title', {
            strings: ['Documentation Download Agent'],
            typeSpeed: 50,
            showCursor: false,
            onComplete: () => {
                // Add gradient animation after typing
                document.getElementById('main-title').classList.add('gradient-text');
            }
        });
        
        // Animate cards on load
        anime({
            targets: '.hover-lift',
            translateY: [50, 0],
            opacity: [0, 1],
            delay: anime.stagger(200),
            duration: 800,
            easing: 'easeOutExpo'
        });
    }
    
    validateUrl() {
        const url = this.urlInput.value.trim();
        const isValid = this.isValidUrl(url);
        
        if (url && !isValid) {
            this.urlInput.classList.add('border-red-500');
            this.urlInput.classList.remove('border-gray-700');
        } else {
            this.urlInput.classList.remove('border-red-500');
            this.urlInput.classList.add('border-gray-700');
        }
        
        this.startButton.disabled = !isValid || !url;
        return isValid;
    }
    
    isValidUrl(string) {
        try {
            const url = new URL(string);
            return url.protocol === 'http:' || url.protocol === 'https:';
        } catch (_) {
            return false;
        }
    }
    
    toggleAdvancedOptions() {
        const isHidden = this.advancedPanel.classList.contains('hidden');
        
        if (isHidden) {
            this.advancedPanel.classList.remove('hidden');
            this.toggleIcon.style.transform = 'rotate(180deg)';
            
            // Animate panel appearance
            anime({
                targets: this.advancedPanel,
                opacity: [0, 1],
                translateY: [-20, 0],
                duration: 300,
                easing: 'easeOutQuad'
            });
        } else {
            this.advancedPanel.classList.add('hidden');
            this.toggleIcon.style.transform = 'rotate(0deg)';
        }
    }
    
    async startCrawl() {
        const url = this.urlInput.value.trim();
        if (!url || !this.validateUrl()) {
            this.showNotification('Please enter a valid URL', 'error');
            return;
        }
        
        this.showLoading('Starting crawl...');
        
        try {
            const requestData = {
                url: url,
                max_depth: parseInt(this.maxDepthSlider.value),
                include_images: this.includeImages.checked,
                include_css: this.includeCss.checked,
                include_js: this.includeJs.checked,
                include_fonts: this.includeFonts.checked,
                rate_limit: parseFloat(this.rateLimitSlider.value),
                user_agent: 'DocumentationAgent/1.0'
            };
            
            console.log('Starting crawl with config:', requestData);
            
            const response = await fetch('/api/start_crawl', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(requestData)
            });
            
            const result = await response.json();
            console.log('Crawl response:', result);
            
            if (response.ok) {
                this.currentCrawlId = result.crawl_id;
                this.startTime = Date.now();
                
                // Update UI
                this.startButton.disabled = true;
                this.stopButton.disabled = false;
                this.statusSection.classList.remove('hidden');
                this.errorSection.classList.add('hidden');
                
                // Start status monitoring
                this.startStatusMonitoring();
                
                this.showNotification('Crawl started successfully!', 'success');
            } else {
                throw new Error(result.detail || 'Failed to start crawl');
            }
        } catch (error) {
            console.error('Start crawl error:', error);
            this.showNotification(`Error: ${error.message}`, 'error');
        } finally {
            this.hideLoading();
        }
    }
    
    async stopCrawl() {
        if (!this.currentCrawlId) return;
        
        this.showLoading('Stopping crawl...');
        
        try {
            const response = await fetch(`/api/stop_crawl/${this.currentCrawlId}`, {
                method: 'POST'
            });
            
            if (response.ok) {
                this.showNotification('Crawl stopped successfully', 'success');
                this.resetCrawlState();
            } else {
                const error = await response.json();
                throw new Error(error.detail || 'Failed to stop crawl');
            }
        } catch (error) {
            this.showNotification(`Error: ${error.message}`, 'error');
        } finally {
            this.hideLoading();
        }
    }
    
    startStatusMonitoring() {
        this.statusInterval = setInterval(async () => {
            await this.updateCrawlStatus();
        }, 2000);
    }
    
    stopStatusMonitoring() {
        if (this.statusInterval) {
            clearInterval(this.statusInterval);
            this.statusInterval = null;
        }
    }
    
    async updateCrawlStatus() {
        if (!this.currentCrawlId) return;
        
        try {
            const response = await fetch(`/api/crawl_status/${this.currentCrawlId}`);
            const status = await response.json();
            
            if (!response.ok) {
                throw new Error(status.detail || 'Failed to get status');
            }
            
            // Update status displays
            this.updateStatusDisplay(status);
            
            // Check if crawl is completed or failed
            if (status.status === 'completed' || status.status === 'failed') {
                this.stopStatusMonitoring();
                this.onCrawlComplete(status);
            }
            
            // Update errors
            if (status.errors && status.errors.length > 0) {
                this.updateErrorLog(status.errors);
            }
            
        } catch (error) {
            console.error('Error updating status:', error);
            this.stopStatusMonitoring();
        }
    }
    
    updateStatusDisplay(status) {
        // Update status indicator
        const statusIndicator = this.crawlStatus.querySelector('.status-indicator');
        statusIndicator.className = 'status-indicator';
        
        switch (status.status) {
            case 'running':
                statusIndicator.classList.add('status-running');
                this.crawlStatus.innerHTML = '<span class="status-indicator status-running"></span>Running';
                break;
            case 'completed':
                statusIndicator.classList.add('status-completed');
                this.crawlStatus.innerHTML = '<span class="status-indicator status-completed"></span>Completed';
                break;
            case 'failed':
                statusIndicator.classList.add('status-error');
                this.crawlStatus.innerHTML = '<span class="status-indicator status-error"></span>Failed';
                break;
            default:
                statusIndicator.classList.add('status-stopped');
                this.crawlStatus.innerHTML = '<span class="status-indicator status-stopped"></span>Stopped';
        }
        
        // Update counters
        this.pagesFound.textContent = status.pages_found || 0;
        this.pagesDownloaded.textContent = status.pages_downloaded || 0;
        
        // Update elapsed time
        if (this.startTime) {
            const elapsed = Math.floor((Date.now() - this.startTime) / 1000);
            const minutes = Math.floor(elapsed / 60);
            const seconds = elapsed % 60;
            this.elapsedTime.textContent = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
        }
        
        // Update progress bar
        const progress = status.pages_found > 0 ? (status.pages_downloaded / status.pages_found) * 100 : 0;
        this.progressPercentage.textContent = `${Math.round(progress)}%`;
        this.progressFill.style.width = `${progress}%`;
        
        // Update current page
        if (status.current_page) {
            this.currentPage.textContent = `Processing: ${status.current_page}`;
        } else {
            this.currentPage.textContent = 'Processing...';
        }
    }
    
    async onCrawlComplete(status) {
        this.startButton.disabled = false;
        this.stopButton.disabled = true;
        
        if (status.status === 'completed') {
            this.showNotification('Crawl completed successfully!', 'success');
            
            // Show file browser
            this.fileBrowserSection.classList.remove('hidden');
            
            // Load file structure
            await this.loadFileStructure();
            
            // Animate completion
            this.animateCompletion();
        } else {
            this.showNotification('Crawl failed. Check error log for details.', 'error');
        }
    }
    
    async loadFileStructure() {
        if (!this.currentCrawlId) return;
        
        try {
            const response = await fetch(`/api/list_files/${this.currentCrawlId}`);
            const data = await response.json();
            
            if (response.ok) {
                this.fileStructure = data.file_structure;
                this.renderFileTree(this.fileStructure);
            } else {
                throw new Error(data.detail || 'Failed to load files');
            }
        } catch (error) {
            console.error('Error loading file structure:', error);
            this.fileTree.innerHTML = '<div class="text-center text-red-500 py-8">Error loading files</div>';
        }
    }
    
    renderFileTree(structure) {
        if (!structure || !structure.files) {
            this.fileTree.innerHTML = '<div class="text-center text-gray-500 py-8">No files found</div>';
            return;
        }
        
        const html = this.buildFileTreeHTML(structure);
        this.fileTree.innerHTML = html;
        
        // Animate file tree appearance
        anime({
            targets: this.fileTree.children,
            opacity: [0, 1],
            translateX: [-20, 0],
            delay: anime.stagger(50),
            duration: 400,
            easing: 'easeOutQuad'
        });
    }
    
    buildFileTreeHTML(structure, level = 0) {
        let html = '<ul class="space-y-1">';
        
        // Group files by directory
        const filesByDir = {};
        let totalFiles = 0;
        
        structure.files.forEach(file => {
            const pathParts = file.path.split('/');
            const filename = pathParts.pop();
            const dirPath = pathParts.join('/') || 'root';
            
            if (!filesByDir[dirPath]) {
                filesByDir[dirPath] = [];
            }
            filesByDir[dirPath].push({
                name: filename,
                path: file.path,
                size: file.size,
                content_type: file.content_type
            });
            totalFiles++;
        });
        
        // Render directories and files
        const directories = Object.keys(filesByDir).sort();
        
        directories.forEach(dir => {
            const indent = level * 20;
            const folderIcon = level === 0 ? '📁' : '📂';
            
            html += `<li style="margin-left: ${indent}px;" class="cursor-pointer hover:bg-gray-800 rounded p-2" onclick="toggleDirectory(this)">`;
            html += `<span class="folder-name">${folderIcon} ${dir === 'root' ? 'Documentation' : dir}</span>`;
            html += `</li>`;
            
            // Add files in this directory
            filesByDir[dir].forEach(file => {
                const fileIcon = this.getFileIcon(file.name);
                const sizeFormatted = this.formatFileSize(file.size);
                
                html += `<li style="margin-left: ${indent + 20}px;" class="hover:bg-gray-800 rounded p-1 text-sm">`;
                html += `<span class="file-item">${fileIcon} ${file.name} <span class="text-gray-500 text-xs">(${sizeFormatted})</span></span>`;
                html += `</li>`;
            });
        });
        
        html += '</ul>';
        
        // Add summary
        if (totalFiles > 0) {
            html = `<div class="mb-4 text-sm text-gray-400">Total files: ${totalFiles}</div>${html}`;
        }
        
        return html;
    }
    
    getFileIcon(filename) {
        const ext = filename.split('.').pop().toLowerCase();
        const iconMap = {
            'html': '🌐',
            'css': '🎨',
            'js': '⚡',
            'json': '📋',
            'png': '🖼️',
            'jpg': '🖼️',
            'jpeg': '🖼️',
            'gif': '🖼️',
            'svg': '🖼️',
            'pdf': '📄',
            'md': '📝',
            'txt': '📝',
            'zip': '📦',
            'xml': '📰',
        };
        return iconMap[ext] || '📄';
    }
    
    formatFileSize(bytes) {
        if (bytes === 0) return '0 B';
        const k = 1024;
        const sizes = ['B', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i];
    }
    
    updateErrorLog(errors) {
        if (!errors || errors.length === 0) {
            this.errorLog.innerHTML = '<div class="text-center text-gray-500">No errors reported</div>';
            return;
        }
        
        const html = errors.map(error => 
            `<div class="text-red-400 text-sm mb-2 p-2 bg-red-900/20 rounded">${error}</div>`
        ).join('');
        
        this.errorLog.innerHTML = html;
        this.errorSection.classList.remove('hidden');
    }
    
    async refreshFiles() {
        if (!this.currentCrawlId) return;
        
        this.showLoading('Refreshing files...');
        
        try {
            await this.loadFileStructure();
            this.showNotification('Files refreshed', 'success');
        } catch (error) {
            this.showNotification('Error refreshing files', 'error');
        } finally {
            this.hideLoading();
        }
    }
    
    async downloadZip() {
        if (!this.currentCrawlId) return;
        
        this.showLoading('Preparing ZIP download...');
        
        try {
            const response = await fetch(`/api/download_zip/${this.currentCrawlId}`);
            
            if (response.ok) {
                // Create download link
                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.style.display = 'none';
                a.href = url;
                a.download = `documentation_${this.currentCrawlId}.zip`;
                
                document.body.appendChild(a);
                a.click();
                
                window.URL.revokeObjectURL(url);
                document.body.removeChild(a);
                
                this.showNotification('ZIP download started!', 'success');
            } else {
                throw new Error('Failed to create ZIP file');
            }
        } catch (error) {
            this.showNotification(`Download failed: ${error.message}`, 'error');
        } finally {
            this.hideLoading();
        }
    }
    
    searchFiles() {
        const query = this.fileSearch.value.toLowerCase().trim();
        
        if (!query || !this.fileStructure) {
            this.renderFileTree(this.fileStructure);
            return;
        }
        
        // Filter files based on search query
        const filteredStructure = {
            ...this.fileStructure,
            files: this.fileStructure.files.filter(file => 
                file.path.toLowerCase().includes(query) ||
                file.name.toLowerCase().includes(query)
            )
        };
        
        this.renderFileTree(filteredStructure);
    }
    
    resetCrawlState() {
        this.stopStatusMonitoring();
        this.currentCrawlId = null;
        this.startTime = null;
        this.fileStructure = null;
        
        // Reset UI
        this.startButton.disabled = false;
        this.stopButton.disabled = true;
        this.statusSection.classList.add('hidden');
        this.fileBrowserSection.classList.add('hidden');
        this.errorSection.classList.add('hidden');
        
        // Reset displays
        this.crawlStatus.innerHTML = '<span class="status-indicator"></span>Ready';
        this.pagesFound.textContent = '0';
        this.pagesDownloaded.textContent = '0';
        this.elapsedTime.textContent = '00:00';
        this.progressPercentage.textContent = '0%';
        this.progressFill.style.width = '0%';
        this.currentPage.textContent = 'Ready to crawl';
    }
    
    animateCompletion() {
        // Animate stats cards
        anime({
            targets: '.stats-card',
            scale: [1, 1.05, 1],
            duration: 600,
            delay: anime.stagger(100),
            easing: 'easeInOutQuad'
        });
        
        // Animate progress bar completion
        anime({
            targets: this.progressFill,
            backgroundColor: ['#00a8ff', '#00ff88'],
            duration: 1000,
            easing: 'easeInOutQuad'
        });
    }
    
    showLoading(message = 'Loading...') {
        this.loadingOverlay.querySelector('p').textContent = message;
        this.loadingOverlay.classList.remove('hidden');
    }
    
    hideLoading() {
        this.loadingOverlay.classList.add('hidden');
    }
    
    showNotification(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `fixed top-4 right-4 px-6 py-3 rounded-lg text-white font-medium z-50 transform translate-x-full transition-transform duration-300`;
        
        // Set colors based on type
        switch (type) {
            case 'success':
                notification.classList.add('bg-green-600');
                break;
            case 'error':
                notification.classList.add('bg-red-600');
                break;
            case 'warning':
                notification.classList.add('bg-yellow-600');
                break;
            default:
                notification.classList.add('bg-blue-600');
        }
        
        notification.textContent = message;
        document.body.appendChild(notification);
        
        // Animate in
        setTimeout(() => {
            notification.classList.remove('translate-x-full');
        }, 100);
        
        // Animate out and remove
        setTimeout(() => {
            notification.classList.add('translate-x-full');
            setTimeout(() => {
                document.body.removeChild(notification);
            }, 300);
        }, 3000);
    }
}

// Global functions for file tree interactions
function toggleDirectory(element) {
    const contents = element.nextElementSibling;
    if (contents && contents.classList.contains('folder-contents')) {
        contents.classList.toggle('hidden');
        
        // Update folder icon
        const icon = element.querySelector('.folder-name').textContent;
        if (contents.classList.contains('hidden')) {
            element.querySelector('.folder-name').textContent = icon.replace('📂', '📁');
        } else {
            element.querySelector('.folder-name').textContent = icon.replace('📁', '📂');
        }
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new DocumentationAgent();
});

// Handle page visibility changes to pause/resume status updates
document.addEventListener('visibilitychange', () => {
    // Implementation for background tab handling could go here
});