var socket = io();

socket.on('connect', function() {
    console.log('Connected to server via WebSocket');
});

socket.on('question_posted', function(data) {
    console.log("Question ID:", data.question_id);
    socket.emit('start_timer', { duration: 30, question_id: data.question_id });
});


socket.on('timer_update', function(data) {
    console.log("Timer update received", data);
    const timerElement = document.getElementById(`timer-${data.question_id}`);
    if (data.time_left > 0) {
        timerElement.textContent = data.time_left;
        // Save the remaining time and the current timestamp
        localStorage.setItem(`timer-${data.question_id}`, JSON.stringify({ time_left: data.time_left, timestamp: Date.now() }));
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

document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.question').forEach(question => {
        const questionId = question.id.split('-')[1];
        const timerState = localStorage.getItem(`timer-${questionId}`);
        if (timerState) {
            const { time_left, timestamp } = JSON.parse(timerState);
            const currentTime = Date.now();
            const elapsedTime = Math.floor((currentTime - timestamp) / 1000); // Convert ms to seconds
            const adjustedTimeLeft = Math.max(time_left - elapsedTime, 0);

            if (adjustedTimeLeft > 0) {
                // Restart the timer with the adjusted time left
                startTimer(adjustedTimeLeft, questionId);
            } else {
                // Handle timer end if the adjusted time is 0 or less
                handleTimerEnd(questionId);
            }
        }
    });
});

function startTimer(duration, questionId) {
    const timerElement = document.getElementById(`timer-${questionId}`);
    const interval = setInterval(() => {
        if (duration > 0) {
            duration--;
            timerElement.textContent = duration;
            localStorage.setItem(`timer-${questionId}`, JSON.stringify({ time_left: duration, timestamp: Date.now() }));
        } else {
            clearInterval(interval);
            handleTimerEnd(questionId);
        }
    }, 1000);
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
