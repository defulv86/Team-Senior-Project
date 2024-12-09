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
    if (section === 'dashboard') {
        setCurrentSection('dashboard');
        Promise.all([checkForNewNotifications(), getUserName()]).then(([notificationCount, user]) => {
            dynamicContent.innerHTML = `
                <h2>Dashboard</h2>
                <p>Welcome back, ${user.username}.</p>
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
    } else if (section === 'support') {
        setCurrentSection('support');
        dynamicContent.innerHTML = `
            <h2>Support Tickets</h2>
            <div id="support-section">
                <label for="sort-select">Sort by:</label>
                <select id="sort-select" onchange="loadUserTickets(this.value)">
                    <option value="created_at">Date Created</option>
                    <option value="category">Category</option>
                    <option value="user__username">Submitted By</option>
                </select>
                <label for="status-select">Filter by Status:</label>
                <select id="status-select" onchange="loadUserTickets('created_at', this.value)">
                    <option value="">All</option>
                    <option value="open">Open</option>
                    <option value="in_progress">In Progress</option>
                    <option value="closed">Closed</option>
                </select>
                <div id="ticket-list">
                    <ul id="ticket-items"></ul>
                </div>
            </div>
        `;
        loadUserTickets();
    } else if (section === 'registrationreview') {
        setCurrentSection('registrationreview');
        dynamicContent.innerHTML = `
            <h2>Registration Review</h2>
            <div id="registration-list">
                <ul id="registration-items"></ul>
            </div>
        `;
        loadRegistrationRequests();
    }
    closeNotifications();
}

function updateTicketStatus(ticketId, newStatus) {
    fetch(`/update_ticket_status/${ticketId}/`, {
        method: 'PATCH',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: JSON.stringify({ status: newStatus }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert(`Ticket status updated to ${data.status}.`);
            loadUserTickets(); // Reload the ticket list
        } else {
            alert('Error updating ticket status: ' + (data.error || 'Unknown error.'));
        }
    })
    .catch(error => console.error('Error:', error));
}

// Enhance ticket rendering to include status dropdown
function loadUserTickets(sortBy = 'created_at', statusFilter = '') {
    const ticketList = document.getElementById('ticket-items');
    ticketList.innerHTML = ''; // Clear the list

    fetch(`/admin_tickets/?sort_by=${sortBy}&status=${statusFilter}`)
        .then(response => response.json())
        .then(data => {
            if (data.length === 0) {
                ticketList.innerHTML = '<li>No tickets found.</li>';
            } else {
                data.forEach(ticket => {
                    const ticketItem = document.createElement('li');
                    ticketItem.innerHTML = `
                        <div><strong>Created by:</strong> ${ticket.user__username}</div>
                        <div><strong>Category:</strong> ${ticket.category}</div>
                        <div><strong>Description:</strong> ${ticket.description}</div>
                        <div><strong>Submitted:</strong> ${new Date(ticket.created_at).toLocaleString()}</div>
                        <div>
                            <strong>Status:</strong>
                            <select onchange="updateTicketStatus(${ticket.id}, this.value)">
                                <option value="open" ${ticket.status === 'open' ? 'selected' : ''}>Open</option>
                                <option value="in_progress" ${ticket.status === 'in_progress' ? 'selected' : ''}>In Progress</option>
                                <option value="closed" ${ticket.status === 'closed' ? 'selected' : ''}>Closed</option>
                            </select>
                        </div>
                    `;
                    ticketList.appendChild(ticketItem);
                });
            }
        })
        .catch(error => console.error('Error:', error));
}

function markTicketCompleted(ticketId) {
    fetch(`/complete_ticket/${ticketId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Ticket marked as completed.');
            loadUserTickets();
        } else {
            alert('Error marking ticket as completed.');
        }
    })
    .catch(error => console.error('Error:', error));
}

// Function to load registration requests
function loadRegistrationRequests() {
    const registrationList = document.getElementById('registration-items');
    registrationList.innerHTML = '';  // Clear the list

    fetch('/get_registration_requests/')
        .then(response => response.json())
        .then(data => {
            if (data.length === 0) {
                registrationList.innerHTML = '<li>No registration requests found.</li>';
            } else {
                data.forEach(request => {
                    const listItem = document.createElement('li');
                    listItem.innerHTML = `
                        Username: ${request.username}
                        <button class="btn-green" onclick="approveRegistration(${request.id})">Approve</button>
                        <button class="btn-red" onclick="denyRegistration(${request.id})">Deny</button>
                    `;
                    registrationList.appendChild(listItem);
                });
            }
        })
        .catch(error => console.error('Error:', error));
}

// Function to approve a registration request
function approveRegistration(registrationId) {
    fetch(`/approve_registration/${registrationId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert("Registration approved.");
            loadRegistrationRequests();
        } else {
            alert("Error approving registration.");
        }
    })
    .catch(error => console.error('Error:', error));
}

// Function to deny a registration request
function denyRegistration(registrationId) {
    fetch(`/deny_registration/${registrationId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert("Registration denied.");
            loadRegistrationRequests();
        } else {
            alert("Error denying registration.");
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

window.addEventListener('load', () => {
    // Get the current section from localStorage
    const currentSection = localStorage.getItem('currentSection') || 'dashboard' // Default to 'dashboard' if not found
    loadContent(currentSection);
});