let stimuli = [];
let currentStimulusIndex = 0;
let response = ''; // Store the response from the keyboard
const timestamps = [];
const form = document.querySelector('form');

let introAudio = new Audio('/static/audio/Voiceover_Male1_Intro.mp3');
const stimulusAudioMap = {
    male1: {
        "intro": new Audio('/static/audio/Voiceover_Male1_Intro.mp3'),
        "1": new Audio('/static/audio/Voiceover_Male1_1.mp3'),
        "2": new Audio('/static/audio/Voiceover_Male1_2.mp3'),
        "3": new Audio('/static/audio/Voiceover_Male1_3.mp3'),
        "4": new Audio('/static/audio/Voiceover_Male1_4.mp3'),
        "5": new Audio('/static/audio/Voiceover_Male1_5.mp3'),
        "6": new Audio('/static/audio/Voiceover_Male1_6.mp3'),
        "F": new Audio('/static/audio/Voiceover_Male1_F.mp3'),
        "K": new Audio('/static/audio/Voiceover_Male1_K.mp3'),
        "L": new Audio('/static/audio/Voiceover_Male1_L.mp3'),
        "P": new Audio('/static/audio/Voiceover_Male1_P.mp3'),
        "R": new Audio('/static/audio/Voiceover_Male1_R.mp3'),
        "Y": new Audio('/static/audio/Voiceover_Male1_Y.mp3')
    },
    male2: {
        "intro": new Audio('/static/audio/Voiceover_Male2_Intro.mp3'),
        "1": new Audio('/static/audio/Voiceover_Male2_1.mp3'),
        "2": new Audio('/static/audio/Voiceover_Male2_2.mp3'),
        "3": new Audio('/static/audio/Voiceover_Male2_3.mp3'),
        "4": new Audio('/static/audio/Voiceover_Male2_4.mp3'),
        "5": new Audio('/static/audio/Voiceover_Male2_5.mp3'),
        "6": new Audio('/static/audio/Voiceover_Male2_6.mp3'),
        "F": new Audio('/static/audio/Voiceover_Male2_F.mp3'),
        "K": new Audio('/static/audio/Voiceover_Male2_K.mp3'),
        "L": new Audio('/static/audio/Voiceover_Male2_L.mp3'),
        "P": new Audio('/static/audio/Voiceover_Male2_P.mp3'),
        "R": new Audio('/static/audio/Voiceover_Male2_R.mp3'),
        "Y": new Audio('/static/audio/Voiceover_Male2_Y.mp3')
    },
    female1: {
        "intro": new Audio('/static/audio/Voiceover_Female1_Intro.mp3'),
        "1": new Audio('/static/audio/Voiceover_Female1_1.mp3'),
        "2": new Audio('/static/audio/Voiceover_Female1_2.mp3'),
        "3": new Audio('/static/audio/Voiceover_Female1_3.mp3'),
        "4": new Audio('/static/audio/Voiceover_Female1_4.mp3'),
        "5": new Audio('/static/audio/Voiceover_Female1_5.mp3'),
        "6": new Audio('/static/audio/Voiceover_Female1_6.mp3'),
        "F": new Audio('/static/audio/Voiceover_Female1_F.mp3'),
        "K": new Audio('/static/audio/Voiceover_Female1_K.mp3'),
        "L": new Audio('/static/audio/Voiceover_Female1_L.mp3'),
        "P": new Audio('/static/audio/Voiceover_Female1_P.mp3'),
        "R": new Audio('/static/audio/Voiceover_Female1_R.mp3'),
        "Y": new Audio('/static/audio/Voiceover_Female1_Y.mp3')
    },
    female2: {
        "intro": new Audio('/static/audio/Voiceover_Female2_Intro.mp3'),
        "1": new Audio('/static/audio/Voiceover_Female2_1.mp3'),
        "2": new Audio('/static/audio/Voiceover_Female2_2.mp3'),
        "3": new Audio('/static/audio/Voiceover_Female2_3.mp3'),
        "4": new Audio('/static/audio/Voiceover_Female2_4.mp3'),
        "5": new Audio('/static/audio/Voiceover_Female2_5.mp3'),
        "6": new Audio('/static/audio/Voiceover_Female2_6.mp3'),
        "F": new Audio('/static/audio/Voiceover_Female2_F.mp3'),
        "K": new Audio('/static/audio/Voiceover_Female2_K.mp3'),
        "L": new Audio('/static/audio/Voiceover_Female2_L.mp3'),
        "P": new Audio('/static/audio/Voiceover_Female2_P.mp3'),
        "R": new Audio('/static/audio/Voiceover_Female2_R.mp3'),
        "Y": new Audio('/static/audio/Voiceover_Female2_Y.mp3')
    }
};

// Current audio map by default: Male 1
let currentAudioMap = stimulusAudioMap['male1'];

document.addEventListener('DOMContentLoaded', () => {
    // Ensure the DOM is loaded before attaching event listeners
    const voiceProfileDropdown = document.getElementById('voice-profile');
    
    if (voiceProfileDropdown) {
        voiceProfileDropdown.addEventListener('change', function () {
            const selectedProfile = this.value;
            currentAudioMap = stimulusAudioMap[selectedProfile] || stimulusAudioMap['male1']; // Fallback to Male 1
        });
    } else {
        console.error('Voice profile dropdown not found in the DOM.');
    }
});

// Play Specific Stimulus Character Audio
function playCharacterAudio(character) {
    const characterAudio = currentAudioMap[character];
    if (characterAudio && typeof characterAudio.play === 'function') {
        characterAudio.pause();
        characterAudio.currentTime = 0;
        characterAudio.play();
    }
}


// Toggle Intro Audio
document.getElementById('speak-button').addEventListener('click', () => {
    const introAudio = currentAudioMap["intro"]; // Access intro audio dynamically
    if (introAudio && typeof introAudio.pause === 'function') {
        if (!introAudio.paused) {
            introAudio.pause();
            introAudio.currentTime = 0; // Reset for the next play
        } else {
            introAudio.play();
        }
    } else {
        console.error('Intro audio is not a valid Audio object.');
    }
});

form.addEventListener('submit', function (e) {
    e.preventDefault();
    var selectedFontSize = document.getElementById("fontSize").value;
    changeFontSize(selectedFontSize);
});

function changeFontSize(size) {
    document.getElementById("intro").style.fontSize = size;
}

function getFontSize() {
    return document.getElementById("fontSize").value;
}

// Check the test status when the page loads
document.addEventListener('DOMContentLoaded', () => {
    testLink = document.getElementById('test-link').value; // Retrieve the test link

    fetch(`/check-test-status/${testLink}/`)
        .then(response => response.json())
        .then(data => {
            if (data.status === 'completed') {
                window.location.href = '/completed/';
            }

            if (data.status === 'invalid') {
                window.location.href = '/errorpage/';
            }
        })
        .catch(error => {
            console.error('Error checking test status:', error);
        });
});

// Function to mark the test as complete in the backend
function markTestComplete(testLink) {
    testLink = document.getElementById('test-link').value; // Retrieve the test link
    fetch(`/mark-test-complete/${testLink}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                console.log('Test marked as complete.');
            }
        })
        .catch(error => {
            console.error('Error marking test as complete:', error);
        });
}

// Play Specific Stimulus Character Audio
function playCharacterAudio(character) {
    const characterAudio = currentAudioMap[character];
    if (characterAudio && typeof characterAudio.play === 'function') {
        characterAudio.pause();
        characterAudio.currentTime = 0;
        characterAudio.play();
    }
}

// Flash Stimulus
function flashStimulus(stimulus) {
    const stimulusDiv = document.getElementById('stimulus');
    const logoDiv = document.getElementById('logo');
    const digitKeyboard = document.getElementById('digit-keyboard');
    const alphanumericKeyboard = document.getElementById('alphanumeric-keyboard');
    const responseSection = document.getElementById('response-section');

    // Hide both keyboards and the response section initially
    digitKeyboard.style.display = 'none';
    logoDiv.style.display = 'block';
    alphanumericKeyboard.style.display = 'none';
    responseSection.style.display = 'none'; // Hide the response section

    const stimulusContent = stimulus.stimulus_content;
    let currentCharIndex = 0;

    const showNextChar = () => {
        if (currentCharIndex < stimulusContent.length) {
            const currentChar = stimulusContent[currentCharIndex];
            stimulusDiv.textContent = currentChar;
            playCharacterAudio(currentChar); // Play audio for the current character
            currentCharIndex++;
            setTimeout(showNextChar, 1500); // Show next character after 1.5 seconds
        } else {
            stimulusDiv.textContent = '';
            timestamps.push(performance.now());

            if (stimulus.stimulus_type.includes('Digit')) {
                digitKeyboard.style.display = 'flex';
            } else if (stimulus.stimulus_type.includes('Mixed')) {
                alphanumericKeyboard.style.display = 'flex';
            }
            responseSection.style.display = 'block';
        }
    };

    showNextChar();
}

// Add event listeners for keyboard buttons
document.querySelectorAll('.key').forEach(key => {
    key.addEventListener('click', () => {
        response += key.dataset.value;  // Append clicked key value
        timestamps.push(performance.now()); // Capture timestamp for each character entered
        console.log(response);
    });
});

function showPauseScreen(type ,message, callback) {
    const pauseScreen = document.getElementById('pause-screen');
    const messageDiv = document.getElementById('pause-message');
    const continueButton = document.getElementById('continue-button');
    const introVideoDiv =  document.getElementById('intro-video-div');
    const mixedVideoDiv =  document.getElementById('mixed-video-div');
    const introVideo = document.getElementById('intro-vid');
    const mixedVideo = document.getElementById('mixed-vid')

    messageDiv.textContent = message;
    pauseScreen.style.display = 'flex';

    if (type == "4_Span_Mixed_Pr") {
        mixedVideoDiv.style.display = 'block';
    } 
    else if (type == "4_Span_Digit_Pr") {
        introVideoDiv.style.display = 'block';
    }

    continueButton.onclick = function (event) {
        event.stopPropagation();
        pauseScreen.style.display = 'none';
        mixedVideoDiv.style.display = 'none';
        introVideoDiv.style.display = 'none';
        introVideo.pause();
        mixedVideo.pause();
        if (callback) callback();
    };
}

let shownTypes = new Set();
function nextStimulus() {
    if (currentStimulusIndex < stimuli.length) {
        const currentStimulus = stimuli[currentStimulusIndex];
        const stimulusType = currentStimulus.stimulus_type;

        if (['4_Span_Digit_Pr', '4_Span_Digit', '4_Span_Mixed_Pr', '4_Span_Mixed'].includes(stimulusType) && !shownTypes.has(stimulusType)) {
            shownTypes.add(stimulusType);
            const messageMap = {
                '4_Span_Digit_Pr': "When you proceed, you will see two digit practice stimuli.",
                '4_Span_Digit': "The actual test will now begin. You will now see six different digit stimuli. These results will be recorded.", // "six digit stimuli" by itself sounded a bit confusing and misleading in my opinion
                '4_Span_Mixed_Pr': "The next section includes mixed stimuli. Watch the video below for instructions on how to respond.",
                '4_Span_Mixed': "The actual test will now begin. You will now see six different mixed stimuli. These results will be recorded." // "six mixed stimuli" sounds a little less confusing but I changed it anyway for consistency
            };

            showPauseScreen(stimulusType, messageMap[stimulusType], () => {
                flashStimulus(currentStimulus);
                currentStimulusIndex++;
            });
        } else {
            flashStimulus(currentStimulus);
            currentStimulusIndex++;
        }

        response = '';
        timestamps.length = 0;

    } else {
        const stimulusElement = document.getElementById('stimulus');
        // First line of message
        stimulusElement.textContent = 'Congratulations on Completing Your Philadelphia Pointing Span Test.';
        stimulusElement.style.fontSize = '2.5em';
        stimulusElement.style.fontWeight = 'bolder';
        stimulusElement.style.fontFamily = 'Montserrat';
        stimulusElement.style.color = '#0077b3';
        stimulusElement.style.height = '250px';
    
        // Create a new element for the second line of text
        const additionalText = document.createElement('div');
        additionalText.innerHTML = 'You have successfully <b>completed</b> your <b>Philadelphia Pointing Span Test</b>. Your health provider has been notified of your updated test status. The results will be available for your health provider\'s review for further medical evaluation.';
        additionalText.style.fontSize = '32px'; // Adjusted font size
        additionalText.style.color = '#000000'; // Different color
        additionalText.style.fontFamily = 'Montserrat';
        additionalText.style.width = '70%';
        additionalText.style.textAlign = 'center';
        additionalText.style.marginTop = '-80px';
        additionalText.style.lineHeight = '1.6';
    
        // Append the new text to the parent of the stimulus element
        stimulusElement.parentNode.appendChild(additionalText);
    
        document.getElementById('response-section').style.display = 'none';


        markTestComplete();
    }
}


function get_correct_answer(stimulus) {
    if (stimulus.stimulus_type.includes('Digit')) {
        // Sort digits in numerical order
        return stimulus.stimulus_content.split('').sort((a, b) => a - b).join('');
    } else if (stimulus.stimulus_type.includes('Mixed')) {
        // Sort digits numerically and letters alphabetically
        const digits = stimulus.stimulus_content.split('').filter(char => !isNaN(char)).sort();
        const letters = stimulus.stimulus_content.split('').filter(char => isNaN(char)).sort();
        return digits.concat(letters).join('');
    }
    return '';
}

document.getElementById('submit-response').addEventListener('click', () => {
    if (!response) {
        alert('Please enter a response before submitting.');
        return;
    }

    const currentStimulus = stimuli[currentStimulusIndex - 1];
    const correctAnswer = get_correct_answer(currentStimulus);
    const characterLatencies = [];
    const accuracies = [];

    // Determine expected length based on stimulus type
    let expectedLength;
    if (currentStimulus.stimulus_type.includes('4_Span')) {
        expectedLength = 4;
    } else if (currentStimulus.stimulus_type.includes('5_Span')) {
        expectedLength = 5;
    }

    // Truncate response to expected length
    const truncatedResponse = response.slice(0, expectedLength);

    // Skip practice questions when counting correct answers
    const isPracticeQuestion = currentStimulus.stimulus_type.includes('_Pr');

    fetch('/submit-response/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            link: testLink,
            response_text: truncatedResponse,
            stimulus_id: currentStimulus.id,
            response_position: currentStimulusIndex,
            character_latencies: characterLatencies,
            character_accuracies: accuracies,
            expected_stimulus: correctAnswer,
            timestamps: timestamps,
            is_practice: isPracticeQuestion // Add a flag to identify practice questions
        })
    })
        .then(response => {
            if (!response.ok) {
                console.error('Error:', response.statusText);
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(() => {
            response = '';
            timestamps.length = 0;
            nextStimulus();
        })
        .catch(error => {
            console.error('There was a problem with the fetch operation:', error);
            alert('An error occurred while submitting your response. Please try again.');
        });
});

function playDemo() { // shows demo video and speaks/shows instructions
    var video = document.createElement("VIDEO");
    video.width = 420;
    video.height = 300;
    video.controls = true;
    video.src = "/static/images/IntroVideo.mp4"; // Static video path
    document.getElementById("demo_vid").appendChild(video); // shows video
    var titleText = document.getElementById("title").textContent;
    var welcomeText = document.getElementById("Welcome").textContent;
    speak(titleText);
    speak(welcomeText);

    var paragraph = document.getElementById("P");
    paragraph.style.color = "#0077b3";
    paragraph.style.fontFamily = "Open Sans";
    paragraph.style.fontWeight = "bold";
    paragraph.classList.add("centered-text");
    paragraph.style.fontSize = "24px"; // This is here so that the font size has an initial value declared. After this point, getFontSize() does all the work.
    paragraph.textContent = "Please turn the volume on your device up. This is a demo video for the Philadelphia Pointing Span Test. Do NOT close your browser window while taking this test. Exiting out of the test before its completion will invalidate the results, and you will not be able to continue. Once you are prepared to proceed, click the button below to take the two demo tests. Then you will be prompted to take the actual test.";
    paragraph.style.fontSize = getFontSize();
    document.getElementById("demo_vid").appendChild(paragraph);
    speak(paragraph.textContent);
    document.getElementById("playDemo").style.display = "none"; // Hides button
    document.getElementById("demoTest1").style.display = "block"; // shows demo1 video 
}

function startTest() {
    testLink = document.getElementById('test-link').value; // Retrieve the test link

    // Record the start time on the backend
    fetch(`/start-test/${testLink}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                console.log('Test start time recorded.');
                fetch('/get-stimuli/')
                    .then(response => response.json())
                    .then(data => {
                        stimuli = data;
                        nextStimulus();  // Proceed with the test
                    })
                    .catch(error => {
                        console.error('Error fetching stimuli:', error);
                    });
            }
        })
        .catch(error => {
            console.error('Error recording start time:', error);
        });
}



// Stop Intro Audio on Start Test
document.getElementById('start-test').addEventListener('click', () => {
    const introAudio = currentAudioMap["intro"]; // Access intro audio dynamically
    if (introAudio && typeof introAudio.pause === 'function') {
        introAudio.pause();
        introAudio.currentTime = 0; // Stop and reset the intro audio
    }

    document.getElementById('introduction').style.display = 'none';
    startTest();
});

// CSRF token retrieval function
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



// Function to invalidate the test in the backend
function invalidateTest(testLink) {
    testLink = document.getElementById('test-link').value; // Retrieve the test link
    fetch(`/invalidate_test/${testLink}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({ link: testLink }),
        keepalive: true  // Ensures fetch request completes even if the page is unloading
    })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                console.log('Test marked as invalid.');
            } else {
                console.warn('Failed to invalidate test:', data);
            }
        })
        .catch(error => {
            console.error('Error invalidating test:', error);
        });
}
let confirmUnload = false; // Flag to check if user confirmed the unload

// Warn the user if they try to leave the page with an incomplete test
window.onbeforeunload = function (event) {
    if (currentStimulusIndex < stimuli.length) { // Check if the test is incomplete
        // Display the warning message
        const warningMessage = "You have unfinished responses. Leaving this page will invalidate your test. Are you sure you want to proceed?";
        event.returnValue = warningMessage; // Required for most browsers
        confirmUnload = true; // Set the flag if the user confirms
        return warningMessage;
    }
};

// Invalidate the test if the user confirmed the unload
window.addEventListener('pagehide', function () {
    if (confirmUnload && currentStimulusIndex < stimuli.length) {
        const testLink = document.getElementById('test-link').value;
        invalidateTest(testLink);
    }
});