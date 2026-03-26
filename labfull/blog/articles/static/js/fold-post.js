document.addEventListener('DOMContentLoaded', function() {
    const buttons = document.querySelectorAll('.fold-button');
    buttons.forEach(button => {
        button.addEventListener('click', function() {
            const card = this.closest('.post-card');
            if (card) {
                const content = card.querySelector('.post-content');
                if (content) {
                    content.classList.toggle('folded');
                    this.textContent = content.classList.contains('folded') ? 'Развернуть' : 'Свернуть';
                }
            }
        });
    });
});