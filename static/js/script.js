document.addEventListener('DOMContentLoaded', function() {
    fetchQuestions();
});

function fetchQuestions() {
    fetch('/get-questions')
        .then(response => response.json())
        .then(questions => {
            const container = document.getElementById('questionsContainer');
            questions.forEach(question => {
                const questionElem = document.createElement('div');
                questionElem.textContent = question.question;
                container.appendChild(questionElem);

                question.answers.forEach((answer, index) => {
                    const answerElem = document.createElement('button');
                    answerElem.textContent = answer;
                    answerElem.onclick = () => submitAnswer(question._id, index);
                    questionElem.appendChild(answerElem);
                });
            });
        });
}

function submitAnswer(questionId, answerIndex) {
    fetch('/validate-answer', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ questionId, answerIndex }),
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message); // Assuming the server sends back a message indicating if the answer was correct or not
    });
}