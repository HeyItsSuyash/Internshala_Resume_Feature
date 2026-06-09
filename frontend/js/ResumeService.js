class ResumeService {
    constructor() {
        this.API_BASE = 'http://localhost:8000/api';
    }

    async getAllResumes() {
        try {
            const response = await fetch(`${this.API_BASE}/resumes`);
            if (!response.ok) throw new Error('Failed to fetch resumes');
            return await response.json();
        } catch (e) {
            console.error(e);
            return [];
        }
    }

    async getPrimaryResume() {
        const resumes = await this.getAllResumes();
        return resumes.find(r => r.is_primary) || resumes[0];
    }

    async parseResume(file) {
        const formData = new FormData();
        formData.append('file', file);

        const response = await fetch(`${this.API_BASE}/resumes/upload`, {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error('Failed to upload and parse resume');
        }

        return await response.json();
    }

    async setPrimaryResume(id) {
        const response = await fetch(`${this.API_BASE}/resumes/${id}/primary`, {
            method: 'PUT'
        });
        if (!response.ok) throw new Error('Failed to set primary resume');
        return await response.json();
    }

    async deleteResume(id) {
        const response = await fetch(`${this.API_BASE}/resumes/${id}`, {
            method: 'DELETE'
        });
        if (!response.ok) throw new Error('Failed to delete resume');
        return await response.json();
    }

    async analyzeMatch(resumeId, jobRequirementsText) {
        const response = await fetch(`${this.API_BASE}/match`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                resume_id: parseInt(resumeId),
                job_requirements: jobRequirementsText
            })
        });

        if (!response.ok) throw new Error('Failed to calculate match');
        return await response.json();
    }
    
    // Application Analytics
    async saveApplication(jobId, jobTitle, matchScore, resumeUsed) {
        const response = await fetch(`${this.API_BASE}/applications`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                job_id: jobId,
                job_title: jobTitle,
                match_score: matchScore,
                resume_used: resumeUsed
            })
        });
        if (!response.ok) throw new Error('Failed to save application');
        return await response.json();
    }
    
    async getApplications() {
        try {
            const response = await fetch(`${this.API_BASE}/applications`);
            if (!response.ok) throw new Error('Failed to fetch applications');
            return await response.json();
        } catch (e) {
            console.error(e);
            return [];
        }
    }
}

// Expose globally
window.resumeService = new ResumeService();
