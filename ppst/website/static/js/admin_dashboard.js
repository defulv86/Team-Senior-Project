// Load content dynamically based on selected tab
function loadContent(section) {
    const dynamicContent = document.getElementById('dynamic-content');

    if (section === 'dashboard') {
        dynamicContent.innerHTML = `
            <h2>Dashboard</h2>
            <p>Overview of recent activity and statistics will be displayed here.</p>
        `;
    } else if (section === 'support') {
        dynamicContent.innerHTML = `
            <h2>Support Tickets</h2>
            <div id="support-section">
                <div id="ticket-list">
                    <h3>Your Tickets</h3>
                    <ul id="ticket-items"></ul>
                </div>
            </div>
        `;
        loadUserTickets();
    } else if (section === 'registrationreview') {
        dynamicContent.innerHTML = `
            <h2>Registration Review</h2>
            <div id="registration-list">
                <ul id="registration-items"></ul>
            </div>
        `;
        loadRegistrationRequests();
    }
}

// Function to load the user's support tickets
function loadUserTickets() {
    const ticketList = document.getElementById('ticket-items');
    ticketList.innerHTML = '';  // Clear the list

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

