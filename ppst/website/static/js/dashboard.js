// Load content dynamically based on selected tab
function loadContent(section) {
    const dynamicContent = document.getElementById('dynamic-content');
    
    if (section === 'account') {
        dynamicContent.innerHTML = `
            <h2>My Account</h2>
            <p>Manage your account details, such as changing your password, updating your email, or editing your profile information.</p>
        `;
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
                    <form id="ticketForm">
                        <label for="category">Category:</label>
                        <select id="category" required>
                            <option value="general">General Issue</option>
                            <option value="technical">Technical Issue</option>
                            <option value="account">Account Management</option>
                            <option value="bug/error">Bug/Error Report</option>
                        </select>
                        <label for="description">Issue Description:</label>
                        <textarea id="description" rows="4" required></textarea>
                        <button type="button" onclick="submitTicket()">Submit Ticket</button>
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

    // Ensure the form is not empty
    if (!category || !description) {
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

function generateTestLink() {
    const age = document.getElementById('patient-age').value;
    const linkContainer = document.getElementById('generated-link');

    if (age) {
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
            const testLink = data.test_link;
            linkContainer.innerHTML = `<p>Here is the link to your patient's unique test:</p>
                                       <a href="${testLink}" target="_blank">${testLink}</a>`;
        })
        .catch(error => console.error('Error:', error));
    } else {
        linkContainer.innerHTML = `<p style="color: red;">Invalid: Please enter a valid age.</p>`;
    }
}
function retrieveTestResults() {
    const testContent = document.getElementById('test-content');
    testContent.innerHTML = '<h2>Retrieve Patient Test Results</h2>';

    fetch('/get_test_results/')
    .then(response => response.json())
    .then(data => {
        data.tests.forEach(test => {
            let colorClass = 'gray-button';  // Default to in-progress
            if (test.status === 'complete') {
                colorClass = 'blue-button';
            } else if (test.status === 'invalid') {
                colorClass = 'red-button';
            }

            testContent.innerHTML += `
                <button class="${colorClass}" onclick="viewTestResults(${test.id})">
                    Test ID ${test.id} Results
                </button><br>`;
        });
    })
    .catch(error => console.error('Error:', error));
}

function viewTestResults(testId) {
    fetch(`/test_results/${testId}/`)
    .then(response => response.json())
    .then(data => {
        const testContent = document.getElementById('test-content');
        testContent.innerHTML = `
            <h2>Test Results for ID ${testId}</h2>
            <table>
                <thead>
                    <tr>
                        <th>Metric</th>
                        <th>Value</th>
                    </tr>
                </thead>
                <tbody>
                    ${data.results.map(result => `
                        <tr>
                            <td>${result.metric}</td>
                            <td>${result.value}</td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
            <button onclick="goBack()">Back to Tests</button>
        `;
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
    document.getElementById('notification-popout').style.display = 'none';
}

// Show or hide the notification popout
function toggleNotifications(event) {
    // Prevent the default action of the anchor tag
    event.preventDefault();

    // Toggle the display of the notification popout
    const notificationPopout = document.getElementById('notification-popout');
    notificationPopout.style.display = 
        notificationPopout.style.display === 'block' ? 'none' : 'block';

    // Update the isNotificationsOpen variable based on the visibility of the popout
    isNotificationsOpen = notificationPopout.style.display === 'block';
}

// Automatically load the "Dashboard" tab when the page is first loaded
window.addEventListener('load', () => {
    loadContent('dashboard');
});

