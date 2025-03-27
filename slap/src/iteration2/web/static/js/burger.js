

function toggleMenu() {
    const overlay = document.getElementById('menuOverlay');
    overlay.classList.toggle('active');
}

// Close menu when clicking outside
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('menuOverlay').addEventListener('click', function(e) {
        console.log("clicked")
        if (e.target === this) {
            this.classList.remove('active');
        }
    });
});