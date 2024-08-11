document.addEventListener('DOMContentLoaded', function() {
    const postCommentBtn = document.getElementById('post-comment-btn');
    const commentInput = document.getElementById('comment-input');
    const commentsDisplayArea = document.getElementById('comments-display-area');
    const toggleCommentsBtn = document.getElementById('toggle-comments-btn');
    const addCommentIcon = document.querySelector('.add-comment-icon');
    const viewCommentsIcon = document.querySelector('.view-comments-icon');
    const commentForm = document.querySelector('.comment-form');
    const commentsDisplay = document.querySelector('.comments-display');

    postCommentBtn.addEventListener('click', function() {
        const content = commentInput.value.trim();
        if (content) {
            postComment(content);
        }
    });

    toggleCommentsBtn.addEventListener('click', function() {
        if (commentsDisplayArea.style.display === 'none' || commentsDisplayArea.style.display === '') {
            commentsDisplayArea.style.display = 'block';
            toggleCommentsBtn.textContent = 'Hide Comments';
        } else {
            commentsDisplayArea.style.display = 'none';
            toggleCommentsBtn.textContent = 'Show Comments';
        }
    });

    addCommentIcon.addEventListener('click', function() {
        commentForm.style.display = commentForm.style.display === 'none' || commentForm.style.display === '' ? 'block' : 'none';
    });

    viewCommentsIcon.addEventListener('click', function() {
        commentsDisplay.style.display = commentsDisplay.style.display === 'none' || commentsDisplay.style.display === '' ? 'block' : 'none';
    });

    function postComment(content) {
        fetch('/comments', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ content: content, post_id: postId })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                addCommentToDisplay(data.comment);
                commentInput.value = '';
            } else {
                showError('Failed to post. Please try again.');
            }
        })
        .catch(() => showError('Failed to post. Please try again.'));
    }

    function addCommentToDisplay(comment) {
        const commentElement = document.createElement('div');
        commentElement.classList.add('comment');
        commentElement.setAttribute('data-id', comment.id);
        commentElement.innerHTML = `
            <div class="commenter-info">
                <img src="${comment.author.profile_picture}" alt="${comment.author.name}" width="30" height="30">
                <span>${comment.author.name}</span>
                <span>${comment.timestamp}</span>
            </div>
            <div class="comment-content">${comment.content}</div>
            <div class="reactions">
                <span class="reply-btn">Reply</span>
                <span class="reaction-icon">👍</span><span>${comment.reactions.like}</span>
            </div>
            <div class="reply-box" style="display: none;">
                <textarea placeholder="Add a reply..."></textarea>
                <button>Reply</button>
            </div>
        `;
        commentsDisplayArea.appendChild(commentElement);

        const replyBtn = commentElement.querySelector('.reply-btn');
        replyBtn.addEventListener('click', function() {
            const replyBox = commentElement.querySelector('.reply-box');
            replyBox.style.display = replyBox.style.display === 'none' ? 'block' : 'none';
        });

        const replyBoxBtn = commentElement.querySelector('.reply-box button');
        replyBoxBtn.addEventListener('click', function() {
            const replyContent = commentElement.querySelector('.reply-box textarea').value.trim();
            if (replyContent) {
                postReply(replyContent, comment.id);
            }
        });
    }

    function postReply(content, parentCommentId) {
        fetch('/comments', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ content: content, post_id: postId, parent_comment_id: parentCommentId })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                addReplyToDisplay(data.comment, parentCommentId);
            } else {
                showError('Failed to post. Please try again.');
            }
        })
        .catch(() => showError('Failed to post. Please try again.'));
    }

    function addReplyToDisplay(reply, parentCommentId) {
        const parentComment = document.querySelector(`.comment[data-id="${parentCommentId}"]`);
        const replyBox = parentComment.querySelector('.reply-box');
        const replyElement = document.createElement('div');
        replyElement.classList.add('comment');
        replyElement.innerHTML = `
            <div class="commenter-info">
                <img src="${reply.author.profile_picture}" alt="${reply.author.name}" width="30" height="30">
                <span>${reply.author.name}</span>
                <span>${reply.timestamp}</span>
            </div>
            <div class="comment-content">${reply.content}</div>
            <div class="reactions">
                <span class="reaction-icon">👍</span><span>${reply.reactions.like}</span>
            </div>
        `;
        replyBox.appendChild(replyElement);
    }

    function showError(message) {
        const errorMessage = document.createElement('div');
        errorMessage.classList.add('error-message');
        errorMessage.textContent = message;
        commentsDisplayArea.appendChild(errorMessage);
    }
});
