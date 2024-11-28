const dialogEditor = document.getElementById('dialogEditor');
const essayEditor = document.getElementById('essayEditor');
const chatMessages = document.getElementById('chatMessages');

function addMessage(message, isUser = true) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isUser ? 'user' : 'tutor'}`;
    messageDiv.textContent = message;
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}
    
async function submitDialog() {
    const message = dialogEditor.value;
    if (!message.trim()) return;

    addMessage(message, true);
    dialogEditor.value = '';

    try {
        const response = await fetch('http://127.0.0.1:8000/dialog', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                message: message
            })
        });
        
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        
        const data = await response.json();
        // Simulate tutor response
        console.log(data)
        addMessage(data.message, false);
        //showSaveAnimation(dialogEditor);
    } catch (error) {
        console.error('Error submitting dialog:', error);
        alert('Error submitting dialog. Please try again.');
    }
}
    
async function submitEssay() {
    try {
        const response = await fetch("http://127.0.0.1:8000/essay", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                essay: "Hello"//essayEditor.value
            })
        });
        
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        
        const data = await response.json();
        //showSaveAnimation(essayEditor);
        console.log('Essay submitted successfully:', data);
    } catch (error) {
        console.error('Error submitting essay:', error);
        alert('Error submitting essay. Please try again.');
    }
}
    
function showSaveAnimation(element) {
    element.parentElement.classList.add('saving');
    setTimeout(() => {
        element.parentElement.classList.remove('saving');
    }, 1000);
}
    
// Load saved content on page load
window.addEventListener('load', () => {
    // Add welcome message
    addMessage('Здравствуйте! Я ваш виртуальный тьютор. Чем могу помочь?', false);
});
    
// Handle Enter key in dialog
dialogEditor.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        submitDialog();
    }
});