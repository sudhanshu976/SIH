// Toggle chatbot expansion
document.getElementById('chatbot-icon').addEventListener('click', function() {
    const chatbot = document.getElementById('chatbot');
    chatbot.classList.toggle('expanded');
    document.getElementById('chatbot-header').style.display = chatbot.classList.contains('expanded') ? 'flex' : 'none';
    document.getElementById('chatbot-messages').style.display = chatbot.classList.contains('expanded') ? 'flex' : 'none';
    document.getElementById('chatbot-input').style.display = chatbot.classList.contains('expanded') ? 'flex' : 'none';
});

// Close button functionality
document.getElementById('chatbot-close-btn').addEventListener('click', function(event) {
    event.stopPropagation(); // Prevent triggering the chatbot expansion toggle
    const chatbot = document.getElementById('chatbot');
    chatbot.classList.remove('expanded');
    document.getElementById('chatbot-header').style.display = 'none';
    document.getElementById('chatbot-messages').style.display = 'none';
    document.getElementById('chatbot-input').style.display = 'none';
});
