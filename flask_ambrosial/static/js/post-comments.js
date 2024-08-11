document.addEventListener('DOMContentLoaded', function() {
    const addCommentIcons = document.querySelectorAll('.add-comment-icon');
    const viewCommentsIcons = document.querySelectorAll('.view-comments-icon');
    const readMoreLinks = document.querySelectorAll('.read-more');

    addCommentIcons.forEach(icon => {
        icon.addEventListener('click', function() {
            const commentForm = document.querySelector('.comment-form');
            commentForm.style.display = commentForm.style.display === 'none' || commentForm.style.display === '' ? 'block' : 'none';
        });
    });

    viewCommentsIcons.forEach(icon => {
        icon.addEventListener('click', function() {
            const commentsDisplay = document.querySelector('.comments-display');
            commentsDisplay.style.display = commentsDisplay.style.display === 'none' || commentsDisplay.style.display === '' ? 'block' : 'none';
        });
    });

    document.querySelectorAll('.reply-icon').forEach(icon => {
        icon.addEventListener('click', function() {
            const replyForm = this.closest('.media-body').querySelector('.reply-form');
            replyForm.style.display = replyForm.style.display === 'none' || replyForm.style.display === '' ? 'block' : 'none';
        });
    });

    function addReadMoreEventListeners() {
        document.querySelectorAll('.read-more').forEach(link => {
            link.addEventListener('click', function(event) {
                event.preventDefault();
                const fullContent = this.getAttribute('data-full-content');
                const articleContent = this.closest('.article-content');
                if (this.textContent === 'Read more') {
                    articleContent.innerHTML = fullContent + ' <a href="#" class="read-more" data-full-content="' + fullContent + '">Show less</a>';
                } else {
                    articleContent.innerHTML = fullContent.split(' ').slice(0, 20).join(' ') + '... <a href="#" class="read-more" data-full-content="' + fullContent + '">Read more</a>';
                }
                addReadMoreEventListeners();
            });
        });
    }

    addReadMoreEventListeners();
});
