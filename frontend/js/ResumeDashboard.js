// Resume Dashboard Logic

document.addEventListener('DOMContentLoaded', () => {
    if (window.location.pathname.includes('resume_page.html')) {
        initVaultUI();
    }
});

async function initVaultUI() {
    const oldContainers = document.querySelectorAll('.max-width-container, #content, .content, .container, #wrapper');
    if (oldContainers.length > 0) {
        oldContainers.forEach(c => {
            if (c.id !== 'header' && !c.closest('#header')) {
                c.style.display = 'none';
            }
        });
    }

    const vaultContainer = document.createElement('div');
    vaultContainer.className = 'resume-vault-container container';
    vaultContainer.innerHTML = `
        <div class="resume-vault-header">
            <div>
                <h1>Resume Vault</h1>
                <p>Manage your tailored resumes and find the perfect match.</p>
            </div>
            <div>
                <span class="is-chip is-chip-warning" id="vault-count">0/5 Resumes</span>
            </div>
        </div>
        
        <div class="resume-grid" id="resume-grid"></div>
        
        <div class="insights-widget" style="display:none;" id="analytics-widget">
            <h2 style="font-size: 20px; font-weight: bold; margin-bottom: 10px;">Application Insights</h2>
            <div id="analytics-list"></div>
        </div>
    `;

    document.body.appendChild(vaultContainer);

    await renderResumeGrid();
    await renderAnalytics();
}

async function renderResumeGrid() {
    const resumes = await window.resumeService.getAllResumes();
    const grid = document.getElementById('resume-grid');
    grid.innerHTML = '';
    
    document.getElementById('vault-count').textContent = `${resumes.length}/5 Resumes`;

    resumes.forEach(resume => {
        const card = document.createElement('div');
        card.className = `resume-card ${resume.is_primary ? 'primary-resume' : ''}`;
        
        // Handle new Groq JSON structure
        const skillsList = resume.keywords.skills || [];
        const educationList = resume.keywords.education || [];
        const experienceList = resume.keywords.experience || [];
        
        card.innerHTML = `
            <div class="resume-card-header">
                <div>
                    <div class="resume-card-title">${resume.filename}</div>
                    <div class="resume-card-type">Uploaded: ${new Date(resume.uploaded_at).toLocaleDateString()}</div>
                </div>
                ${resume.is_primary ? '<span class="is-chip is-chip-success">Primary</span>' : ''}
            </div>
            <div class="resume-card-body">
                <div style="font-size:12px;color:#333;margin-bottom:5px;"><strong>Extracted Profile:</strong></div>
                <p style="font-size:12px;color:#666;margin:2px 0;">🏫 ${educationList[0] || 'Unknown'}</p>
                <p style="font-size:12px;color:#666;margin:2px 0;">💼 ${experienceList[0] || 'No Experience listed'}</p>
                <p style="font-size:12px;color:#666;margin-top:5px;"><strong>Skills:</strong> ${skillsList.slice(0, 5).join(', ')}</p>
            </div>
            <div class="resume-card-footer">
                ${!resume.is_primary ? `<button class="btn btn-sm btn-outline-primary" onclick="setPrimaryResume(${resume.id})">Make Primary</button>` : '<span></span>'}
                <button class="btn btn-sm btn-outline-danger" onclick="deleteResume(${resume.id})">Delete</button>
            </div>
        `;
        grid.appendChild(card);
    });

    if (resumes.length < 5) {
        const uploadCard = document.createElement('div');
        uploadCard.className = 'resume-card upload-card';
        uploadCard.innerHTML = `
            <div class="upload-icon">📄</div>
            <div style="font-weight: bold; font-size: 16px; color: #008bdc; margin-bottom: 5px;">Import Resume</div>
            <div style="font-size: 12px; color: #666;">PDF or DOCX</div>
            <input type="file" id="resume-upload-input" style="display:none;" accept=".pdf,.doc,.docx" />
        `;
        uploadCard.onclick = () => document.getElementById('resume-upload-input').click();
        grid.appendChild(uploadCard);

        setTimeout(() => {
            document.getElementById('resume-upload-input')?.addEventListener('change', handleUpload);
        }, 100);
    }
}

async function handleUpload(event) {
    const file = event.target.files[0];
    if (!file) return;

    showUploadModal(file.name);

    try {
        await window.resumeService.parseResume(file);
        hideUploadModal();
        await renderResumeGrid();
    } catch (err) {
        alert(err.message);
        hideUploadModal();
    }
}

function showUploadModal(filename) {
    const modal = document.createElement('div');
    modal.className = 'vault-modal-overlay';
    modal.id = 'upload-modal';
    modal.innerHTML = `
        <div class="vault-modal">
            <h3 style="font-size: 20px; font-weight: bold;">Extracting Resume</h3>
            <p style="font-size: 14px; color: #666;">Analyzing ${filename} with Groq...</p>
            <div class="progress-bar-container">
                <div class="progress-bar-fill" id="upload-progress"></div>
            </div>
        </div>
    `;
    document.body.appendChild(modal);

    let progress = 0;
    const bar = document.getElementById('upload-progress');
    const interval = setInterval(() => {
        progress += 5;
        if (bar) bar.style.width = `${Math.min(progress, 95)}%`;
        if (progress >= 95) clearInterval(interval);
    }, 200);
    
    modal.dataset.interval = interval;
}

function hideUploadModal() {
    const modal = document.getElementById('upload-modal');
    if (modal) {
        if(modal.dataset.interval) clearInterval(parseInt(modal.dataset.interval));
        modal.remove();
    }
}

window.setPrimaryResume = async function(id) {
    await window.resumeService.setPrimaryResume(id);
    await renderResumeGrid();
};

window.deleteResume = async function(id) {
    if(confirm('Are you sure you want to delete this resume?')) {
        await window.resumeService.deleteResume(id);
        await renderResumeGrid();
    }
};

async function renderAnalytics() {
    const apps = await window.resumeService.getApplications();
    if (apps.length > 0) {
        const widget = document.getElementById('analytics-widget');
        const list = document.getElementById('analytics-list');
        widget.style.display = 'block';
        list.innerHTML = apps.map(app => `
            <div class="insight-item">
                <div>
                    <div style="font-weight: bold;">${app.jobTitle}</div>
                    <div style="font-size: 12px; color: #666;">Applied: ${new Date(app.appliedAt).toLocaleDateString()}</div>
                </div>
                <div style="text-align:right;">
                    <div class="is-chip is-chip-success">Match: ${app.matchScore}%</div>
                    <div style="font-size: 12px; color: #666;">Using: ${app.resumeUsed}</div>
                </div>
            </div>
        `).join('');
    }
}
