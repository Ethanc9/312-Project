document.getElementById('postBtn').addEventListener('click', function() {
    const question = document.getElementById('questionInput').value;
    const answerBoxes = document.querySelectorAll('.answer-box');
    const imageInput = document.getElementById('image');
    const imageFile = imageInput.files[0];
    
    if (!question && !imageFile) {
        alert('Please provide a question or upload an image.');
        return;
    }

    const answers = Array.from(answerBoxes).map(box => box.textContent.trim()).filter(text => text !== '' && text !== 'Type your answer here...');
    const correctAnswer = +document.getElementById('correctAnswer').value;

    const postData = {
        question: question,
        answers: answers,
        correctAnswer: correctAnswer
    };

    // If an image file is uploaded, add it to the postData
    if (imageFile) {
        const reader = new FileReader();
        reader.onload = function(event) {
            postData.image = event.target.result;
            sendPostData(postData);
        };
        reader.readAsDataURL(imageFile);
    } else {
        sendPostData(postData);
    }
});

function sendPostData(postData) {
    fetch('/post-question', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(postData),
    })
    .then(response => {
        if (response.ok) {
            window.location.href = '/';
        } else {
            alert('Failed to post question. Please try again.');
        }
    })
    .catch(error => console.error('Error:', error));
}

document.getElementById('addBtn').addEventListener('click', function() {
    const container = document.getElementById('answerContainer');
    if (container.children.length >= 5) {
        alert('A maximum of 5 answers are allowed.');
        return;
    }

    const answerContainer = document.createElement('div');
    answerContainer.classList.add('answer-container');

    const newAnswerBox = document.createElement('div');
    newAnswerBox.classList.add('answer-box');
    newAnswerBox.contentEditable = true;
    newAnswerBox.style.border = '1px solid #ccc';
    newAnswerBox.style.margin = '10px 0';
    newAnswerBox.style.padding = '5px';

    const deleteButton = document.createElement('button');
    deleteButton.textContent = 'Remove';
    deleteButton.style.float = 'right';
    deleteButton.addEventListener('click', function() {
        answerContainer.remove();
    });

    answerContainer.appendChild(newAnswerBox);
    answerContainer.appendChild(deleteButton);

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

    container.appendChild(answerContainer);
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