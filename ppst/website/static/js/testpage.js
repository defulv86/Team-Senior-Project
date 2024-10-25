let stimuli = [];
let currentStimulusIndex = 0;
let responseLatency = 0;
let startTime;
let response = ''; // Store the response from the keyboard

function flashStimulus(stimulus) {
    const stimulusDiv = document.getElementById('stimulus');
    const digitKeyboard = document.getElementById('digit-keyboard');
    const alphanumericKeyboard = document.getElementById('alphanumeric-keyboard');
    const responseSection = document.getElementById('response-section');

    // Hide both keyboards and the response section initially
    digitKeyboard.style.display = 'none';
    alphanumericKeyboard.style.display = 'none';
    responseSection.style.display = 'none'; // Hide the response section

    const stimulusContent = stimulus.stimulus_content;
    let currentCharIndex = 0;

    // Function to show the next character
    const showNextChar = () => {
        if (currentCharIndex < stimulusContent.length) {
            stimulusDiv.textContent = stimulusContent[currentCharIndex];
            currentCharIndex++;
            setTimeout(showNextChar, 1000); // Show next character after 1 second
        } else {
            // Clear the stimulus and show the keyboard
            stimulusDiv.textContent = '';
            if (stimulus.stimulus_type.includes('Digit')) {
                digitKeyboard.style.display = 'flex';
            } else if (stimulus.stimulus_type.includes('Mixed')) {
                alphanumericKeyboard.style.display = 'flex';
            }
            responseSection.style.display = 'block'; // Show the response section again
        }
    };

    // Start showing characters
    showNextChar();
}

// Add event listeners for keyboard buttons
document.querySelectorAll('.key').forEach(key => {
    key.addEventListener('click', () => {
        if (key.dataset.value === 'C') {
            response = '';  // Clear input
        } else {
            response += key.dataset.value;  // Append clicked key value
        }
        console.log(response); // For debugging
    });
});

function nextStimulus() {
    if (currentStimulusIndex < stimuli.length) {
        startTime = new Date().getTime();
        flashStimulus(stimuli[currentStimulusIndex]);
        currentStimulusIndex++;
        response = ''; // Reset response for next stimulus
    } else {
        document.getElementById('stimulus').textContent = 'Test completed! Thank you for your participation.';
        document.getElementById('response-section').style.display = 'none';
    }
}

document.getElementById('submit-response').addEventListener('click', () => {
    if (!response) {
        alert('Please enter a response before submitting.');
        return;
    }

    const currentStimulus = stimuli[currentStimulusIndex - 1];
    const maxLength = currentStimulus.stimulus_content.length;

    // Truncate response if it exceeds the maximum length
    if (response.length > maxLength) {
        response = response.substring(0, maxLength);
    }

    fetch('/submit-response/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            link: testLink,
            response_text: response, // The response input from the user
            stimulus_id: currentStimulus.id, // Use the correct stimulus ID
            response_position: currentStimulusIndex // Current position in the stimulus sequence
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
            response = ''; // Reset response after submission
            nextStimulus();
        })
        .catch(error => {
            console.error('There was a problem with the fetch operation:', error);
            alert('An error occurred while submitting your response. Please try again.');
        });
});

function startTest() {
    testLink = document.getElementById('test-link').value; // Retrieve the test link

    fetch('/get-stimuli/')
        .then(response => {
            if (!response.ok) {
                throw new Error(`Fetch error: ${response.status} ${response.statusText}`);
            }
            return response.json();
        })
        .then(data => {
            stimuli = data; // Use the newly ordered stimuli
            nextStimulus();
        })
        .catch(error => {
            console.error('Error fetching stimuli:', error);
        });
}

document.getElementById('start-test').addEventListener('click', function () {
    document.getElementById('introduction').style.display = 'none';
    startTest();
});

let voices = [];

// Function to populate the voice dropdown
function populateVoices() {
    voices = window.speechSynthesis.getVoices();
}

// Load voices when the voices are changed
window.speechSynthesis.onvoiceschanged = populateVoices;

// Function to speak the text
function speakText() {
    const textElement = document.getElementById('text-to-speak');
    const text = textElement.innerText; // Get the text content

    if ('speechSynthesis' in window) {
        window.speechSynthesis.cancel(); // Stop any ongoing speech

        const speech = new SpeechSynthesisUtterance(text);
        speech.voice = voices[0]; // Choose the first available voice
        speech.lang = 'en-US'; // Set the language
        speech.volume = 1; // Volume from 0 to 1
        speech.rate = 1; // Speed of speech
        speech.pitch = 1; // Pitch of voice

        window.speechSynthesis.speak(speech);
    } else {
        alert('Sorry, your browser does not support text-to-speech.');
    }
}

document.getElementById('speak-button').addEventListener('click', speakText);
document.addEventListener('DOMContentLoaded', populateVoices);