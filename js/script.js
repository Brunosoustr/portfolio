document.addEventListener('DOMContentLoaded', () => {

    // --- GSAP Registration ---
    gsap.registerPlugin(ScrollTrigger);

    // --- Header Animation ---
    gsap.from('.header', {
        y: -100,
        opacity: 0,
        duration: 1,
        ease: 'power3.out'
    });

    // --- Hero Content Animation ---
    gsap.from('.hero-title', {
        y: 50,
        opacity: 0,
        duration: 1,
        ease: 'power3.out',
        delay: 0.5
    });

    gsap.from('.hero-subtitle', {
        y: 50,
        opacity: 0,
        duration: 1,
        ease: 'power3.out',
        delay: 0.7
    });

    gsap.from('.hero .btn', {
        scale: 0,
        opacity: 0,
        duration: 0.8,
        ease: 'back.out(1.7)',
        delay: 0.9
    });
    
    // --- Project Cards Animation (Staggered Fade In) ---
    // Instead of hiding the whole section, we animate the cards inside
    gsap.from('.project-card', {
        opacity: 0,
        y: 50,
        duration: 0.8,
        ease: 'power3.out',
        stagger: 0.2,
        scrollTrigger: {
            trigger: '.projects-grid',
            start: 'top 85%',
        }
    });

    // --- Project Cards Tilt Effect ---
    const cards = document.querySelectorAll('.project-card');
    cards.forEach(card => {
        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;
            const rotateX = (y - centerY) / 20;
            const rotateY = (centerX - x) / 20;

            gsap.to(card, {
                rotationX: rotateX,
                rotationY: rotateY,
                scale: 1.05,
                ease: 'power1.out'
            });
        });

        card.addEventListener('mouseleave', () => {
            gsap.to(card, {
                rotationX: 0,
                rotationY: 0,
                scale: 1,
                ease: 'power1.out'
            });
        });
    });

    // --- "About Me" Horizontal Scroll Section ---
    const horizontalSection = document.querySelector(".about-section-horizontal");
    const wrapper = document.querySelector(".horizontal-wrapper");
    const panels = gsap.utils.toArray(".panel");

    if (horizontalSection && wrapper && panels.length > 0) {
        gsap.to(panels, {
            xPercent: -100 * (panels.length - 1),
            ease: "none",
            scrollTrigger: {
                trigger: ".about-section-horizontal",
                pin: true,
                scrub: 1,
                // Snap to each panel automatically
                snap: {
                    snapTo: 1 / (panels.length - 1),
                    duration: {min: 0.2, max: 0.5},
                    delay: 0
                },
                // Duration of the scroll (how long it stays pinned)
                end: () => "+=" + (panels.length * 100) + "%" 
            }
        });
    }

    // --- Force ScrollTrigger Refresh ---
    // Ensures positions are calculated correctly after DOM load
    ScrollTrigger.refresh();

});
