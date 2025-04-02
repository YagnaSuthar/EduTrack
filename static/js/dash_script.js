// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize all charts
    initStudentStatisticChart();
    initProgressCharts();
    initAttendanceChart();
    
    // Theme toggle functionality
    const themeToggle = document.getElementById('theme-toggle');
    themeToggle.addEventListener('change', function() {
        document.body.classList.toggle('dark-theme');
    });
});

// Initialize Student Statistic Chart
function initStudentStatisticChart() {
    const ctx = document.getElementById('studentChart').getContext('2d');
    
    // Create gradient for bar fill
    const barGradient = ctx.createLinearGradient(0, 0, 0, 400);
    barGradient.addColorStop(0, 'rgba(0, 71, 178, 0.9)');
    barGradient.addColorStop(1, 'rgba(0, 71, 178, 0.6)');
    
    const studentChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Class A', 'Class B', 'Class C', 'Class D', 'Class E','Class F'],
            datasets: [
                {
                    type: 'bar',
                    label: 'Performance',
                    data: [87, 53, 55, 45, 97, 41],
                    backgroundColor: barGradient,
                    borderRadius: 6,
                    borderSkipped: false,
                    barPercentage: 0.5,
                    categoryPercentage: 0.8
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100,
                    ticks: {
                        stepSize: 10
                    },
                    grid: {
                        display: false
                    }
                },
                x: {
                    grid: {
                        display: false
                    }
                }
            },
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    backgroundColor: 'rgba(255, 255, 255, 0.9)',
                    titleColor: '#333',
                    bodyColor: '#666',
                    borderColor: '#ddd',
                    borderWidth: 1,
                    caretPadding: 10,
                    cornerRadius: 6,
                    displayColors: false
                }
            }
        }
    });
}

// Initialize Progress Charts (Circular)
let charts = {}; // Store chart instances

function initProgressCharts(classKey = 'A') {
    const classData = {
        A: [
            { id: 'progressChartA', percentage: 32 },
            { id: 'progressChartB', percentage: 43 },
            { id: 'progressChartC', percentage: 67 },
            { id: 'progressChartD', percentage: 56 }
        ],
        B: [
            { id: 'progressChartA', percentage: 50 },
            { id: 'progressChartB', percentage: 60 },
            { id: 'progressChartC', percentage: 75 },
            { id: 'progressChartD', percentage: 80 }
        ],
        C: [
            { id: 'progressChartA', percentage: 15 },
            { id: 'progressChartB', percentage: 90 },
            { id: 'progressChartC', percentage: 7 },
            { id: 'progressChartD', percentage: 86 }
        ],
        D: [
            { id: 'progressChartA', percentage: 62 },
            { id: 'progressChartB', percentage: 93 },
            { id: 'progressChartC', percentage: 27 },
            { id: 'progressChartD', percentage: 46 }
        ],
        E: [
            { id: 'progressChartA', percentage: 72 },
            { id: 'progressChartB', percentage: 93 },
            { id: 'progressChartC', percentage: 97 },
            { id: 'progressChartD', percentage: 26 }
        ],
        F: [
            { id: 'progressChartA', percentage: 32 },
            { id: 'progressChartB', percentage: 53 },
            { id: 'progressChartC', percentage: 17 },
            { id: 'progressChartD', percentage: 96 }
        ]
    };

    const selectedData = classData[classKey] || classData.A;

    selectedData.forEach(data => {
        const canvas = document.getElementById(data.id);
        if (!canvas) return;
        const ctx = canvas.getContext('2d');

        // Destroy existing chart if it exists
        if (charts[data.id]) {
            charts[data.id].destroy();
        }

        // Create new chart instance
        charts[data.id] = new Chart(ctx, {
            type: 'doughnut',
            data: {
                datasets: [{
                    data: [data.percentage, 100 - data.percentage],
                    backgroundColor: [
                        'rgba(0, 71, 178, 0.9)',
                        'rgba(66, 42, 185, 0.35)'
                    ],
                    borderWidth: 0,
                    cutout: '80%'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        enabled: false
                    }
                }
            }
        });
    });
}

// Event listener for dropdown change
document.getElementById("classSelect").addEventListener("change", function () {
    const selectedClass = this.value; // Get selected class
    initProgressCharts(selectedClass);
});

// Initialize default charts
initProgressCharts();


// Initialize Attendance Chart
function initAttendanceChart() {
    const ctx = document.getElementById('attendanceChart').getContext('2d');
    
    // Create gradient for area fill
    const areaGradient = ctx.createLinearGradient(0, 0, 0, 400);
    areaGradient.addColorStop(0, 'rgba(2, 67, 165, 0.45)');
    areaGradient.addColorStop(1, 'rgba(255, 255, 255, 0)');
    
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['Week 1', 'Week 2', 'Week 3', 'Week 4', 'Week 5','Week 6'],
            datasets: [{
                label: 'Attendance',
                data: [55, 45, 30, 70, 90, 44],
                borderColor: 'rgba(0, 71, 178, 1)',
                backgroundColor: areaGradient,
                pointBackgroundColor: '#fff',
                pointBorderColor: 'rgba(0, 71, 178, 1)',
                pointBorderWidth: 2,
                pointRadius: 4,
                pointHoverRadius: 6,
                fill: true,
                tension: 0.412
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100,
                    ticks: {
                        stepSize: 20
                    },
                    grid: {
                        display: true,
                        color: 'rgba(0, 0, 0, 0.05)'
                    }
                },
                x: {
                    grid: {
                        display: true,
                        color: 'rgba(0, 0, 0, 0.05)'
                    }
                }
            },
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    backgroundColor: 'rgba(255, 255, 255, 0.9)',
                    titleColor: '#333',
                    bodyColor: '#666',
                    borderColor: '#ddd',
                    borderWidth: 1,
                    caretPadding: 10,
                    cornerRadius: 6,
                    displayColors: false
                }
            }
        }
    });
}

// Handle responsive sidebar
const sidebarToggle = document.createElement('button');
sidebarToggle.className = 'sidebar-toggle';
sidebarToggle.innerHTML = '<i class="fas fa-bars"></i>';
document.querySelector('.header').prepend(sidebarToggle);

sidebarToggle.addEventListener('click', function() {
    document.querySelector('.sidebar').classList.toggle('active');
    document.querySelector('.main-content').classList.toggle('sidebar-active');
});

// document.addEventListener("DOMContentLoaded", function() {
//     let header = document.querySelector('.header');
    
//     if (header) {
//         const sidebarToggle = document.createElement('button');
//         sidebarToggle.className = 'sidebar-toggle';
//         sidebarToggle.innerHTML = '<i class="fas fa-bars"></i>';
//         header.prepend(sidebarToggle);

//         sidebarToggle.addEventListener('click', function() {
//             document.querySelector('.sidebar')?.classList.toggle('active');
//             document.querySelector('.main-content')?.classList.toggle('sidebar-active');
//         });
//     } else {
//         console.error("Header element not found!");
//     }
// });


// Add responsive styles
const responsiveStyles = document.createElement('style');
responsiveStyles.textContent = `
    @media (max-width: 768px) {
        .sidebar {
            transform: translateX(-100%);
            transition: transform 0.3s ease;
            z-index: 1000;
        }
        
        .sidebar.active {
            transform: translateX(0);
        }
        
        .main-content {
            margin-left: 0;
            transition: margin-left 0.3s ease;
        }
        
        .sidebar-toggle {
            display: block;
            background: none;
            border: none;
            font-size: 1.5rem;
            cursor: pointer;
            color: var(--primary-color);
            margin-right: 10px;
        }
        
        .header {
            padding: 10px;
        }
        
        .search-bar {
            width: 200px;
        }
    }
    
    @media (min-width: 769px) {
        .sidebar-toggle {
            display: none;
        }
    }
    
    @media (max-width: 992px) {
        .dashboard-grid {
            grid-template-columns: 1fr;
        }
        
        .student-statistic, 
        .class-progress, 
        .upcoming-activities,
        .attendance,
        .staff-room,
        .documents {
            grid-column: span 1;
        }
    }
`;

document.head.appendChild(responsiveStyles);
