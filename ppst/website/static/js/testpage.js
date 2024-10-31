const form = document.querySelector('form');

form.addEventListener('submit', function(e) {
    e.preventDefault();
    var selectedFontSize = document.getElementById("fontSize").value;
    changeFontSize(selectedFontSize);
});

function changeFontSize(size) {
    document.getElementById("P").style.fontSize = size;
}

function getFontSize() {
    return document.getElementById("fontSize").value;
}

function speak(text) { // allows text to be spoken
    var utterance = new SpeechSynthesisUtterance(text);
    window.speechSynthesis.speak(utterance);
}

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
    paragraph.style.color =  "#0077b3";
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

function demoTest1() {
    // show demo test1
    document.getElementById("demo_vid").style.display = "none";
    document.getElementById("test").style.display = "block";
    displayTest(demosTest1);
    // show buttons
    document.getElementById("d12t4").style.display = "block"; // if else buttons for each test
    document.getElementById("demoTest1").style.display = "none"; // change to demoTest
    document.getElementById("demoTest2").style.display = "block"; // change to demoTest
}

function demoTest2() {
    // show demo test2
    document.getElementById("d12t4").style.display = "none";
    document.getElementById("test").style.display = "block";
    displayTest(demosTest2);
    document.getElementById("d12t4").style.display = "block";
    // show take test
    document.getElementById("demoTest2").style.display = "none";
    document.getElementById("takeTest").style.display = "block";
}

function takeTest() { // sends user to test page and hides video/demo button 
    document.getElementById("d12t4").style.display = "none";
    document.getElementById("takeTest").style.display = "none";
    document.getElementById("demoTest2").style.display = "none";
    document.getElementById("test").style.display = "block";
    displayTest(test1);
    document.getElementById("t136").style.display = "block";
    document.getElementById("submit").style.display = "block";
}

let userInput = "";
function choice(value) { // takes selected num/let and adds to answer when submitted
    userInput += value;
}

function compareAnswers(testX) {
    let correctAnswer;
    switch (testX) {
        case test1:
            correctAnswer = test1_ans;
            break;
        case test2:
            correctAnswer = test2_ans;
            break;
        case test3:
            correctAnswer = test3_ans;
            break;
        case test4:
            correctAnswer = test4_ans;
            break;
        case test5:
            correctAnswer = test5_ans;
            break;
        case test6:
            correctAnswer = test6_ans;
            break;
        case test7:
            correctAnswer = test7_ans;
            break;
        case test8:
            correctAnswer = test8_ans;
            break;
        case test9:
            correctAnswer = test9_ans;
            break;
        case test10:
            correctAnswer = test10_ans;
            break;
        case test11:
            correctAnswer = test11_ans;
            break;
        case test12:
            correctAnswer = test12_ans;
            break;
        default:
            console.error("Invalid test number");
            return;
    }

    let correctCount = 0;
    for (let i = 0; i < userInput.length; i++) {
        if (userInput[i] === correctAnswer[i]) {
            correctCount++;
        }
    }
    let percentage = (correctCount / correctAnswer.length) * 100;
    return percentage;
}

function submit() { // sends user to submission page and hides submit button
    var paragraph = document.getElementById("P");
    paragraph.textContent = "Thank you for successfully completing the Philadelphia Pointing Span Test. Your health provider has been notified and the results will be available to them. You may now exit this screen.";
    paragraph.style.fontSize = getFontSize();
    paragraph.style.color =  "black";
    paragraph.style.fontFamily = "Open Sans";
    paragraph.classList.add("centered-text");
    document.getElementById("submit_p").appendChild(paragraph);
    speak(paragraph.textContent);
    document.getElementById("t136").style.display = "none";
    document.getElementById("submit").style.display = "none";
    document.getElementById("test").style.display = "none";
}

let currentIndex = 0;
function displayTest(testString) {
    const testDiv = document.getElementById("test");
    testDiv.innerHTML = "";
    currentIndex = 0;

    const interval = setInterval(() => {
        if (currentIndex < testString.length) {
            const letter = document.createElement("span");
            letter.textContent = testString[currentIndex];
            letter.style.fontSize = "90px"; // font size
            testDiv.appendChild(letter);
            speak(testString[currentIndex]);  // speak the letter or number

            setTimeout(() => {
                testDiv.removeChild(letter);
            }, 1000);

            currentIndex++;
        } else {
            clearInterval(interval);
        }
    }, 2000); // slow or speed test up /down
}

// d12t4 = used for demo 1, 2 and test 4
const demosTest1 = "6254";  // demo1
const demosTest2 = "46723"; // demo2
const demosTest3 = "6E5T";  // demo3 mixed
const demosTest4 = "4H7A3"; // demo4 mixed
const test1 = "89512"; /* Num test 1 5 digit */ 
const test2 = "73406"; /* Num test 2 5 digit */ 
const test3 = "95231"; /* Num test 3 5 digit */ 
const test4 = "2463";  // Num test 1 4 digit
const test5 = "9067";  // Num test 2 4 digit
const test6 = "8105";  // Num test 3 4 digit
const test7 = "946KJ"; // Mix test 1 5 digit
const test8 = "S370V"; // Mix test 2 5 digit
const test9 = "30RE4"; // Mix test 3 5 digit
const test10 = "6F9A"; // Mix test 1 4 digit
const test11 = "HY42"; // Mix test 2 4 digit
const test12 = "P5L8"; // Mix test 3 4 digit

const test1_ans = "12589";
const test2_ans = "64307";
const test3_ans = "12359";
const test4_ans = "2346";
const test5_ans = "0679";
const test6_ans = "0158";
const test7_ans = "469JK";
const test8_ans = "037SV";
const test9_ans = "034ER";
const test10_ans = "69AF";
const test11_ans = "24HY";
const test12_ans = "58LP";
