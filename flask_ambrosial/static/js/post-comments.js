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

    document.querySelectorAll('.edit-comment-icon').forEach(icon => {
        icon.addEventListener('click', function() {
            const commentId = this.dataset.commentId;
            window.location.href = `/post/${postId}/comment/${commentId}/edit`;
        });
    });
    
    document.querySelectorAll('.delete-comment-icon').forEach(icon => {
        icon.addEventListener('click', function() {
            const commentId = this.dataset.commentId;
            if (confirm('Are you sure you want to delete this comment?')) {
                fetch(`/post/${postId}/comment/${commentId}/delete`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': document.querySelector('input[name="csrf_token"]').value
                    }
                }).then(response => {
                    if (response.ok) {
                        location.reload();
                    } else {
                        alert('Failed to delete comment.');
                    }
                });
            }
        });
    });
    
    document.querySelectorAll('.edit-reply-icon').forEach(icon => {
        icon.addEventListener('click', function() {
            const replyId = this.dataset.replyId;
            window.location.href = `/post/${postId}/reply/${replyId}/edit`;
        });
    });
    
    document.querySelectorAll('.delete-reply-icon').forEach(icon => {
        icon.addEventListener('click', function() {
            const replyId = this.dataset.replyId;
            if (confirm('Are you sure you want to delete this reply?')) {
                fetch(`/post/${postId}/reply/${replyId}/delete`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': document.querySelector('input[name="csrf_token"]').value
                    }
                }).then(response => {
                    if (response.ok) {
                        location.reload();
                    } else {
                        alert('Failed to delete reply.');
                    }
                });
            }
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
