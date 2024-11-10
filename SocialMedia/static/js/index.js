console.log('jQuery version:', $.fn.jquery);
console.log('index.js is loaded');

function toggleMenu() {
    const navItems = document.querySelector('.nav-items');
    navItems.classList.toggle('active');
    document.body.classList.toggle('menu-open');
}

document.addEventListener('DOMContentLoaded', () => {
    // Toggle comments section
    const commentToggleButtons = document.querySelectorAll('.comment-toggle-button');
    commentToggleButtons.forEach(button => {
        button.addEventListener('click', () => {
            const commentSection = button.parentElement.nextElementSibling;
            commentSection.style.display = commentSection.style.display === 'block' ? 'none' : 'block';
        });
    });

    // Submit comment
    const submitCommentButtons = document.querySelectorAll('.submit-comment-button');
    submitCommentButtons.forEach(button => {
        button.addEventListener('click', () => {
            const commentInput = button.previousElementSibling;
            const commentContent = commentInput.value.trim();
            const commentsList = button.parentElement.previousElementSibling;

            if (commentContent) {
                const newComment = document.createElement('div');
                newComment.textContent = `You: ${commentContent}`;
                commentsList.appendChild(newComment);
                commentInput.value = '';

                // Optional: AJAX to submit the comment
                const postId = button.getAttribute('data-post-id');
                const csrfToken = '{{ csrf_token }}';

                $.ajax({
                    url: "{% url 'add_comment' %}",
                    type: 'POST',
                    data: {
                        'post_id': postId,
                        'content': commentContent,
                        'csrfmiddlewaretoken': csrfToken
                    },
                    success: function(response) {
                        // Handle success (e.g., append response comment)
                        const commentHtml = `<div>${response.author}: ${response.content}</div>`;
                        commentsList.appendChild(commentHtml);
                    },
                    error: function(xhr, status, error) {
                        console.error(error);
                    }
                });
            } else {
                alert("Please enter a comment.");
            }
        });
    });

    // Event listeners for delete buttons
    document.querySelectorAll('.delete-button').forEach(button => {
        button.addEventListener('click', function() {
            const postId = this.getAttribute('data-post-id');
            deletePost(postId);
        });
    });
});
