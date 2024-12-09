async function checkForNewNotifications() {
    try {
        const response = await fetch('/get_user_notifications/unread');
        const data = await response.json();

        const notificationCount = data.notifications ? data.notifications.length : 0;
        return notificationCount;
    } catch (error) {
        console.error('Error checking for notifications:', error);
        return 0; // Default to no notifications if there's an error
    }
}

async function getUserName() {
    try {
        const response = await fetch('/get_user_info/');
        const data = await response.json();

        if (data.error) {
            throw new Error(data.error);
        }

        return data; // Assuming the data contains a `username` field
    } catch (error) {
        console.error('Error fetching user info:', error);
        return { username: 'Guest' }; // Fallback for guest users
    }
}
function setCurrentSection(section) {
    localStorage.setItem('currentSection', section);
}

function clearCurrentSection() {
    localStorage.removeItem('currentSection');
}

// Load content dynamically based on selected tab
function loadContent(section) {
    const dynamicContent = document.getElementById('dynamic-content');

    if (section === 'account') {
        setCurrentSection('account');
        dynamicContent.innerHTML = `
<form id="account-form">
<h2>My Account</h2>
    <fieldset>
        <legend>Update Your Information</legend>

        <!-- Form fields (First Name, Last Name, etc.) -->
        <div class="input-group">
            <label for="first-name">First Name:</label>
            <input type="text" id="first-name" name="first_name" placeholder="Enter your first name" required>
        </div>

        <div class="input-group">
            <label for="last-name">Last Name:</label>
            <input type="text" id="last-name" name="last_name" placeholder="Enter your last name" required>
        </div>

        <div class="input-group">
            <label for="email">Email:</label>
            <input type="email" id="email" name="email" placeholder="Enter your email" required>
        </div>

        <div class="input-group">
            <label for="current-password">Current Password:</label>
            <input type="password" id="current-password" name="current_password" placeholder="Enter your current password" required>
        </div>

        <div class="input-group">
            <label for="new-password">New Password:</label>
            <input type="password" id="new-password" name="new_password" placeholder="Enter a new password">
        </div>

        <!-- Submit Button and Messages Container -->
        <div class="form-actions">
            <button type="button" onclick="saveAccountChanges()">Save Changes</button>

            <!-- Success and Error messages (initially hidden) -->
            <div id="account-message" class="message success" style="display: none;"></div>
            <div id="account-error-message" class="message error" style="display: none;"></div>
        </div>
    </fieldset>
</form>
        `;

        // calling getUserInfo() to populate the form with user info, such as first name, last name, and email.
        getUserInfo();
    } else if (section === 'dashboard') {
        setCurrentSection('dashboard');
        // Fetch notifications and user information
        Promise.all([checkForNewNotifications(), getUserName()]).then(([notificationCount, user]) => {
            dynamicContent.innerHTML = `
                <h2>Dashboard</h2>
                <p>Welcome back, ${user.first_name} ${user.last_name}. </p>
                ${notificationCount > 0 
                    ? `<p style="color: green; font-weight: bold;">You have ${notificationCount} new notification${notificationCount > 1 ? 's' : ''}!</p>`
                    : `<p>You have no new notifications.</p>`}
            `;
        }).catch(error => {
            console.error("Error loading dashboard content:", error);
            dynamicContent.innerHTML = `
                <h2>Dashboard</h2>
                <p>Overview of recent activity, test statistics, and other relevant information will be displayed here.</p>
            `;
        });
    } else if (section === 'tests') {
        setCurrentSection('tests'); 
        dynamicContent.innerHTML = `
            <div class="dynamic-content">
                <h2>Tests</h2>

                <div class="test-buttons">
                    <button class="btn-create-test" onclick="createTest()">Create a New Test</button>
                    <button class="btn-retrieve-results" onclick="retrieveTestResults()">Retrieve Patient Test Results</button>
                </div>

                <div class="filter-content-wrapper" id="filter-content-wrapper">
                    <!-- Test Status Filter Section -->
                    <div class="test-status-filter" id="test-status-filter">
                        <!-- Legend Section Above the Filter -->
                            <div class="legend" id="legend">
                                <div class="legend-item">
                                    <span class="legend-circle legend-green"></span>
                                    <span class="legend-text">Complete</span>
                                </div>
                                <div class="legend-item">
                                    <span class="legend-circle legend-gray"></span>
                                    <span class="legend-text">Pending</span>
                                </div>
                                <div class="legend-item">
                                    <span class="legend-circle legend-red"></span>
                                    <span class="legend-text">Invalid</span>
                                </div>
                            </div>

                            <label for="test_status_menu">Test Status:</label>
                            <select id="test_status_menu" name="test_status_menu">
                                <option value="all">All</option>
                                <option value="completed">Completed</option>
                                <option value="pending">Pending</option>
                                <option value="invalid">Invalid</option>
                            </select>

                            <!-- Button to Apply Filter -->
                            <button onclick="retrieveTestResults()" class="apply-filter-button">Apply Filter</button>
                        </div>

                        <!-- Test Results Section -->
                        <div id="test-content">
                            <!-- Dynamic content for tests will be loaded here -->
                        </div>
                </div>
            </div>
        `;
        toggleTestStatusFilter(false);
    } else if (section === 'support') {
        setCurrentSection('support');
        dynamicContent.innerHTML = `
            <section id="support-section">
                <h2>Support</h2>

                <!-- Create a Support Ticket Section -->
                <div id="create-ticket">
                    <h3>Create a Support Ticket</h3>
                    <form id="ticketForm">
                        <div class="input-group">
                        <label for="category">Category:</label>
                        <select id="category" name="category" required>
                            <option value="general">General Issue</option>
                            <option value="technical">Technical Issue</option>
                            <option value="account">Account Management</option>
                            <option value="bug/error">Bug/Error Report</option>
                        </select>
                        </div>

                        <div class="input-group">
                            <label for="description">Issue Description:</label>
                            <textarea id="description" name="description" rows="4" required placeholder="Describe the issue you are facing..."></textarea>
                        </div>

                        <div class="form-actions">
                            <button type="button" onclick="submitTicket()">Submit Ticket</button>
                            <div id="ticket-message" class="message success" style="display: none;"></div>
                            <div id="ticket-error-message" class="message error" style="display: none;"></div>
                        </div>
                    </form>
                </div>

                <!-- List of Submitted Tickets -->
                <div id="ticket-list">
                    <h3>Your Tickets</h3>
                    <ul id="ticket-items"></ul>
                </div>
            </section>
        `;
        loadUserTickets();
    }
    closeNotifications();
}

// Function to submit a ticket
function submitTicket() {
    const category = document.getElementById('category').value;
    const description = document.getElementById('description').value;
    const errorMessage = document.getElementById('error-message');

    document.getElementById("ticket-message").style.display = "none";
    document.getElementById("ticket-error-message").style.display = "none";

    // Ensure the form is not empty or the description doesn't contain only spaces.
    if (!category || !description) {
        // Show error message if validation fails
        document.getElementById("ticket-error-message").textContent = "All fields are required!";
        document.getElementById("ticket-error-message").style.display = "block";
        return;
    }

    // Create form data object instead of sending JSON
    const formData = new FormData();
    formData.append('category', category);
    formData.append('description', description);

    // Submit the ticket via AJAX
    fetch('/submit_ticket/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken') // Ensure CSRF protection
        },
        body: formData // Send form data
    })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                document.getElementById("ticket-error-message").textContent = "All fields are required!";
                document.getElementById("ticket-error-message").style.display = "block";
            } else {
                document.getElementById("ticket-message").textContent = "Your support ticket has been submitted!";
                document.getElementById("ticket-message").style.display = "block"; // Show success message
                loadUserTickets(); // Reload tickets
                document.getElementById('ticketForm').reset(); // Clear the form
            }
        })
        .catch(error => console.error('Error:', error));
}

// Function to load the user's tickets
function loadUserTickets() {
    const ticketList = document.getElementById('ticket-items');
    ticketList.innerHTML = ''; // Clear the current list

    // Fetch the user's tickets
    fetch('/get_user_tickets/')
        .then(response => response.json())
        .then(data => {
            if (data.length === 0) {
                ticketList.innerHTML = '<li>No tickets found.</li>';
            } else {
                // Group tickets by status
                const ticketsByStatus = {
                    open: [],
                    inProgress: [],
                    closed: []
                };

                data.forEach(ticket => {
                    if (ticket.status === 'open') {
                        ticketsByStatus.open.push(ticket);
                    } else if (ticket.status === 'in progress') {
                        ticketsByStatus.inProgress.push(ticket);
                    } else if (ticket.status === 'closed') {
                        ticketsByStatus.closed.push(ticket);
                    }
                });

                // Helper function to create a ticket section
                function createTicketSection(status, tickets) {
                    if (tickets.length === 0) return `<li>No ${status} tickets.</li>`;
                    return tickets
                        .map(ticket => `
                            <li>
                                <strong>${ticket.category}</strong>: ${ticket.description}
                                <br>Submitted: ${new Date(ticket.created_at).toLocaleString()}
                            </li>
                        `)
                        .join('');
                }

                // Append sections for each status
                ticketList.innerHTML = `
                    <h4>Open Tickets</h4>
                    <ul>${createTicketSection('Open', ticketsByStatus.open)}</ul>
                    <h4>In Progress Tickets</h4>
                    <ul>${createTicketSection('In Progress', ticketsByStatus.inProgress)}</ul>
                    <h4>Closed Tickets</h4>
                    <ul>${createTicketSection('Closed', ticketsByStatus.closed)}</ul>
                `;
            }
        })
        .catch(error => console.error('Error:', error));
}

// CSRF token helper function
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Function that creates a new test with a given age of 18 or older and stores it into the backend as a link.
function createTest() {
    // Hide the test-status filter
    toggleTestStatusFilter(false);
    const testContent = document.getElementById('test-content');
    testContent.innerHTML = `
        <div class="create-test-section">
            <h2>Create a New Test</h2>
            <label for="patient-age">Please provide the patient's age:</label>
            <input type="number" id="patient-age" name="patient-age" required class="small-input"><br><br>
            <button onclick="generateTestLink()">Generate Test Link</button>
            <div id="generated-link"></div>
        </div>
    `;
    testContent.classList.add('loaded');
}

function deleteTest(testId) {
    if (!confirm("Are you sure you want to delete this invalid test?")) {
        return; // Exit if the user cancels the confirmation
    }

    fetch(`/delete_test/${testId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken') // Include CSRF token for security
        }
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        } else {
            throw new Error("Failed to delete test.");
        }
    })
    .then(data => {
        alert(data.message);
        // Optionally remove the deleted test button from the UI
        const testButton = document.getElementById(`test-${testId}`);
        if (testButton) {
            testButton.remove();
        }
    })
    .catch(error => {
        console.error("Error:", error);
        alert("An error occurred while deleting the test.");
    });
}

// Function that serves as a helper to generate a test link in the createTest function.
function generateTestLink() {
    const age = document.getElementById('patient-age').value;
    const linkContainer = document.getElementById('generated-link');

    if (age && age >= 18) {
        fetch('/create_test/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'), // CSRF Token
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ age: age })
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                linkContainer.innerHTML = `<p style="color: red;">${data.error}</p>`;
            } else {
                const testLink = data.test_link;
                linkContainer.innerHTML = `
                    <p>Here is the link to your patient's unique test:</p>
                    <input type="text" id="test-link" value="${testLink}" readonly style="width: 100%; margin-bottom: 5px;">
                    <button id="btn-copy-link" onclick="copyLink('${testLink}')">Copy Link</button>
                    <p id="copy-confirmation" style="color: green; display: none;">Test link has been copied!</p>
                `;
            }
        })
        .catch(error => console.error('Error:', error));
    } else {
        if (age) {
            linkContainer.innerHTML = `<p style="color: red;">Invalid: Age must be 18 or older.</p>`;
        } else {
            linkContainer.innerHTML = `<p style="color: red;">Please input an age for the patient.</p>`;
        }
    }
}

/**
 * Copies a given test link to the user's clipboard, and displays a confirmation message after successful copy.
 *
 * @param {string} testLink - The link to the test.
 */
function copyLink(testLink) {
    const copyButton = document.getElementById("btn-copy-link");
    const confirmationMessage = document.getElementById("copy-confirmation");

    navigator.clipboard.writeText(testLink);
    copyButton.textContent = "Link copied!";
    confirmationMessage.style.display = "block";

    // Hide the confirmation message after 2 seconds
    setTimeout(() => {
        copyButton.textContent = "Copy Link";
        confirmationMessage.style.display = "none";
    }, 2000);
}

function retrieveTestResults() {
    // Show the test-status filter
    toggleTestStatusFilter(true);
    const testContent = document.getElementById('test-content');

    let content = `
        <div class="test-results-section">
            <h2>Patient Test Results</h2>
    `;

    const test_status = document.getElementById('test_status_menu');
    const test_status_selection = test_status.options[test_status.selectedIndex].text;

    fetch(`/get_test_results/${test_status_selection}`)
        .then(response => response.json())
        .then(data => {
            if (data.tests && data.tests.length > 0) {
                data.tests.forEach(test => {
                    let colorClass = '';
                    let onclickAttr = '';
                    let deleteButtonHTML = ''; // For delete button
                    let copyButtonHTML = ''; // For copy button

                    if (test.status === 'completed') {
                        colorClass = 'completed';
                        onclickAttr = `onclick="viewTestResults(${test.id})"`;
                    } else if (test.status === 'invalid') {
                        colorClass = 'invalid';
                        deleteButtonHTML = `
                            <button class="btn btn-danger" id="delete-test-${test.id}" onclick="deleteTest(${test.id})">
                                Delete Test
                            </button>
                        `;
                    } else if (test.status === 'pending') {
                        // Set colorClass to gray for pending tests, matching the delete button style
                        colorClass = 'incomplete';
                        copyButtonHTML = `
                            <button class="btn btn-copy" onclick="copyTestLink('localhost:8000/testpage/${test.link}')">Copy Link</button>
                        `;
                    }

                    content += `
                        <div class="test-entry">
                            <button class="${colorClass}" ${onclickAttr}>
                                Test ID ${test.id} | Link: ${test.link}
                            </button>
                            ${copyButtonHTML}
                            ${deleteButtonHTML}
                        </div>
                    `;
                });
            } else {
                content += "<p>No test results available.</p>";
            }

            content += `</div>`;

            testContent.innerHTML = content;
            testContent.classList.add('loaded');
        })
        .catch(error => {
            console.error('Error:', error);

            content += `</div>`;
            testContent.innerHTML = content;
            testContent.classList.add('loaded');
        });
}

function copyTestLink(testLink) {
    navigator.clipboard.writeText(testLink);
    alert("Test link has been copied!");
}

// Track if we're in test viewing mode
let isViewingTest = false;

function viewTestResults(testId) {
    const testContent = document.getElementById('test-content');
    isViewingTest = true;
    toggleTestButtons();

    fetch(`/test_results/${testId}/`)
        .then(response => response.json())
        .then(data => {
            if (!data.test_results || data.test_results.length === 0) {
                testContent.innerHTML = `<p style="color:red;">No test results available for this test.</p>`;
                return;
            }

            // Render the table view by default
            renderTestResultsTable(data, testId);

            // Ensure only one "View as Graph" button is added
            if (!document.getElementById('viewGraphButton')) {
                const toggleButton = document.createElement("button");
                toggleButton.id = 'viewGraphButton'; // Add an ID to the button
                toggleButton.textContent = "View as Graph";
                toggleButton.onclick = () => toggleResultsView(testId, data);
                testContent.appendChild(toggleButton);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            testContent.innerHTML = `<p style="color:red;">Failed to load test results.</p>`;
        });

}

function renderTestResultsTable(data, testId) {
    const testContent = document.getElementById('test-content');
    testContent.innerHTML = `
    <div class="table-container">
        <div class="test-results-header">
            <h2>Test Results for Link: ${data.test_link}</h2>
        </div>
        <p><strong>Patient's Age:</strong> ${data.patient_age}</p>
        <p><strong>Amount Correct:</strong> ${data.amount_correct}</p>
        <table class="results-table">
            <thead>
                <tr>
                    <th>Metric</th>
                    <th>Accuracy Values</th>
                    <th>Accuracy Value Avg</th>
                    <th>Aggregate Accuracy Value Avg</th>
                    <th>Accuracy Comparison</th>
                    <th>Latency Values</th>
                    <th>Latency Value Avg</th>
                    <th>Aggregate Latency Value Avg</th>
                    <th>Latency Comparison</th>
                </tr>
            </thead>
            <tbody>
                ${data.test_results.map(result => {
        let accuracyComparisonText = result.accuracy_comparison || "N/A";
        let latencyComparisonText = result.latency_comparison || "N/A";
        let accuracyColorStyle = '';  // Inline styles for color coding accuracy
        let latencyColorStyle = '';  // Inline styles for color coding latency

        // Apply color rules for accuracy comparison
        if (accuracyComparisonText === 'Above average') {
            accuracyColorStyle = 'color: green; font-weight: bold;';
        } else if (accuracyComparisonText === 'Below average') {
            accuracyColorStyle = 'color: red; font-weight: bold;';
        } else if (accuracyComparisonText === 'Average') {
            accuracyColorStyle = 'color: black; font-weight: bold;';
        }

        // Apply color rules for latency comparison
        if (latencyComparisonText === 'Above average') {
            latencyColorStyle = 'color: red; font-weight: bold;'; // Higher latency is worse
        } else if (latencyComparisonText === 'Below average') {
            latencyColorStyle = 'color: green; font-weight: bold;'; // Lower latency is better
        } else if (latencyComparisonText === 'Average') {
            latencyColorStyle = 'color: black; font-weight: bold;';
        }

        return `
                    <tr>
                        <td>${result.metric.replace(/_/g, ' ')}</td>
                        <td>${result.user_accuracy_values.join(", ")}</td>  <!-- Display all values -->
                        <td>${result.user_accuracy_average}</td>   <!-- Display user average -->
                        <td>${result.accuracy_average}</td>   <!-- Display aggregate average -->
                        <td style="${accuracyColorStyle}">  <!-- Apply inline color style for accuracy -->
                            ${accuracyComparisonText}
                        </td>
                        <td>${result.user_latency_values.join(", ")}</td>  <!-- Display all latency values -->
                        <td>${result.user_latency_average}</td>   <!-- Display user latency average -->
                        <td>${result.latency_average}</td>   <!-- Display aggregate latency average -->
                        <td style="${latencyColorStyle}">  <!-- Apply inline color style for latency -->
                            ${latencyComparisonText}
                        </td>
                    </tr>`;
    }).join('')}
            </tbody>
        </table>
    </div>
    <div class="table-container">
        <div class="aggregate-results-header">
            <h3>Aggregate Results (Ages: ${data.min_age}-${data.max_age})</h3>
        </div>
        <table class="results-table">
            <thead>
                <tr>
                    <th>Metric</th>
                    <th>Accuracy Average</th>
                    <th>Latency Average</th>
                </tr>
            </thead>
            <tbody>
                ${data.aggregate_results.map(result => `
                    <tr>
                        <td>${result.metric.replace(/_/g, ' ')}</td>
                        <td>${result.accuracy_average}</td>
                        <td>${result.latency_average}</td>
                    </tr>
                `).join('')}
            </tbody>
        </table>
    </div>
    <div class="results-buttons">
        <button onclick="backToTestResults()">Back to Test Results</button>
        <button id="exportToSpreadsheetBtn" onclick="exportToSpreadsheet(${testId})">Export to Spreadsheet</button>
    </div>
    `;

    // Check if the View as Graph button is already present
    if (!document.getElementById('viewGraphButton')) {
        const toggleButton = document.createElement("button");
        toggleButton.id = 'viewGraphButton'; // Add an ID to the button
        toggleButton.textContent = "View as Graph";
        toggleButton.onclick = () => toggleResultsView(testId, data);
        testContent.appendChild(toggleButton);
    }
}

function toggleResultsView(testId, data) {
    const testContent = document.getElementById('test-content');

    if (data) {
        currentTestData = data;
    }
    // If currently in the table view, switch to the graph view with latency chart as default
    if (testContent.querySelector('.results-table')) {
        testContent.innerHTML = `
            <div class="graph-main-header">
                <h2>Patient vs Aggregate Comparison</h2>
            </div>
            <div class="chart-toggle-buttons">
                <button onclick="loadLatencyChart(${testId})">Latency Comparison</button>
                <button onclick="loadAccuracyChart(${testId})">Accuracy Comparison</button>
            </div>
            <h2 id="chart-header"></h2>
            <canvas id="comparisonChart"></canvas>
            <div class="view-toggle-buttons">
                <button onclick="retrieveTestResults()">Back to Patient's Results Tab</button>
                <button onclick="toggleResultsView(${testId})">Back to Table View</button>
            </div>
        `;
        loadLatencyChart(testId);  // Load latency chart by default
    } else {
        // Switch back to table view
        if (currentTestData) {
            renderTestResultsTable(currentTestData, testId);
        } else {
            console.error("No test data found to render table view.");
        }
    }
}

// Map positions to the corresponding metric names
const metrics = [
    'fourdigit_1', 'fourdigit_2', 'fourdigit_3',
    'fivedigit_1', 'fivedigit_2', 'fivedigit_3',
    'fourmixed_1', 'fourmixed_2', 'fourmixed_3',
    'fivemixed_1', 'fivemixed_2', 'fivemixed_3'
];

// Function to determine the metric based on position
function getMetricForPosition(pos) {
    const position = parseInt(pos); // Ensure pos is treated as a number
    if (position >= 3 && position <= 5) return metrics[position - 3]; // fourdigit
    if (position >= 6 && position <= 8) return metrics[position - 3]; // fivedigit
    if (position >= 11 && position <= 13) return metrics[position - 5]; // fourmixed
    if (position >= 14 && position <= 16) return metrics[position - 5]; // fivemixed
    return `Metric ${pos}`; // Fallback for invalid positions
}

// Function to load latency comparison chart
function loadLatencyChart(testId) {
    fetch(`/get_test_comparison_data/${testId}/`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                document.getElementById('test-content').innerHTML = `<p style="color:red;">${data.error}</p>`;
                return;
            }

            // Set header for the chart
            const { min_age, max_age } = data.age_group;
            document.getElementById('chart-header').innerText = `Latency Comparison Graph (Ages: ${min_age} - ${max_age})`;

            
            const labels = Object.keys(data.patient.latencies || data.patient.accuracies)
                .map(pos => getMetricForPosition(pos));
            const patientLatencies = Object.values(data.patient.latencies);
            const aggregateLatencies = Object.values(data.aggregate.latencies);

            const ctx = document.getElementById('comparisonChart').getContext('2d');

            // Check if comparisonChart exists and has a destroy method
            if (window.comparisonChart && typeof window.comparisonChart.destroy === 'function') {
                window.comparisonChart.destroy();  // Destroy any existing chart instance
            }

            window.comparisonChart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [
                        {
                            label: 'Patient Latencies',
                            data: patientLatencies,
                            borderColor: 'rgb(75, 192, 192)',
                            backgroundColor: 'rgba(75, 192, 192, 0.2)',
                            fill: false,
                        },
                        {
                            label: 'Aggregate Latencies',
                            data: aggregateLatencies,
                            borderColor: 'rgb(153, 102, 255)',
                            backgroundColor: 'rgba(153, 102, 255, 0.2)',
                            fill: false,
                        }
                    ]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            position: 'top',
                        },
                    },
                    scales: {
                        x: {
                            title: {
                                display: true,
                                text: 'Metrics'
                            }
                        },
                        y: {
                            title: {
                                display: true,
                                text: 'Latency (ms)'
                            }
                        }
                    }
                }
            });
        })
        .catch(error => console.error('Error:', error));
}

// Function to load accuracy comparison chart
function loadAccuracyChart(testId) {
    fetch(`/get_test_comparison_data/${testId}/`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                document.getElementById('test-content').innerHTML = `<p style="color:red;">${data.error}</p>`;
                return;
            }

            // Set header for the chart
            const { min_age, max_age } = data.age_group;
            document.getElementById('chart-header').innerText = `Accuracy Comparison Graph (Ages: ${min_age} - ${max_age})`;

            const labels = Object.keys(data.patient.latencies || data.patient.accuracies)
                .map(pos => getMetricForPosition(pos));
            const patientAccuracies = Object.values(data.patient.accuracies);
            const aggregateAccuracies = Object.values(data.aggregate.accuracies);

            const ctx = document.getElementById('comparisonChart').getContext('2d');
            if (window.comparisonChart) {
                window.comparisonChart.destroy();  // Destroy any existing chart instance
            }
            window.comparisonChart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [
                        {
                            label: 'Patient Accuracies',
                            data: patientAccuracies,
                            borderColor: 'rgb(75, 192, 192)',
                            backgroundColor: 'rgba(75, 192, 192, 0.2)',
                            fill: false,
                        },
                        {
                            label: 'Aggregate Accuracies',
                            data: aggregateAccuracies,
                            borderColor: 'rgb(153, 102, 255)',
                            backgroundColor: 'rgba(153, 102, 255, 0.2)',
                            fill: false,
                        }
                    ]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            position: 'top',
                        },
                    },
                    scales: {
                        x: {
                            title: {
                                display: true,
                                text: 'Metrics'
                            }
                        },
                        y: {
                            title: {
                                display: true,
                                text: 'Accuracy (%)'
                            }
                        }
                    }
                }
            });
        })
        .catch(error => console.error('Error:', error));
}



function backToTestResults() {
    console.log('Navigating back to test results...');
    isViewingTest = false; // Reset view state
    toggleTestButtons();   // Make buttons visible again
    retrieveTestResults(); // Load test results
}

function toggleTestButtons() {
    const testButtons = document.querySelector('.test-buttons');
    const testStatusFilter = document.querySelector('.test-status-filter');
    const applyFilterButton = document.querySelector('.apply-filter-button');
    console.log('isViewingTest:', isViewingTest);
    if (testButtons) {
        testButtons.style.display = isViewingTest ? 'none' : 'block';
        console.log('Test buttons visibility:', testButtons.style.display);
    }
    if (testStatusFilter) {
        testStatusFilter.style.display = isViewingTest ? 'none' : 'block';
        console.log('Test filter visibility:', testStatusFilter.style.display);
    }
        if (applyFilterButton) {
        applyFilterButton.style.display = isViewingTest ? 'none' : 'block';
    }
}



function toggleTestStatusFilter(show) {
    const testStatusFilter = document.querySelector('.test-status-filter');
    const applyFilterButton = document.querySelector('.apply-filter-button');
    if (testStatusFilter) {
        testStatusFilter.style.display = show ? 'block' : 'none';
    }
    if (applyFilterButton) {
        applyFilterButton.style.display = show ? 'block' : 'none';
    }
}


async function exportToSpreadsheet(testId) {
    try {
        const response = await fetch(`/test_results/${testId}/`);
        const data = await response.json();

        const images = await getSpreadsheetImages(testId);
        
        if (!data) {
            console.error('No data received');
            return;
        }

        // Initialize a new workbook
        const workbook = new ExcelJS.Workbook();

        const addSheet = (workbook, sheetName, headers, rows) => {
            const sheet = workbook.addWorksheet(sheetName);
            const headerRow = sheet.addRow(headers);
            applyHeaderStyle(headerRow);

            rows.forEach((row, index) => {
                const rowObj = sheet.addRow(row);
                applyRowStyle(rowObj, index);
            });

            return sheet;
        };

        const applyHeaderStyle = (headerRow) => {
            headerRow.eachCell(cell => {
                cell.style = {
                    font: { bold: true },
                    alignment: { horizontal: 'center', vertical: 'middle' },
                    fill: { type: 'pattern', pattern: 'solid', fgColor: { argb: 'ff3c6d9e' } },
                    border: {
                        top: { style: 'thin' },
                        left: { style: 'thin' },
                        bottom: { style: 'double' },
                        right: { style: 'thin' }
                    }
                };
            });
        };

        const applyRowStyle = (rowObj, index) => {
            rowObj.eachCell(cell => {
                if (index % 2 === 0) {
                    cell.style.fill = { type: 'pattern', pattern: 'solid', fgColor: { argb: 'FFF8F8F8' } };
                } else {
                    cell.style.fill = { type: 'pattern', pattern: 'solid', fgColor: { argb: 'FFFFFFFF' } };
                }

                cell.style.alignment = { horizontal: 'center', vertical: 'middle' };

                cell.style.border = {
                    top: { style: 'thin' },
                    left: { style: 'thin' },
                    bottom: { style: 'thin' },
                    right: { style: 'thin' }
                };
            });
        };

        // Patient Test Results Sheet
        const patientResultsHeaders = [
            'Stimulus Type', 'Stimulus Question', 'Stimulus Correct Answer', 'Patient Response',
            'Patient First Character', 'Latency for First Character', 'Accuracy for First Character',
            'Patient Second Character', 'Latency for Second Character', 'Accuracy for Second Character',
            'Patient Third Character', 'Latency for Third Character', 'Accuracy for Third Character',
            'Patient Fourth Character', 'Latency for Fourth Character', 'Accuracy for Fourth Character',
            'Patient Fifth Character', 'Latency for Fifth Character', 'Accuracy for Fifth Character'
        ];

        const patientResultsRows = data.stimuli_responses
            .filter(item => !item.stimulus_type.toLowerCase().includes("pr"))
            .map((item, index) => {
                const stimulusType = item.stimulus_type || "N/A";
                const stimulusQuestion = item.stimulus_content || "N/A";
                const correctAnswer = item.correct_answer || "N/A";
                const patientResponse = item.response || "N/A";

                const patientResponseChars = patientResponse.split('');

                const accuracyValues = data.test_results[index]?.user_accuracy_values || [];
                const latencyValues = data.test_results[index]?.user_latency_values || [];

                const row = [
                    stimulusType,
                    stimulusQuestion,
                    correctAnswer,
                    patientResponse
                ];

                for (let i = 0; i < 5; i++) {
                    const character = patientResponseChars[i] || "";

                    const latency = latencyValues[i] !== undefined ? `${(latencyValues[i] / 1000).toFixed(2)} seconds`: ""; //Converted to seconds.
                    const accuracy = accuracyValues[i] !== undefined ? accuracyValues[i] : "";

                    row.push(character, latency, accuracy);
                }

                return row;
            });

        addSheet(workbook, 'Patient Results', patientResultsHeaders, patientResultsRows);

        // Aggregate Results Sheet
        const aggregateResultsHeaders = ['Metric', 'Latency Average', 'Accuracy Average'];
        const aggregateResultsRows = data.aggregate_results.map(result => [
            result.metric.replace(/_/g, ' '),
            result.latency_average !== null ? `${(result.latency_average / 1000).toFixed(2)} seconds` : "0 seconds",
            result.accuracy_average !== null ? result.accuracy_average : 0,
        ]);
        addSheet(
            workbook, 
            `Aggregate Results ${data.min_age}-${data.max_age}`, 
            aggregateResultsHeaders, 
            aggregateResultsRows
        );

        
        // Comparison Results Sheet
        const comparisonResultsHeaders = [
            'Metric', 'Patient Accuracy Average', 'Aggregate Accuracy Average', 
            'Accuracy Comparison', 'Patient Latency Average', 'Aggregate Latency Average', 
            'Latency Comparison'
        ];
        const comparisonResultsRows = data.test_results.map(result => [
            result.metric.replace(/_/g, ' '),
            result.user_accuracy_average || "N/A",
            result.accuracy_average || "N/A",
            result.accuracy_comparison || "N/A",
            result.user_latency_average || "N/A",
            result.latency_average || "N/A",
            result.latency_comparison || "N/A"
        ]);
        const comparisonSheet = addSheet(workbook, 'Comparison Results', comparisonResultsHeaders, comparisonResultsRows);

        const applyColorFormat = (sheet, row, column, comparisonValue, isLatency) => {
            const cell = sheet.getCell(row, column);
        
            // Determine the color based on the type (latency or accuracy)
            if (isLatency) {
                // Green for below average, red for above average
                if (comparisonValue === 'Below average') {
                    cell.style.fill = { type: 'pattern', pattern: 'solid', fgColor: { argb: 'FF00FF00' } };
                } else if (comparisonValue === 'Above average') {
                    cell.style.fill = { type: 'pattern', pattern: 'solid', fgColor: { argb: 'FFFF0000' } };
                }
            } else {
                // Green for above average, red for below average
                if (comparisonValue === 'Above average') {
                    cell.style.fill = { type: 'pattern', pattern: 'solid', fgColor: { argb: 'FF00FF00' } };
                } else if (comparisonValue === 'Below average') {
                    cell.style.fill = { type: 'pattern', pattern: 'solid', fgColor: { argb: 'FFFF0000' } };
                }
            }
        
            // Gray for 'Average'
            if (comparisonValue === 'Average') {
                cell.style.fill = { type: 'pattern', pattern: 'solid', fgColor: { argb: 'FF808080' } };
            }
        };

        comparisonResultsRows.forEach((row, index) => {
            const accuracyComparison = row[3]; // Accuracy Comparison column
            if (['Below average', 'Above average', 'Average'].includes(accuracyComparison)) {
                applyColorFormat(comparisonSheet, index + 2, 4, accuracyComparison, false); // false for accuracy
            }
        
            const latencyComparison = row[6]; // Latency Comparison column
            if (['Below average', 'Above average', 'Average'].includes(latencyComparison)) {
                applyColorFormat(comparisonSheet, index + 2, 7, latencyComparison, true); // true for latency
            }
        });

        // Stimuli and Responses Sheet
        const stimuliResponsesHeaders = [
            'Stimulus ID', 'Stimulus Type', 'Stimulus Content', 
            'Correct Answer for Stimuli', 'Patient Response', 'Is Correct', 'Time Submitted'
        ];
        const stimuliResponsesRows = data.stimuli_responses.map(item => [
            item.stimulus_id,
            item.stimulus_type,
            item.stimulus_content,
            item.correct_answer,
            item.response,
            item.is_correct ? "Yes" : "No",
            item.time_submitted || "N/A"
        ]);
        stimuliResponsesRows.push([], ['Practice Correct', 'Actual Correct', 'Total Correct'], [
            data.practice_correct, 
            data.actual_correct, 
            data.total_correct
        ]);
        const accuracyImageId = workbook.addImage({
            base64: images[0], // Provide the base64 string of the image
            extension: 'png',   // Specify the image type (png, jpeg, etc.)
        });
        const latencyImageId = workbook.addImage({
            base64: images[1], // Provide the base64 string of the image
            extension: 'png',   // Specify the image type (png, jpeg, etc.)
        });

        comparisonSheet.addImage(accuracyImageId, {
            tl: { col: 1, row: 15 }, // Top-left corner (column 1, row 1)
            ext: { width: 640, height: 480 }, // Dimensions of the image
        });
        comparisonSheet.addImage(latencyImageId, {
            tl: { col: 14, row: 15 }, // Top-left corner (column 1, row 1)
            ext: { width: 640, height: 480 }, // Dimensions of the image
        });
        addSheet(workbook, 'Stimuli and Responses', stimuliResponsesHeaders, stimuliResponsesRows);
        
        // Completed Patient Tests Sheet
        const completedTestsHeaders = [
            'Test ID', 'Test Link', 'Patient Age', 'Administered By', 
            'Created At', 'Started At', 'Finished At', 'Completion Time'
        ];
        const completedTestsRows = data.completed_tests.map(test => [
            test.id,
            test.link,
            test.age,
            test.user__username,
            test.created_at,
            test.started_at,
            test.finished_at,
            test.completion_time || "N/A"
        ]);
        addSheet(workbook, 'Completed Patient Tests', completedTestsHeaders, completedTestsRows);

        // Pending Patient Tests Sheet
        const pendingTestsHeaders = [
            'Test ID', 'Test Link', 'Patient Age', 'Administered By', 
            'Created At', 'Expiration Date', 'Time Remaining'
        ];
        const pendingTestsRows = data.pending_tests.map(test => [
            test.id,
            test.link,
            test.age,
            test.user__username,
            test.created_at,
            test.expiration_date,
            test.time_remaining
        ]);
        addSheet(workbook, 'Pending Patient Tests', pendingTestsHeaders, pendingTestsRows);

        // Invalid Patient Tests Sheet
        const invalidTestsHeaders = [
            'Test ID', 'Test Link', 'Patient Age', 'Administered By', 
            'Created At', 'Invalidated At', 'Time Since Invalid'
        ];
        const invalidTestsRows = data.invalid_tests.map(test => [
            test.id,
            test.link,
            test.age,
            test.user__username,
            test.created_at,
            test.invalidated_at,
            test.time_since_invalid
        ]);
        addSheet(workbook, 'Invalid Patient Tests', invalidTestsHeaders, invalidTestsRows);

        const sheets = workbook.worksheets;
        sheets.forEach(sheet => {
            sheet.columns.forEach(column => {
                let maxLength = 0;
                column.eachCell({ includeEmpty: true }, (cell) => {
                    const length = cell.value ? cell.value.toString().length : 0;
                    maxLength = Math.max(maxLength, length);
                });
                column.width = maxLength + 2;
            });
        });

        // Save workbook as a Blob and trigger download
        const buffer = await workbook.xlsx.writeBuffer();
        const blob = new Blob([buffer], { type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" });
        const link = document.createElement('a');
        link.href = URL.createObjectURL(blob);
        link.download = `TestResults_${data.test_link}.xlsx`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    } catch (error) {
        console.error('Error exporting spreadsheet:', error);
    }
}


// Function to save account changes for the user.
function saveAccountChanges() {
    const firstName = document.getElementById('first-name').value;
    const lastName = document.getElementById('last-name').value;
    const email = document.getElementById('email').value;
    const currentPassword = document.getElementById('current-password').value;
    const newPassword = document.getElementById('new-password').value;
    const accountMessage = document.getElementById('account-message');
    const accountErrorMessage = document.getElementById('account-error-message');

    // Create form data object
    const formData = new FormData();
    formData.append('first_name', firstName);
    formData.append('last_name', lastName);
    formData.append('email', email);
    formData.append('current_password', currentPassword);
    formData.append('new_password', newPassword);

    fetch('/update_account/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: formData
    })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                accountErrorMessage.textContent = data.error;
                accountErrorMessage.style.display = 'block';
                accountMessage.style.display = 'none';
            } else {
                accountMessage.textContent = 'Account updated successfully!';
                accountMessage.style.display = 'block';
                accountErrorMessage.style.display = 'none';
            }
        })
        .catch(error => console.error('Error:', error));
}

// Function to get user information
function getUserInfo() {
    fetch('/get_user_info/', {
        method: 'GET',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'), // Ensure CSRF protection, if needed
        },
    })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                console.error(data.error);
            } else {
                // Populate the fields with user info
                document.getElementById('first-name').value = data.first_name || '';
                document.getElementById('last-name').value = data.last_name || '';
                document.getElementById('email').value = data.email || '';
            }
        })
        .catch(error => {
            console.error('Error fetching user info:', error);
        });
}

// Enable dragging for the notification popout
let isDragging = false;
let offsetX, offsetY;

const notificationPopout = document.getElementById('notification-popout');
const notificationHeader = document.querySelector('.notification-header');
const notificationBody = document.getElementById('notification-body');
const notificationList = document.getElementById('notification-list');

notificationHeader.addEventListener('mousedown', (e) => {
    isDragging = true;
    offsetX = e.clientX - notificationPopout.offsetLeft;
    offsetY = e.clientY - notificationPopout.offsetTop;
    notificationPopout.style.cursor = 'move';
});

document.addEventListener('mousemove', (e) => {
    if (isDragging) {
        notificationPopout.style.left = `${e.clientX - offsetX}px`;
        notificationPopout.style.top = `${e.clientY - offsetY}px`;
    }
});

document.addEventListener('mouseup', () => {
    isDragging = false;
    notificationPopout.style.cursor = 'default';
});

var isNotificationsOpen = false;
var lastNotifLoadType = 'read'

// Close notifications with the close button
function closeNotifications() {
    notificationPopout.classList.remove('show');
    notificationBody.classList.remove('show');
    notificationList.classList.remove('show');
    isNotificationsOpen = notificationPopout.classList.contains('show');
}

// Show or hide the notification popout
function toggleNotifications(event) {
    // Prevent the default action of the anchor tag
    event.preventDefault();

    //Load notifications if visible
    if (!isNotificationsOpen) {
        loadNotifications("unread");
    }

    // Toggle the "show" class for each element
    notificationPopout.classList.toggle('show');
    notificationBody.classList.toggle('show');
    notificationList.classList.toggle('show');

    // Update the isNotificationsOpen variable based on the visibility of the popout
    isNotificationsOpen = notificationPopout.classList.contains('show');
    console.log("Popout visibility:", notificationPopout.classList.contains('show'));



}



function update_notifications(event) {
    const action = event.target.getAttribute('data-action');
    //whether we want to load show just unread notifications or read notifications
    loadNotifications(action);
    if (action == 'unread') {
        document.getElementById('unread-tab').classList.add('active');
        document.getElementById('read-tab').classList.remove('active');
    }
    else if (action == 'read') {
        document.getElementById('unread-tab').classList.remove('active');
        document.getElementById('read-tab').classList.add('active');
    }
}
// function that loads in notifications based on the current logged in user
function loadNotifications(loadType) {
    const notificationList = document.getElementById('notification-list');
    if (!(lastNotifLoadType == loadType)) {
        notificationList.innerHTML = '';
    }

    fetch(`/get_user_notifications/${loadType}`)
        .then(response => response.json())
        .then(data => {
            const notifications = data.notifications;
            if (notifications.length === 0) {
                if (loadType == 'unread') {
                    notificationList.innerHTML = '<li> No new Notifications </li>';
                }
                else {
                    notificationList.innerHTML = '<li> No Notifications </li>';
                }
            } else if (!(lastNotifLoadType == loadType)) {
                notifications.forEach(notif => {

                    const notifItem = document.createElement('li');

                    const separator = document.createElement('li');
                    notifItem.className = 'separator';
                    notificationList.appendChild(separator);

                    const notificationTime = new Date(notif.time_created);
                    const now = new Date();

                    const current_date = now.getDate() + now.getMonth() + now.getFullYear()
                    const notif_date = notificationTime.getDate() + notificationTime.getMonth() + notificationTime.getFullYear()

                    const dateSpan = document.createElement('span');
                    if (current_date == notif_date) {
                        dateSpan.textContent = `Today at ${new Date(notif.time_created).toLocaleString([], { hour: 'numeric', minute: '2-digit' })}`;
                    }
                    else {
                        dateSpan.textContent = `${new Date(notif.time_created).toLocaleString([], { year: '2-digit', month: '2-digit', day: '2-digit', hour: 'numeric', minute: '2-digit' })}`;
                    }

                    const headerSpan = document.createElement('span');
                    headerSpan.textContent = `${notif.header}`;
                    headerSpan.style.fontWeight = 'bold';

                    const messageSpan = document.createElement('span');
                    messageSpan.textContent = `${notif.message}`;

                    notifItem.appendChild(dateSpan);
                    notifItem.appendChild(document.createElement('br'));
                    notifItem.appendChild(headerSpan);
                    notifItem.appendChild(document.createElement('br'));
                    notifItem.appendChild(messageSpan);
                    notifItem.appendChild(document.createElement('br'));
                    if (notif.is_read) {
                        const archiveButton = document.createElement(`button`);
                        archiveButton.textContent = 'Archive';
                        archiveButton.onclick = () => dismissNotification(notif.id, notifItem);
                        notifItem.appendChild(archiveButton);
                    }
                    else {
                        const archiveButton = document.createElement(`button`);
                        archiveButton.textContent = 'Archive';
                        archiveButton.style.marginRight = '5px';
                        archiveButton.onclick = () => dismissNotification(notif.id, notifItem);
                        notifItem.appendChild(archiveButton);
                        const readButton = document.createElement(`button`);
                        readButton.textContent = 'Mark as Read';
                        readButton.onclick = () => markAsRead(notif.id, notifItem);
                        notifItem.appendChild(readButton);
                    }

                    notificationList.appendChild(notifItem);
                });
            }

            if (lastNotifLoadType == 'read' && loadType != 'read') {
                lastNotifLoadType = 'unread';
            } else if (lastNotifLoadType == 'unread' && loadType != 'unread') {
                lastNotifLoadType = 'read';
            }
        })
        .catch(error => console.error('Error:', error));
}

// removes the notification based on the notifItem corrisponding to the button that was pressed
function dismissNotification(id, notifItem) {
    const notificationList = document.getElementById('notification-list');
    notificationList.removeChild(notifItem);

    fetch(`/dismiss_notification/${id}/`, {
        method: 'PATCH',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: JSON.stringify({ is_archived: true })
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('failed to dismiss notification')
            }
        })
        .catch(error => console.error('Error updating notification', error))
}
// marks the notification as read based on the notifItem corrisponding to the button that was pressed
function markAsRead(id, notifItem) {
    const notificationList = document.getElementById('notification-list');
    notificationList.removeChild(notifItem);

    fetch(`/mark_as_read/${id}/`, {
        method: 'PATCH',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: JSON.stringify({ is_read: true })
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('failed to mark the notification as read')
            }
        })
        .catch(error => console.error('Error updating notification', error))
}

async function getSpreadsheetImages(testId) {
    try {
        const response = await fetch(`/create_result_charts/${testId}/`);
        const data = await response.json();
    
        const accuracyChartBase64 = data.accuracy_chart;
        const latencyChartBase64 = data.latency_chart;
    
        const accuracyImage = `data:image/png;base64,${accuracyChartBase64}`;
        const latencyImage = `data:image/png;base64,${latencyChartBase64}`;
    
        return [accuracyImage,latencyImage];
    } catch (error) {
        console.error('Error fetching images:', error);
        throw error;
    }
}

window.addEventListener('load', () => {
    // Get the current section from localStorage
    const currentSection = localStorage.getItem('currentSection') || 'dashboard' // Default to 'dashboard' if not found
    loadContent(currentSection);
});