document.addEventListener('DOMContentLoaded', function() {
    const addBtn = document.getElementById('addBtn');
    addBtn.addEventListener('click', addAnswer);

    // Assuming there's a function to fetch questions similar to the provided fetchQuestions
    fetchQuestions();
});

function addAnswer() {
    const answerContainer = document.getElementById('answerContainer');
    const newAnswer = document.createElement('div');
    newAnswer.classList.add('answer');

    const answerInput = document.createElement('input');
    answerInput.type = 'text';
    answerInput.placeholder = 'Type your answer here...';

    const removeBtn = document.createElement('button');
    removeBtn.textContent = 'Remove';
    removeBtn.onclick = function() {
        answerContainer.removeChild(newAnswer);
    };

    newAnswer.appendChild(answerInput);
    newAnswer.appendChild(removeBtn);
    answerContainer.appendChild(newAnswer);
}

// Include your existing fetchQuestions and submitAnswer functions here