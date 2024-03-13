document.getElementById('postBtn').addEventListener('click', function() {
    const question = document.getElementById('questionInput').value;
    const answerBoxes = document.querySelectorAll('.answer-box');

    const answers = Array.from(answerBoxes).map(box => box.textContent.trim()).filter(text => text !== '' && text !== 'Type your answer here...');
    const correctAnswer = +document.getElementById('correctAnswer').value;

    fetch('/post-question', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question, answers, correctAnswer }),
    })
    .then(response => {
        if (response.ok) {
            window.location.href = 'index.html';
        } else {
            alert('Failed to post question. Please try again.');
        }
    })
    .catch(error => console.error('Error:', error));
});

document.getElementById('addBtn').addEventListener('click', function() {
    const container = document.getElementById('answerContainer');
    if (container.children.length >= 5) {
        alert('A maximum of 5 answers are allowed.');
        return;
    }

    const newAnswerBox = document.createElement('div');
    newAnswerBox.classList.add('answer-box');
    newAnswerBox.contentEditable = true;
    newAnswerBox.style.border = '1px solid #ccc';
    newAnswerBox.style.margin = '10px 0';
    newAnswerBox.style.padding = '5px';

    const deleteButton = document.createElement('button');
    deleteButton.textContent = 'X';
    deleteButton.style.float = 'right';
    deleteButton.addEventListener('click', function() {
        container.removeChild(newAnswerBox);
        updateCorrectAnswerOptions();
    });

    newAnswerBox.appendChild(deleteButton);

    newAnswerBox.addEventListener('focus', function() {
        if (this.textContent === 'Type your answer here...') {
            this.textContent = '';
        }
    });

    newAnswerBox.addEventListener('blur', function() {
        if (this.textContent.trim() === '') {
            this.textContent = 'Type your answer here...';
        }
    });

    container.appendChild(newAnswerBox);
    updateCorrectAnswerOptions();
});

function updateCorrectAnswerOptions() {
    const answerBoxes = document.querySelectorAll('#answerContainer .answer-box');
    const correctAnswerSelect = document.getElementById('correctAnswer');
    correctAnswerSelect.innerHTML = '';
    answerBoxes.forEach((box, index) => {
        const option = document.createElement('option');
        option.value = index;
        option.textContent = `Answer ${index+1}`; 
        correctAnswerSelect.appendChild(option);
    });
}

document.addEventListener('DOMContentLoaded', function() {
    updateCorrectAnswerOptions();
});