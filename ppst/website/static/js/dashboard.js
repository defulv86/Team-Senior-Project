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
    const dynamicContent = document.getElementById('dynamic-content');
    dynamicContent.innerHTML = `
        <h2>Create a New Test</h2>
        <form>
            <label for="test-name">Test Name:</label>
            <input type="text" id="test-name" name="test-name" required><br><br>
            <label for="test-date">Test Date:</label>
            <input type="date" id="test-date" name="test-date" required><br><br>
            <button type="submit">Submit</button>
        </form>
        <button onclick="goBack()">Back</button>
    `;
}

function viewPreviousTests() {
    const dynamicContent = document.getElementById('dynamic-content');
    dynamicContent.innerHTML = `
        <h2>Previous Tests</h2>
        <ul>
            <li>Test 1 - Completed</li>
            <li>Test 2 - Invalid</li>
            <li>Test 3 - Completed</li>
            <!-- You could load actual test data here from the server -->
        </ul>
        <button onclick="goBack()">Back</button>
    `;
}

function goBack() {
    loadContent('tests');
}

function toggleNotifications() {
    const notificationPopout = document.getElementById('notification-popout');
    notificationPopout.style.display = 
        notificationPopout.style.display === 'block' ? 'none' : 'block';
}

function closeNotifications() {
    document.getElementById('notification-popout').style.display = 'none';
}

function markAllRead() {
    const notificationBody = document.getElementById('notification-body');
    notificationBody.innerHTML = `<p>All notifications are marked as read.</p>`;
}

function clearNotifications() {
    const notificationBody = document.getElementById('notification-body');
    notificationBody.innerHTML = `<p>No new notifications.</p>`;
}


