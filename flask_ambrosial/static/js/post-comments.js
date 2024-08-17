document.addEventListener('DOMContentLoaded', function() {
    // Select all elements with the class 'add-comment-icon'
    const addCommentIcons = document.querySelectorAll('.add-comment-icon');
    // Select all elements with the class 'view-comments-icon'
    const viewCommentsIcons = document.querySelectorAll('.view-comments-icon');
    // Select all elements with the class 'read-more'
    const readMoreLinks = document.querySelectorAll('.read-more');

    // Toggle the display of the comment form when the add comment icon is clicked
    addCommentIcons.forEach(icon => {
        icon.addEventListener('click', function() {
            const commentForm = document.querySelector('.comment-form');
            commentForm.style.display = commentForm.style.display === 'none' 
                || commentForm.style.display === '' ? 'block' : 'none';
        });
    });

    // Toggle the display of the comments section when the view comments icon is clicked
    viewCommentsIcons.forEach(icon => {
        icon.addEventListener('click', function() {
            const commentsDisplay = document.querySelector('.comments-display');
            commentsDisplay.style.display = commentsDisplay.style.display === 'none' 
                || commentsDisplay.style.display === '' ? 'block' : 'none';
        });
    });

    // Toggle the display of the reply form when the reply icon is clicked
    document.querySelectorAll('.reply-icon').forEach(icon => {
        icon.addEventListener('click', function() {
            const replyForm = this.closest('.media-body')
                .querySelector('.reply-form');
            replyForm.style.display = replyForm.style.display === 'none' 
                || replyForm.style.display === '' ? 'block' : 'none';
        });
    });

    // Redirect to the edit comment page when the edit comment icon is clicked
    document.querySelectorAll('.edit-comment-icon').forEach(icon => {
        icon.addEventListener('click', function() {
            const commentId = this.dataset.commentId;
            window.location.href = `/post/${postId}/comment/${commentId}/edit`;
        });
    });
    
    // Handle the deletion of a comment when the delete comment icon is clicked
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
    
    // Redirect to the edit reply page when the edit reply icon is clicked
    document.querySelectorAll('.edit-reply-icon').forEach(icon => {
        icon.addEventListener('click', function() {
            const replyId = this.dataset.replyId;
            window.location.href = `/post/${postId}/reply/${replyId}/edit`;
        });
    });
    
    // Handle the deletion of a reply when the delete reply icon is clicked
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

    // Function to add event listeners to 'read more' links
    function addReadMoreEventListeners() {
        document.querySelectorAll('.read-more').forEach(link => {
            link.addEventListener('click', function(event) {
                event.preventDefault();
                const fullContent = this.getAttribute('data-full-content');
                const articleContent = this.closest('.article-content');
                if (this.textContent === 'Read more') {
                    articleContent.innerHTML = fullContent + 
                        ' <a href="#" class="read-more" data-full-content="' + 
                        fullContent + '">Show less</a>';
                } else {
                    articleContent.innerHTML = fullContent.split(' ')
                        .slice(0, 20).join(' ') + 
                        '... <a href="#" class="read-more" data-full-content="' + 
                        fullContent + '">Read more</a>';
                }
                addReadMoreEventListeners();
            });
        });
    }

    // Initialize 'read more' event listeners
    addReadMoreEventListeners();
});
