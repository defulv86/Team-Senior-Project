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
            <button onclick="createTest()">Create a Test</button>
            <button onclick="viewPreviousTests()">View Previous Tests</button>
        `;
    } else if (section === 'support') {
        dynamicContent.innerHTML = `
            <h2>Support</h2>
            <p>Need help? Here you can find resources, contact support, and get answers to frequently asked questions.</p>
        `;
    }
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
        // Simulate generating a unique test link
        const testLink = `www.test.com/${Math.random().toString(36).substr(2, 9)}`;
        linkContainer.innerHTML = `<p>Here is the link to your patient's unique test:</p>
                                   <a href="http://${testLink}" target="_blank">${testLink}</a>`;
    } else {
        linkContainer.innerHTML = `<p style="color: red;">Invalid: Please enter a valid age.</p>`;
    }
}

function retrieveTestResults() {
    const testContent = document.getElementById('test-content');
    testContent.innerHTML = `
        <h2>Retrieve Patient Test Results</h2>
        <ul class="test-list">
            <li class="completed">Retrieve Test ID a35OLw08s4 Test Results</li>
            <li class="invalid">Retrieve Test ID B5mDbS0d3s Test Results</li>
            <li class="completed">Retrieve Test ID f454fd5ds3s Test Results</li>
            <li class="completed">Retrieve Test ID Gp84rfB8SW Test Results</li>
            <li class="incomplete">Retrieve Test ID b6Ds29c9I6 Test Results</li>
            <li class="incomplete">Retrieve Test ID 65w45hG5ifc Test Results</li>
        </ul>
    `;
}


function goBack() {
    loadContent('tests');
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
function toggleNotifications() {
    notificationPopout.style.display = 
        notificationPopout.style.display === 'block' ? 'none' : 'block';
}


