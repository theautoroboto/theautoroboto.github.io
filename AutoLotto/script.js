const form = document.getElementById('lotto');
const number1 = document.getElementById('number1');
const number2 = document.getElementById('number2');
const number3 = document.getElementById('number3');
const number4 = document.getElementById('number4');
const number5 = document.getElementById('number5');
const my_number1 = document.getElementById('my_number1');
const my_number2 = document.getElementById('my_number2');
const my_number3 = document.getElementById('my_number3');
const my_number4 = document.getElementById('my_number4');
const my_number5 = document.getElementById('my_number5');
const messageContainer = document.querySelector('.message-container');
const message = document.getElementById('message');
const winnings = document.getElementById('winnings');
const times_played = document.getElementById('times_played');
const num_correct = document.getElementById('correct');
const auto_btn = document.getElementById('autoPick');

const formatter = new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 2
  })

winnings.textContent = 0;
times_played.textContent = 0;

// By default we do not have a valid form
let isValid = false;

function validateForm() {
    isValid = form.checkValidity();
    // console.log(isValid);
    // message.textContent = 'Invalid'
}

function playLotto() {
    var correct = 0;
    var lotto_number1 = Math.floor(Math.random() * 9) + 1;
    var lotto_number2 = Math.floor(Math.random() * 9) + 1;
    var lotto_number3 = Math.floor(Math.random() * 9) + 1;
    var lotto_number4 = Math.floor(Math.random() * 9) + 1;
    var lotto_number5 = Math.floor(Math.random() * 9) + 1;
    number1.textContent = lotto_number1.toString();
    number2.textContent = lotto_number2.toString();
    number3.textContent = lotto_number3.toString();
    number4.textContent = lotto_number4.toString();
    number5.textContent = lotto_number5.toString();
    // console.log(number1.textContent);
    // console.log(my_number1.value);
    if (my_number1.value === number1.textContent) correct++;
    if (my_number2.value === number2.textContent) correct++;
    if (my_number3.value === number3.textContent) correct++;
    if (my_number4.value === number4.textContent) correct++;
    if (my_number5.value === number5.textContent) correct++;

    num_correct.textContent = correct.toString();
    console.log(correct);

    if (correct == 0) {
        message.textContent = 'LOSER'
        document.body.style.backgroundColor = "#787c78";
        message.textContent = 'LOSER'
        my_winnings = parseInt(winnings.textContent, 10);
        --my_winnings;
        winnings.textContent = my_winnings.toString();
    }
    if (correct == 1) {
        message.textContent = 'Only 1 Right'
        document.body.style.backgroundColor = "#787c78";
        my_winnings = parseInt(winnings.textContent, 10); 
        --my_winnings;
        winnings.textContent = my_winnings.toString();
    }
    if (correct == 2) {
        message.textContent = 'You got 2'
        document.body.style.backgroundColor = "#224b27";
        my_winnings = parseInt(winnings.textContent, 10); 
        my_winnings = my_winnings + 1;
        winnings.textContent = my_winnings.toString();
    }
    if (correct == 3) {
        message.textContent = '3 correct, getting closer'
        document.body.style.backgroundColor = "#2b8037";
        my_winnings = parseInt(winnings.textContent, 10); 
        my_winnings = my_winnings + 100;
        winnings.textContent = my_winnings.toString();
    }
    if (correct == 4) {
        message.textContent = '4 CORRECT ALMOST!!!'
        document.body.style.backgroundColor = "#23b339";
        my_winnings = parseInt(winnings.textContent, 10); 
        my_winnings = my_winnings + 10000;
        winnings.textContent = my_winnings.toString();
    }


    if (correct == 5) {
        console.log("YAY");
        message.textContent = 'Hot Damn you actually WON'
        document.body.style.backgroundColor = "#00ff26";
        document.getElementById("submit").disabled = true;
        my_winnings = parseInt(winnings.textContent, 10);
        my_winnings = my_winnings + 10000000;
        winnings.textContent = my_winnings.toString();
    }
    my_plays = parseInt(times_played.textContent, 10);
    my_plays++;
    times_played.textContent = my_plays.toString();

}

function autoPick() {
    var lotto_number1 = Math.floor(Math.random() * 9) + 1;
    var lotto_number2 = Math.floor(Math.random() * 9) + 1;
    var lotto_number3 = Math.floor(Math.random() * 9) + 1;
    var lotto_number4 = Math.floor(Math.random() * 9) + 1;
    var lotto_number5 = Math.floor(Math.random() * 9) + 1;
    my_number1.value = lotto_number1.toString();
    my_number2.value = lotto_number2.toString();
    my_number3.value = lotto_number3.toString();
    my_number4.value = lotto_number4.toString();
    my_number5.value = lotto_number5.toString();
}

function processFormData(e) {
    e.preventDefault();
    // Validate
    validateForm();
  // Play lotto if Valid
  if (isValid) {
    playLotto();
  }
}

// Event Listner
form.addEventListener('submit', processFormData);
auto_btn.addEventListener("click", autoPick)
