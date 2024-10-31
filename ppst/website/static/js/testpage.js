let stimuli = [];
let currentStimulusIndex = 0;
let response = ''; // Store the response from the keyboard
const timestamps = [];

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

            const keyboardShowTime = new Date().toISOString();
            timestamps.push(keyboardShowTime);

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
        response += key.dataset.value;  // Append clicked key value
        timestamps.push(new Date().toISOString()); // Capture timestamp for each character entered
        console.log(response); // For debugging
    });
});

function nextStimulus() {
    if (currentStimulusIndex < stimuli.length) {
        startTime = new Date().getTime();
        flashStimulus(stimuli[currentStimulusIndex]);
        currentStimulusIndex++;
        response = ''; // Reset response for next stimulus
        timestamps.length = 0; // Clear timestamps for the next stimulus
    } else {
        document.getElementById('stimulus').textContent = 'Test completed! Thank you for your participation.';
        document.getElementById('response-section').style.display = 'none';
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

    fetch('/submit-response/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            link: testLink,
            response_text: response,
            stimulus_id: currentStimulus.id,
            response_position: currentStimulusIndex,
            character_latencies: characterLatencies, // Send latencies to the backend
            character_accuracies: accuracies, // Send accuracies to the backend
            expected_stimulus: correctAnswer, // Send the expected stimulus for accuracy checks
            timestamps: timestamps
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
            timestamps.length = 0; // Clear the timestamps for the next response
            nextStimulus();
        })
        .catch(error => {
            console.error('There was a problem with the fetch operation:', error);
            alert('An error occurred while submitting your response. Please try again.');
        });
});

document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('response-input').addEventListener('input', (event) => {
        response = event.target.value; // Update the response variable
        const firstCharacterTime = new Date().toISOString();
        timestamps.push(firstCharacterTime);
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
            stimuli = data;
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
function populateVoices() {
    voices = window.speechSynthesis.getVoices();
}

window.speechSynthesis.onvoiceschanged = populateVoices;

function speakText() {
    const textElement = document.getElementById('text-to-speak');
    const text = textElement.innerText;

    if ('speechSynthesis' in window) {
        window.speechSynthesis.cancel();

        const speech = new SpeechSynthesisUtterance(text);
        speech.voice = voices[0];
        speech.lang = 'en-US';
        speech.volume = 1;
        speech.rate = 1;
        speech.pitch = 1;

        window.speechSynthesis.speak(speech);
    } else {
        alert('Sorry, your browser does not support text-to-speech.');
    }
}

document.getElementById('speak-button').addEventListener('click', speakText);
document.addEventListener('DOMContentLoaded', populateVoices);