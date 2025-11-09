document.addEventListener('DOMContentLoaded', function() {
    const messageList = document.getElementById('message-list');
    if (messageList) {
        setTimeout(function() {
            messageList.style.display = 'none';
        }, 2000); 
    }
});