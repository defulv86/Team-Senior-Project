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
// Function to view test results for a completed test.
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
    document.getElementById('notification-popout').style.display = 'none';
    document.getElementById('notification-body').style.display = 'none';
    document.getElementById('notification-list').style.display = 'none';
}

// Show or hide the notification popout
function toggleNotifications(event) {
    // Prevent the default action of the anchor tag
    event.preventDefault();
    
    //Load notifications if visible
    if (!isNotificationsOpen) {
        loadNotifications();
    }

    // Toggle the display of the notification popout
    const notificationPopout = document.getElementById('notification-popout');
    notificationPopout.style.display = 
    notificationPopout.style.display === 'block' ? 'none' : 'block';
    
    const notificationBody = document.getElementById('notification-body');
    notificationBody.style.display = 
    notificationBody.style.display === 'block' ? 'none' : 'block';

    const notificationList = document.getElementById('notification-list');
    notificationList.style.display = 
    notificationList.style.display === 'block' ? 'none' : 'block';
    
    // Update the isNotificationsOpen variable based on the visibility of the popout
    isNotificationsOpen = notificationPopout.style.display === 'block';
}
isNotificationsOpen = false;

// function that loads in notifications based on the current logged in user
function loadNotifications(){
    const notificationList = document.getElementById('notification-list');
    notificationList.innerHTML = '';


    fetch('/get_user_notifications/')
    .then(response => response.json())
    .then(data => {
        if (data.length === 0) {
            notificationList.innerHTML = '<li> No new Notifications </li>';
        } else {
            data.forEach(notif => {
                if (notif.is_dismissed == false) {
                    
                    const notifItem = document.createElement('li');

                    const separator = document.createElement('li');
                    notifItem.className = 'separator';
                    notificationList.appendChild(separator);
    
                    const notificationTime = new Date(notif.time_created);
                    const now = new Date();
                
                    // Calculate the time difference in milliseconds
                    const timeDiff = now - notificationTime;
                    const hoursDiff = timeDiff / (1000 * 60 * 60); //convert to hours
                    
                    const dateSpan = document.createElement('span');
                    if (hoursDiff < 24) {
                        dateSpan.textContent = `Today at ${new Date(notif.time_created).toLocaleString([], { hour: 'numeric', minute: '2-digit' })}`;
                    }
                    else{
                        dateSpan.textContent = `${new Date(notif.time_created).toLocaleString()}`;
                    }

                    const headerSpan = document.createElement('span');
                    headerSpan.textContent = `${notif.header}`;
                    headerSpan.style.fontWeight = 'bold';
    
                    const messageSpan = document.createElement('span');
                    messageSpan.textContent = `${notif.message}`;
    
                    const dismissButton = document.createElement(`button`);
                    dismissButton.textContent = 'Dismiss';
                    dismissButton.onclick = () => dismissNotification(notif.id, notifItem);

                    notifItem.appendChild(dateSpan);
                    notifItem.appendChild(document.createElement('br'));
                    notifItem.appendChild(headerSpan);
                    notifItem.appendChild(document.createElement('br'));
                    notifItem.appendChild(messageSpan);
                    notifItem.appendChild(document.createElement('br'));
                    notifItem.appendChild(dismissButton);
                    
                    notificationList.appendChild(notifItem);
                }
            });
        }
    })
    .catch(error => console.error('Error:', error));    
}

// removes the notification based on the notifItem corrisponding to the button that was pressed
function dismissNotification(id ,notifItem){
    const notificationList = document.getElementById('notification-list');
    notificationList.removeChild(notifItem);

    fetch(`/dismiss_notification/${id}/`,{
        method: 'PATCH',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: JSON.stringify({ is_dismissed: true })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('failed to dismiss notification')
        }
    })
    .catch(error => console.error('Error updating notification', error))
}

// Automatically load the "Dashboard" tab when the page is first loaded
window.addEventListener('load', () => {
    loadContent('dashboard');
});

