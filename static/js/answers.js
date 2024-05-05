var socket = io();

socket.on('connect', function() {
    console.log('Connected to server via WebSocket');
});


socket.on('timer_update', function(data) {
    console.log("Timer update received", data);
    const timerElement = document.getElementById(`timer-${data.question_id}`);
    if (data.time_left != 0) {
        timerElement.textContent = data.time_left;        
    } else {
        handleTimerEnd(data.question_id);
    }
});

function handleTimerEnd(questionId) {
    console.log("Timer has ended for question ID:", questionId);
    const submitButton = document.querySelector(`form[data-question-id="${questionId}"] button[type="submit"]`);
    submitButton.disabled = true;
    submitButton.style.backgroundColor = '#ccc';
    const resultsButton = document.getElementById(`resultsButton-${questionId}`);
    if (resultsButton) {
        resultsButton.style.display = 'block'; // Show the results button
    }
}


async function submitAnswer(event, form, questionId) {
    event.preventDefault();
    const selectedAnswer = form.querySelector(`input[name="answer-${questionId}"]:checked`).value;

    const data = {
        questionId: questionId,
        answerIndex: parseInt(selectedAnswer, 10)
    };

    try {
        const response = await fetch('/validate-answer', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        });

        if (response.ok) {
            const result = await response.json();
            alert(result.message);
        } else {
            console.error('Submission failed', await response.text());
        }
    } catch (error) {
        console.error('Network error:', error);
    }
}

function toggleResults(questionId) {
    const dropdown = document.getElementById(`results-content-${questionId}`);
    if (dropdown.style.display === 'none' || dropdown.style.display === '') {
        fetch(`/question-results/${questionId}`)
            .then(response => response.json())
            .then(data => {
                const answers = Object.keys(data);
                const counts = Object.values(data);
                const labels = answers.map((answer, index) => `Option ${index + 1}`);

                const ctx = document.createElement('canvas').getContext('2d');
                new Chart(ctx, {
                    type: 'bar',
                    data: {
                        labels: labels,
                        datasets: [{
                            label: 'Votes',
                            data: counts,
                            backgroundColor: 'rgba(54, 162, 235, 0.5)',
                            borderColor: 'rgba(54, 162, 235, 1)',
                            borderWidth: 1
                        }]
                    },
                    options: {
                        scales: {
                            y: {
                                beginAtZero: true
                            }
                        }
                    }
                });

                dropdown.innerHTML = ''; // Clear previous content
                dropdown.appendChild(ctx.canvas);
                dropdown.style.display = 'block';
            })
            .catch(error => {
                console.error('Error fetching results:', error);
                dropdown.innerHTML = 'Failed to fetch results';
                dropdown.style.display = 'block';
            });
    } else {
        dropdown.style.display = 'none';
    }
}