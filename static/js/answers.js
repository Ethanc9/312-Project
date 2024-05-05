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
    if (timerElement) {
        timerElement.textContent = data.time_left;
    }
});

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
