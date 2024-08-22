//3D Tilt effect on cards hover
document.addEventListener('DOMContentLoaded', function() {
    const cards = document.querySelectorAll('.category-card .card');

    cards.forEach(card => {
        card.addEventListener('mousemove', handleMouseMove);
        card.addEventListener('mouseleave', handleMouseLeave);
    });

    function handleMouseMove(e) {
        const card = this;
        const cardRect = card.getBoundingClientRect();
        const cardCenterX = cardRect.left + cardRect.width / 2;
        const cardCenterY = cardRect.top + cardRect.height / 2;
        const mouseX = e.clientX - cardCenterX;
        const mouseY = e.clientY - cardCenterY;
        const rotateY = (mouseX / cardRect.width) * 20;
        const rotateX = -(mouseY / cardRect.height) * 20;

        card.style.transform = `rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale(1.05)`;
    }

    function handleMouseLeave(e) {
        this.style.transform = 'rotateX(0) rotateY(0) scale(1)';
    }
});
