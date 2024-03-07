function postQuestion() {
    const questionInput = document.getElementById('question-input');
    const questionText = questionInput.value;
    if (questionText.trim() !== '') {
        document.getElementById('question-text').innerText = questionText;
        document.getElementById('question-display').classList.remove('hidden');
        
        // Example: Dynamically add answer options
        const answersDiv = document.getElementById('answers');
        answersDiv.innerHTML = ''; // Clear previous answers
        for (let i = 1; i <= 4; i++) { // Example: Add 4 answer options
            const answerDiv = document.createElement('div');
            answerDiv.classList.add('answer');
            answerDiv.innerText = `Answer ${i}`;
            answerDiv.onclick = function() { alert(`Answer ${i} clicked`); };
            answersDiv.appendChild(answerDiv);
        }
        
        questionInput.value = ''; // Clear the question input field
    }
}