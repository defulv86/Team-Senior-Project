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

    function speakCharacter(character) {
        const utterance = new SpeechSynthesisUtterance(character);
        window.speechSynthesis.speak(utterance);
    }

    // Function to show the next character
    const showNextChar = () => {
        if (currentCharIndex < stimulusContent.length) {
            stimulusDiv.textContent = stimulusContent[currentCharIndex];
            speakCharacter(stimulusContent[currentCharIndex]);
            currentCharIndex++;
            setTimeout(showNextChar, 1500); // Show next character after 1.5 seconds
        } else {
            stimulusDiv.textContent = '';

            const keyboardShowTime = new Date().toISOString();
            timestamps.push(keyboardShowTime);

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
        timestamps.push(new Date().toISOString()); // Capture timestamp for each character entered
        console.log(response);
    });
});

function showPauseScreen(message, callback) {
    const pauseScreen = document.getElementById('pause-screen');
    const messageDiv = document.getElementById('pause-message');
    const continueButton = document.getElementById('continue-button');

    messageDiv.textContent = message;
    pauseScreen.style.display = 'flex';

    continueButton.onclick = function (event) {
        event.stopPropagation();
        pauseScreen.style.display = 'none';
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
                '4_Span_Digit_Pr': "You will now see two digit practice stimuli.",
                '4_Span_Digit': "You will now see six digit stimuli.",
                '4_Span_Mixed_Pr': "You will now see two mixed practice stimuli.",
                '4_Span_Mixed': "You will now see six mixed stimuli."
            };

            showPauseScreen(messageMap[stimulusType], () => {
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

    // Determine expected length based on stimulus type
    let expectedLength;
    if (currentStimulus.stimulus_type.includes('4_Span')) {
        expectedLength = 4;
    } else if (currentStimulus.stimulus_type.includes('5_Span')) {
        expectedLength = 5;
    }

    // Truncate response to expected length
    const truncatedResponse = response.slice(0, expectedLength);

    fetch('/submit-response/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            link: testLink,
            response_text: truncatedResponse, // Use truncated response
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

function playDemo() { // shows demo video and speaks/shows instructions
    var video = document.createElement("VIDEO");
    video.width = 420;
    video.height = 300; video.controls = true;
    video.src = "/static/images/PPSTTestIntoVid.mp4"; // Static video path
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
    paragraph.style.fontSize = "25px"; // This is here so that the font size has an initial value declared. After this point, getFontSize() does all the work.
    paragraph.textContent = "Please turn the volume on your device up. This is a demo video for the Philadelphia Pointing Span Test. Do NOT close your browser window while taking this test. Exiting out of the test before its completion will invalidate the results, and you will not be able to continue. Once you are prepared to proceed, click the button below to take the two demo tests. Then you will be prompted to take the actual test.";
    paragraph.style.fontSize = getFontSize();
    document.getElementById("demo_vid").appendChild(paragraph);
    speak(paragraph.textContent);
    document.getElementById("playDemo").style.display = "none"; // Hides button
    document.getElementById("demoTest1").style.display = "block"; // shows demo1 video 
}

function startTest() {
    testLink = document.getElementById('test-link').value; // Retrieve the test link

    fetch('/get-stimuli/')
        .then(response => {
            if (!response.ok) {
                throw new Error('Fetch error: ${response.status} ${response.statusText}');
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

function speak(text) {
    const utterance = new SpeechSynthesisUtterance(text);
    const selectedVoice = voices.find(voice => voice.name === 'Google US English');

    if (selectedVoice) {
        utterance.voice = selectedVoice;
    }

    speechSynthesis.speak(utterance);
}

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