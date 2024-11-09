// Load content dynamically based on selected tab
function loadContent(section) {
    const dynamicContent = document.getElementById('dynamic-content');

    if (section === 'account') {
        dynamicContent.innerHTML = `
            <h2>My Account</h2>
            <form id="account-form">
                <label for="first-name">First Name:</label>
                <input type="text" id="first-name" name="first_name" required>
                <br>
                <label for="last-name">Last Name:</label>
                <input type="text" id="last-name" name="last_name" required>
                <br>
                <label for="email">Email:</label>
                <input type="email" id="email" name="email" required>
                <br>
                <label for="current-password">Current Password:</label>
                <input type="password" id="current-password" name="current_password" required>
                <br>
                <label for="new-password">New Password:</label>
                <input type="password" id="new-password" name="new_password">
                <br>
                <button type="button" onclick="saveAccountChanges()">Save Changes</button>
            </form>
            <div id="account-message" style="color: green;"></div>
            <div id="account-error-message" style="color: red; display: none;"></div>
        `;

        // calling getUserInfo() to populate the form with user info, such as first name, last name, and email.
        getUserInfo();
    } else if (section === 'dashboard') {
        dynamicContent.innerHTML = `
            <h2>Dashboard</h2>
            <p>Overview of recent activity, test statistics, and other relevant information will be displayed here.</p>
        `;
    } else if (section === 'tests') {
        dynamicContent.innerHTML = `
            <h2>Tests</h2>
            <div class="test-buttons">
                <button class="btn-create-test" onclick="createTest()">Create a New Test</button>
                <button class="btn-retrieve-results" onclick="retrieveTestResults()">Retrieve Patient Test Results</button>
            </div>
            <div id="test-content">
                <!-- Dynamic content for tests will be loaded here -->
            </div>
        `;
    } else if (section === 'support') {
        dynamicContent.innerHTML = `
            <h2>Support</h2>
            <div id="support-section">
                <div id="create-ticket">
                    <h3>Create a Support Ticket</h3>
                    <br>
                    <form id="ticketForm">
                        <label for="category">Category:</label>
                        <select id="category" required>
                            <option value="general">General Issue</option>
                            <option value="technical">Technical Issue</option>
                            <option value="account">Account Management</option>
                            <option value="bug/error">Bug/Error Report</option>
                        </select>
                        <br><br>
                        <label for="description">Issue Description:</label>
                        <br>
                        <textarea id="description" rows="4" required></textarea>
                        <br><br>
                        <button style="background-color: #0099ff; color: white;" type="button" onclick="submitTicket()">Submit Ticket</button>
                    </form>
                    <div id="error-message" style="color: red; display: none;"></div>
                </div>
                <div id="ticket-list">
                    <h3>Your Tickets</h3>
                    <ul id="ticket-items"></ul>
                </div>
            </div>
        `;
        loadUserTickets();
    }
}

// Function to submit a ticket
function submitTicket() {
    const category = document.getElementById('category').value;
    const description = document.getElementById('description').value;
    const errorMessage = document.getElementById('error-message');

    // Ensure the form is not empty or the description doesn't contain only spaces.
    if (!category || !description || description.trim() === "") {
        errorMessage.textContent = 'Please fill in all required fields.';
        errorMessage.style.display = 'block';
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
                errorMessage.textContent = data.error;
                errorMessage.style.display = 'block';
            } else {
                errorMessage.style.display = 'none';
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
                data.forEach(ticket => {
                    const ticketItem = document.createElement('li');
                    ticketItem.textContent = `Category: ${ticket.category}, Description: ${ticket.description}, Submitted: ${new Date(ticket.created_at).toLocaleString()}`;
                    ticketList.appendChild(ticketItem);
                });
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
    const testContent = document.getElementById('test-content');
    testContent.innerHTML = `
        <h2>Create a New Test</h2>
        <label for="patient-age">Please provide the patient's age:</label>
        <input type="number" id="patient-age" name="patient-age" required><br><br>
        <button onclick="generateTestLink()">Generate Test Link</button>
        <div id="generated-link"></div>
    `;
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
                    linkContainer.innerHTML = `<p>Here is the link to your patient's unique test:</p>
                                           <a href="${testLink}" target="_blank">${testLink}</a>`;
                }
            })
            .catch(error => console.error('Error:', error));
    } else {
        linkContainer.innerHTML = `<p style="color: red;">Invalid: Age must be 18 or older.</p>`;
    }
}

function retrieveTestResults() {
    const testContent = document.getElementById('test-content');
    testContent.innerHTML = `<h2>Retrieve Patient Test Results</h2>`;

    // Fetch the test results
    fetch('/get_test_results/')
        .then(response => response.json())
        .then(data => {
            data.tests.forEach(test => {
                let colorClass = 'incomplete';
                let onclickAttr = '';

                if (test.status === 'completed') {
                    colorClass = 'completed';
                    onclickAttr = `onclick="viewTestResults(${test.id})"`;
                } else if (test.status === 'invalid') {
                    colorClass = 'invalid';
                }

                testContent.innerHTML += `
                    <button class="${colorClass}" ${onclickAttr}>
                        Test ID ${test.id} | Link: ${test.link}
                    </button><br>
                `;
            });
        })
        .catch(error => console.error('Error:', error));
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
        <h2>Test Results for ID ${testId}</h2>
        <p><strong>Patient's Age:</strong> ${data.patient_age}</p>
        <p><strong>Amount Correct:</strong> ${data.amount_correct}</p>
        <table class="results-table">
            <thead>
                <tr>
                    <th>Metric</th>
                    <th>Result Values</th>
                    <th>Result Value Avg</th>
                    <th>Aggregate Avg</th>
                    <th>Comparison</th>
                </tr>
            </thead>
            <tbody>
                ${data.test_results.map(result => {
                    let comparisonText = result.comparison || "N/A";
                    let colorStyle = '';  // Inline styles for color coding

                    // Determine if the metric is for latency or accuracy
                    const isLatency = result.metric.toLowerCase().includes("latency");
                    const isAccuracy = result.metric.toLowerCase().includes("accuracy");

                    // Apply color rules based on metric type and comparison value
                    if (isLatency) {
                        // Latency: Above average = red, Below average = green
                        if (comparisonText === 'Above average') {
                            colorStyle = 'color: red; font-weight: bold;';
                        } else if (comparisonText === 'Below average') {
                            colorStyle = 'color: green; font-weight: bold;';
                        } else if (comparisonText === 'Average') {
                            colorStyle = 'color: black; font-weight: bold;';
                        }
                    } else if (isAccuracy) {
                        // Accuracy: Above average = green, Below average = red
                        if (comparisonText === 'Above average') {
                            colorStyle = 'color: green; font-weight: bold;';
                        } else if (comparisonText === 'Below average') {
                            colorStyle = 'color: red; font-weight: bold;';
                        } else if (comparisonText === 'Average') {
                            colorStyle = 'color: black; font-weight: bold;';
                        }
                    }

                    return `
                    <tr>
                        <td>${result.metric.replace(/_/g, ' ')}</td>
                        <td>${result.values.join(", ")}</td>  <!-- Display all values -->
                        <td>${result.average}</td>   <!-- Display user average -->
                        <td>${result.aggregate_average}</td>   <!-- Display aggregate average -->
                        <td style="${colorStyle}">  <!-- Apply inline color style here -->
                            ${comparisonText}
                        </td>
                    </tr>`;
                }).join('')}
            </tbody>
        </table>
    </div>
    <div class="table-container">
        <h3>Aggregate Results for Age Group ${data.min_age}-${data.max_age}</h3>
        <table class="results-table">
            <thead>
                <tr>
                    <th>Metric</th>
                    <th>Average</th>
                </tr>
            </thead>
            <tbody>
                ${data.aggregate_results.map(result => `
                    <tr>
                        <td>${result.metric.replace(/_/g, ' ')}</td>
                        <td>${result.average}</td>
                    </tr>
                `).join('')}
            </tbody>
        </table>
    </div>
    <button onclick="retrieveTestResults()">Back to Test Results</button>
    <button id="exportToSpreadsheetBtn" onclick="exportToSpreadsheet(${testId})">Export to Spreadsheet</button>
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
            <h2>Patient vs Aggregate Comparison</h2>
            <div class="chart-toggle-buttons">
                <button onclick="loadLatencyChart(${testId})">Latency Comparison</button>
                <button onclick="loadAccuracyChart(${testId})">Accuracy Comparison</button>
            </div>
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


// Function to load latency comparison chart
function loadLatencyChart(testId) {
    fetch(`/get_test_comparison_data/${testId}/`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                document.getElementById('test-content').innerHTML = `<p style="color:red;">${data.error}</p>`;
                return;
            }

            const labels = Object.keys(data.patient.latencies).map(pos => `Position ${pos}`);
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

            const labels = Object.keys(data.patient.accuracies).map(pos => `Position ${pos}`);
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
    isViewingTest = false; // Reset when going back
    toggleTestButtons(); // Show the test buttons again
    retrieveTestResults(); // Reload the test results list
}

// Function to toggle visibility of test buttons
function toggleTestButtons() {
    const testButtons = document.querySelector('.test-buttons');
    if (testButtons) {
        testButtons.style.display = isViewingTest ? 'none' : 'block';
    }
}

function exportToSpreadsheet(testId) {
    fetch(`/test_results/${testId}/`)
        .then(response => response.json())
        .then(data => {
            // Initialize workbook and worksheet
            const workbook = XLSX.utils.book_new();

            // Prepare Patient Test Results Sheet
            const patientResults = [
                ['Metric', 'Value', 'Average', 'Comparison']
            ];
            data.test_results.forEach(result => {
                patientResults.push([
                    result.metric.replace(/_/g, ' '),
                    result.value,
                    result.average || "N/A",
                    result.comparison
                ]);
            });

            // Add patient results to the workbook
            const patientSheet = XLSX.utils.aoa_to_sheet(patientResults);
            XLSX.utils.book_append_sheet(workbook, patientSheet, `Patient Results`);

            // Prepare Aggregate Results Sheet
            const aggregateResults = [
                ['Metric', 'Average']
            ];
            data.aggregate_results.forEach(result => {
                aggregateResults.push([
                    result.metric.replace("avg_", "").replace(/_/g, ' '),
                    result.average
                ]);
            });

            // Add aggregate results to the workbook
            const aggregateSheet = XLSX.utils.aoa_to_sheet(aggregateResults);
            XLSX.utils.book_append_sheet(workbook, aggregateSheet, `Aggregate Results`);

            // Export the workbook to a file
            XLSX.writeFile(workbook, `TestResults_${testId}.xlsx`);
        })
        .catch(error => console.error('Error:', error));
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

// Close notifications with the close button
function closeNotifications() {
    notificationPopout.classList.toggle('show');
    notificationBody.classList.toggle('show');
    notificationList.classList.toggle('show');
}
lastNotifLoadType = 'read'
// Show or hide the notification popout
function toggleNotifications(event) {
    // Prevent the default action of the anchor tag
    event.preventDefault();

    //Load notifications if visible
    if (!isNotificationsOpen) {
        loadNotifications("unread");
    }

    // Toggle the display of the notification popout
    const notificationPopout = document.getElementById('notification-popout');
    const notificationBody = document.getElementById('notification-body');
    const notificationList = document.getElementById('notification-list');
  
    // Toggle the "show" class for each element
    notificationPopout.classList.toggle('show');
    notificationBody.classList.toggle('show');
    notificationList.classList.toggle('show');
    
    // Update the isNotificationsOpen variable based on the visibility of the popout
    isNotificationsOpen = notificationPopout.classList.contains('show');
    console.log("Popout visibility:", notificationPopout.classList.contains('show'));
    

    
}

isNotificationsOpen = false;

function update_notifications(event) {
    const action = event.target.getAttribute('data-action');
    //whether we want to load show just unread notifications or read notifications
    loadNotifications(action);
    if(action == 'unread'){
        document.getElementById('unread-tab').classList.add('active');
        document.getElementById('read-tab').classList.remove('active');
    }
    else if(action == 'read'){
        document.getElementById('unread-tab').classList.remove('active');
        document.getElementById('read-tab').classList.add('active');
    }
}
// function that loads in notifications based on the current logged in user
function loadNotifications(loadType){
    const notificationList = document.getElementById('notification-list');
    if (!(lastNotifLoadType == loadType)){
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
            else{
                notificationList.innerHTML = '<li> No Notifications </li>';
            }
        } else if (!(lastNotifLoadType == loadType)){
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
                    else{
                        dateSpan.textContent = `${new Date(notif.time_created).toLocaleString([], {year:'2-digit', month:'2-digit', day:'2-digit', hour:'numeric', minute: '2-digit'})}`;
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
                    else{
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
        } else if(lastNotifLoadType == 'unread' && loadType != 'unread'){
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
function markAsRead(id ,notifItem){
    const notificationList = document.getElementById('notification-list');
    notificationList.removeChild(notifItem);

    fetch(`/mark_as_read/${id}/`,{
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

// Automatically load the "Dashboard" tab when the page is first loaded
window.addEventListener('load', () => {
    loadContent('dashboard');
});

