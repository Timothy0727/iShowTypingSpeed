let wordsArray = [];
const wordsEachLine = 10;   // number of words each line
const totalLines = 5;       // number of lines
readTextFile("source/words.txt")

// quotes to be typed
let quotes_array = [];

let accuracy_text = document.querySelector(".final_accuracy");
let stats_group = document.querySelector(".stats")
let wpm_text = document.querySelector(".final_wpm");
let time_text = document.querySelector(".final_time");
let quote_text = document.querySelector(".quote");
let input_area = document.querySelector(".input_box");
let restart_btn = document.querySelector(".start_new_test");

let timeElapsed = 0;
let accuracy = 0;
let total_time = 0;
let timer = null;
let quoteNo = 0;
let errors = 0;
let total_errors = 0;
let characterTyped = 0;

async function readTextFile(filePath) {
    try {
        const response = await fetch(filePath);
        const data = await response.text();
        wordsArray = data.split('\n').map(word => word.trim()).filter(word => word.length > 0);
        console.log("Words loaded successfully.");
        quotes_array = generateWords();

    } catch (error) {
        console.error('Error loading the file: ', error);
    }
}


function generateWords() {
    if (wordsArray.length === 0) {
        alert('No words loaded. Please check the file path.')
        return;
    }
    const randomWords = [];
    for (let i = 0; i < totalLines; i++) {
        const tempSentence = []
        for (let j = 0; j < wordsEachLine; j++) {
            const randomIndex = Math.floor(Math.random() * wordsArray.length);
            tempSentence.push(wordsArray[randomIndex]);
        }
        randomWords.push(tempSentence.join(' '));
    }
    return randomWords;
}


function updateQuote() {
    quote_text.textContent = null;
    current_quote = quotes_array[quoteNo];

    current_quote.split('').forEach(char => {
        const charSpan = document.createElement('span')
        charSpan.innerText = char
        quote_text.appendChild(charSpan)
    });
}

function processInputText() {
    quoteSpanArray = quote_text.querySelectorAll('span');
    curr_input = input_area.value;
    // console.log(curr_input);
    curr_input_array = curr_input.split('');
    let localErrors = 0

    characterTyped++;

    let isIncorrect = false;

    
    quoteSpanArray.forEach((char, index) => {
        let typedChar = curr_input_array[index]

        if (typedChar == null) {
            char.classList.remove('correct_char');
            char.classList.remove('incorect_char');
        } else if (typedChar === char.innerText) {
            char.classList.add('correct_char');
            char.classList.remove('incorrect_char');
        } else {
            char.classList.add('incorrect_char')
            char.classList.remove('correct_char')
        }
    });

    if (curr_input.length == current_quote.length) {
        curr_input = input_area.value;

        // check number of errors after typing each line
        quoteSpanArray.forEach((char, index) => {
            let typedChar = curr_input_array[index]
            if (typedChar !== char.innerText) {
                errors++;
            }
        });
    
        total_errors += errors;
        errors = 0;

        if (quoteNo < quotes_array.length - 1) {
            quoteNo++;
            updateQuote();
            input_area.value = "";
        } else {    // finished typing test
            total_time = (Date.now() - timeElapsed) / 1000;
            finishGame();
        }
    }
}


function startGame() {
    resetValues();
    updateQuote();
    timeElapsed = Date.now()
    input_area.disabled = false;
    input_area.focus()
    
}


function resetValues() {
    timeElapsed = 0;
    errors = 0;
    total_errors = 0;
    accuracy = 0;
    characterTyped = 0;
    quoteNo = 0;
    quotes_array = generateWords()
    input_area.disabled = false;
    input_area.style.display = "block"
    input_area.focus()
    input_area.value = "";
    quote_text.textContent = 'Click on the area below to start the game.';
    accuracy_text.textContent = '100%';

    stats_group.style.display = "none";
    restart_btn.style.display = "none"
}

function finishGame() {
    stats_group.style
    input_area.value = "";
    input_area.disabled = true;
    quote_text.textContent = "Click on the restart button to start a new game.";
    restart_btn.computedStyleMap.display = "block";
    
    Math.round((((characterTyped / 5) / total_time) * 60));
    accuracy = ((characterTyped - total_errors) / characterTyped * 100).toFixed(2)
    accuracy_text.textContent = accuracy.toString() + "%"
    // cpm = ((characterTyped - total_errors) / total_time) * 60
    wpm = ((characterTyped / 5) / total_time) * 60
    wpm_text.textContent = wpm;
    time_text.textContent = total_time.toFixed(2);
    stats_group.style.display = "flex"
    restart_btn.style.display = "inline-block"
    input_area.style.display = "none"
}