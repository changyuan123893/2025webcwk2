// Favorites handling
document.addEventListener('DOMContentLoaded', function() {
    initializeFavoriteButtons();
    setupFavoriteEventListeners();
});

function initializeFavoriteButtons() {
    document.querySelectorAll('.favorite-btn').forEach(button => {
        const movieId = button.dataset.movieId;
        const isAuthenticated = button.dataset.authenticated === 'true';
        const isFavorite = button.dataset.initialFavorite === 'true';

        updateButtonAppearance(button, isFavorite);

        // Set ARIA attributes
        updateButtonAria(button, movieId, isFavorite);
    });
}

function setupFavoriteEventListeners() {
    // Use event delegation
    document.addEventListener('click', function(e) {
        const favoriteBtn = e.target.closest('.favorite-btn');
        if (favoriteBtn) {
            e.preventDefault();

            // Redirect to login if user is not authenticated
            if (favoriteBtn.dataset.authenticated !== 'true') {
                window.location.href = '/login';
                return;
            }

            handleFavoriteToggle(favoriteBtn);
        }
    });
}

function handleFavoriteToggle(button) {
    const movieId = button.dataset.movieId;
    const currentState = button.dataset.initialFavorite === 'true';

    // loading state
    const originalHTML = button.innerHTML;
    button.innerHTML = '<i class="bi bi-hourglass"></i>';
    button.disabled = true;

    fetch(`/favorite/${movieId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        console.log('Favorite action response:', data);

        if (data.status === 'success') {
            // update button state
            button.dataset.initialFavorite = data.new_state;
            updateButtonAppearance(button, data.new_state);
            updateButtonAria(button, movieId, data.new_state);

            // Update all buttons for the same movie
            updateAllFavoriteButtons(movieId, data.new_state);

            // Update favorite counts
            updateFavoriteCounts(movieId, data.favorite_count);

            //remove list entries
            if (data.action === 'removed') {
                document.querySelectorAll(`.favorite-btn[data-movie-id="${movieId}"]`).forEach(btn => {
                    const li = btn.closest('li');
                    if (li && li.parentElement && li.parentElement.classList.contains('list-group')) {
                        li.remove();
                    }
                });

                // If favorites list is empty, show a short prompt
                const list = document.querySelector('.list-group');
                if (list && list.children.length === 0) {
                    const container = list.parentElement;
                    if (container) {
                        container.innerHTML = `\n                            <p class="text-muted">You don't have any favorite movies yet.</p>\n                            <a href="/movies" class="btn btn-primary btn-sm">Browse movies</a>\n                        `;
                    }
                }
            }
            // Show a notification using the backend message
            showNotification(data.message, 'success');
        } else {
            showNotification(data.message || 'Operation failed', 'error');
        }
    })
    .catch(error => {
        console.error('Request error:', error);
        showNotification('Network error, please try again later', 'error');
    })
    .finally(() => {
        // Restore button state
        button.disabled = false;
        button.innerHTML = originalHTML;
        // restore button appearance
        const isFavorite = button.dataset.initialFavorite === 'true';
        updateButtonAppearance(button, isFavorite);
    });
}

function updateButtonAppearance(button, isFavorite) {
    const icon = button.querySelector('i');
    const textSpan = button.querySelector('.favorite-text');

    if (isFavorite) {
        // Favorited state - solid red
        button.classList.remove('btn-outline-danger');
        button.classList.add('btn-danger', 'active');
        if (icon) icon.className = 'bi bi-heart-fill';
        if (textSpan) textSpan.textContent = 'Favorited';
    } else {
        // Not favorited state - red outline
        button.classList.remove('btn-danger', 'active');
        button.classList.add('btn-outline-danger');
        if (icon) icon.className = 'bi bi-heart';
        if (textSpan) textSpan.textContent = 'Favorite';
    }
}

function updateButtonAria(button, movieId, isFavorite) {
    button.setAttribute('aria-label',
        isFavorite ? `Remove favorite movie ID: ${movieId}` : `Favorite movie ID: ${movieId}`);
    button.setAttribute('aria-pressed', isFavorite);
}

function updateAllFavoriteButtons(movieId, isFavorite) {
    document.querySelectorAll(`.favorite-btn[data-movie-id="${movieId}"]`).forEach(btn => {
        btn.dataset.initialFavorite = isFavorite;
        updateButtonAppearance(btn, isFavorite);
        updateButtonAria(btn, movieId, isFavorite);
    });
}

function updateFavoriteCounts(movieId, count) {
    // Update all favorite count displays
    document.querySelectorAll(`.favorite-count[data-movie-id="${movieId}"]`).forEach(element => {
        element.textContent = count;
    });

    // Update favorite counts in summary widgets
    document.querySelectorAll('.h4.favorite-count').forEach(element => {
        if (element.dataset.movieId === movieId) {
            element.textContent = count;
        }
    });
}

function showNotification(message, type = 'info') {
    // Remove any existing notifications
    const existingNotifications = document.querySelectorAll('.favorite-notification');
    existingNotifications.forEach(notification => {
        if (notification.parentNode) {
            notification.parentNode.removeChild(notification);
        }
    });

    // create notification element
    const notification = document.createElement('div');
    notification.className = `favorite-notification alert alert-${type} alert-dismissible fade show`;
    notification.setAttribute('role', 'alert');
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;

    // append to notification container or body
    const container = document.getElementById('notification-container') || document.body;
    container.appendChild(notification);

    // auto-dismiss
    setTimeout(() => {
        if (notification.parentNode) {
            notification.classList.remove('show');
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
            }, 300);
        }
    }, 3000);
}