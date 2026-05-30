let languagesChart = null;
let currentAnalysisId = null;

document.addEventListener('DOMContentLoaded', () => {
    loadHistory();

    const analyzeBtn = document.getElementById('analyzeBtn');
    const repoUrlInput = document.getElementById('repoUrl');
    const exportPdfBtn = document.getElementById('exportPdfBtn');

    analyzeBtn.addEventListener('click', () => {
        const url = repoUrlInput.value.trim();
        if (url) {
            analyzeRepo(url);
        }
    });

    repoUrlInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            const url = repoUrlInput.value.trim();
            if (url) {
                analyzeRepo(url);
            }
        }
    });

    exportPdfBtn.addEventListener('click', () => {
        if (currentAnalysisId) {
            window.location.href = `/api/export/${currentAnalysisId}`;
        }
    });
});

async function analyzeRepo(url) {
    const loading = document.getElementById('loading');
    const error = document.getElementById('error');
    const dashboard = document.getElementById('dashboard');

    loading.classList.remove('hidden');
    error.classList.add('hidden');
    dashboard.classList.add('hidden');

    try {
        const response = await fetch('/api/analyze', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url })
        });

        if (!response.ok) {
            const detail = await response.json();
            throw new Error(detail.detail || 'Analysis failed');
        }

        const data = await response.json();
        displayData(data);
        loadHistory();
    } catch (err) {
        error.textContent = err.message;
        error.classList.remove('hidden');
    } finally {
        loading.classList.add('hidden');
    }
}

function displayData(data) {
    currentAnalysisId = data.id;
    document.getElementById('dashboard').classList.remove('hidden');
    document.getElementById('exportPdfBtn').classList.remove('hidden');
    document.getElementById('healthScore').textContent = data.health_score;
    document.getElementById('stars').textContent = data.stars.toLocaleString();
    document.getElementById('forks').textContent = data.forks.toLocaleString();
    document.getElementById('issues').textContent = data.open_issues.toLocaleString();
    
    document.getElementById('repoName').textContent = data.repo_name;
    document.getElementById('repoOwner').textContent = data.owner;
    document.getElementById('contributors').textContent = data.contributors_count;

    // Display top contributors
    const contributorsList = document.getElementById('contributorsList');
    if (data.top_contributors && data.top_contributors.length > 0) {
        contributorsList.innerHTML = data.top_contributors.map(c => `
            <a href="${c.html_url}" target="_blank" class="contributor-card">
                <img src="${c.avatar_url}" alt="${c.login}" class="contributor-avatar">
                <span class="contributor-name">${c.login}</span>
                <span class="contributor-commits">${c.contributions} commits</span>
            </a>
        `).join('');
    } else {
        contributorsList.innerHTML = '<p>No contributor data available</p>';
    }

    // Health score color
    const hs = data.health_score;
    const hsElement = document.getElementById('healthScore');
    if (hs >= 80) hsElement.style.color = '#2ea44f';
    else if (hs >= 50) hsElement.style.color = '#dbab09';
    else hsElement.style.color = '#cf222e';

    updateChart(data.languages);
}

function updateChart(languages) {
    const ctx = document.getElementById('languagesChart').getContext('2d');
    
    if (languagesChart) {
        languagesChart.destroy();
    }

    const labels = Object.keys(languages);
    const data = Object.values(languages);

    languagesChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                data: data,
                backgroundColor: [
                    '#2ea44f', '#0969da', '#dbab09', '#cf222e', '#8250df', 
                    '#bf3989', '#953800', '#6e7781', '#0550ae', '#116329'
                ]
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { position: 'bottom' }
            }
        }
    });
}

async function loadHistory() {
    const historyList = document.getElementById('historyList');
    try {
        const response = await fetch('/api/history');
        const history = await response.json();

        historyList.innerHTML = history.map(item => `
            <div class="history-item" onclick="analyzeRepo('${item.repo_url}')">
                <h4>${item.owner}/${item.repo_name}</h4>
                <p>Score: ${item.health_score} | Stars: ${item.stars}</p>
                <p>${new Date(item.created_at).toLocaleDateString()}</p>
            </div>
        `).join('');
    } catch (err) {
        console.error('Failed to load history', err);
    }
}
