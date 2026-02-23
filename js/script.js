document.addEventListener('DOMContentLoaded', () => {

    // ── GSAP Registration ──────────────────────────────────────────
    gsap.registerPlugin(ScrollTrigger);

    // ── Header: scrolled class ─────────────────────────────────────
    const header = document.querySelector('.header');
    window.addEventListener('scroll', () => {
        header.classList.toggle('scrolled', window.pageYOffset > 60);
    }, { passive: true });

    // ── Hero Animations ────────────────────────────────────────────
    gsap.from('.header', { y: -70, opacity: 0, duration: 0.8, ease: 'power3.out' });

    // ── Project Cards: always visible, subtle fade on scroll ───────
    const projectCards = document.querySelectorAll('.project-card');
    if (projectCards.length) {
        gsap.set(projectCards, { opacity: 1, y: 0, visibility: 'visible' });
        gsap.from(projectCards, {
            opacity: 0, y: 40, duration: 0.7, ease: 'power3.out', stagger: 0.18,
            scrollTrigger: { trigger: '.projects-section', start: 'top 80%', toggleActions: 'play none none none' }
        });
    }

    // ── Project Cards: subtle 3-D tilt ─────────────────────────────
    projectCards.forEach(card => {
        card.addEventListener('mousemove', e => {
            const r = card.getBoundingClientRect();
            const rx = ((e.clientY - r.top) / r.height - 0.5) * 8;
            const ry = ((e.clientX - r.left) / r.width - 0.5) * -8;
            gsap.to(card, { rotationX: rx, rotationY: ry, ease: 'power1.out', duration: 0.3 });
        });
        card.addEventListener('mouseleave', () => {
            gsap.to(card, { rotationX: 0, rotationY: 0, ease: 'power1.out', duration: 0.5 });
        });
    });

    // ── Horizontal Scroll (About) ──────────────────────────────────
    const horizontalSection = document.querySelector('.about-section-horizontal');
    const wrapper = document.querySelector('.horizontal-wrapper');
    const panels = gsap.utils.toArray('.panel');

    if (!horizontalSection || !wrapper || !panels.length) return;

    // Mobile / tablet: stack vertically
    if (window.innerWidth <= 1024) {
        panels.forEach(panel => {
            const content = panel.querySelector('.panel-content');
            if (content) {
                gsap.from(content, {
                    opacity: 0, y: 30, duration: 0.7, ease: 'power3.out',
                    scrollTrigger: { trigger: panel, start: 'top 85%', toggleActions: 'play none none none' }
                });
            }
        });
        return;
    }

    // ── Progress bar ───────────────────────────────────────────────
    const progressBar = document.createElement('div');
    Object.assign(progressBar.style, {
        position: 'fixed',
        top: '0',
        left: '0',
        width: '0%',
        height: '3px',
        background: 'linear-gradient(90deg, #2563eb, #10b981)',
        zIndex: '999',
        transition: 'width 0.08s linear',
        borderRadius: '0 2px 2px 0',
    });
    document.body.appendChild(progressBar);

    // ── Dot indicators (right side) ────────────────────────────────
    const dotsWrap = document.createElement('div');
    dotsWrap.className = 'panel-indicators-container';
    Object.assign(dotsWrap.style, {
        position: 'fixed',
        right: '1.75rem',
        top: '50%',
        transform: 'translateY(-50%)',
        zIndex: '200',
        display: 'flex',
        flexDirection: 'column',
        gap: '0.7rem',
        alignItems: 'center',
    });

    // Panel labels for tooltip text
    const panelLabels = ['Resumo', 'Experiência', 'Formação', 'Skills'];

    panels.forEach((panel, i) => {
        const dot = document.createElement('button');
        dot.className = 'panel-indicator';
        dot.setAttribute('aria-label', panelLabels[i] || `Painel ${i + 1}`);
        dot.title = panelLabels[i] || '';
        Object.assign(dot.style, {
            width: '8px',
            height: '8px',
            borderRadius: '50%',
            border: 'none',
            background: 'rgba(37, 99, 235, 0.15)',
            cursor: 'pointer',
            padding: '0',
            transition: 'all 0.3s',
            outline: 'none',
        });
        dotsWrap.appendChild(dot);
    });
    document.body.appendChild(dotsWrap);

    const dots = dotsWrap.querySelectorAll('.panel-indicator');

    function setActiveDot(idx) {
        dots.forEach((d, i) => {
            if (i === idx) {
                Object.assign(d.style, {
                    background: '#2563eb',
                    transform: 'scale(1.6)',
                    boxShadow: '0 0 0 3px rgba(37, 99, 235, 0.15)',
                });
                panels[i].classList.add('is-active');
            } else {
                Object.assign(d.style, {
                    background: 'rgba(37, 99, 235, 0.15)',
                    transform: 'scale(1)',
                    boxShadow: 'none',
                });
                panels[i].classList.remove('is-active');
            }
        });
    }

    setActiveDot(0);

    // ── GSAP Horizontal Scroll Tween ───────────────────────────────
    const scrollTween = gsap.to(panels, {
        xPercent: -100 * (panels.length - 1),
        ease: 'none',
        scrollTrigger: {
            trigger: '.about-section-horizontal',
            pin: true,
            scrub: 0.5,
            end: () => '+=' + (panels.length * 100) + '%',
            onUpdate: self => {
                const progress = self.progress;

                // Progress bar width
                progressBar.style.width = `${progress * 100}%`;

                // Active dot
                const activeIdx = Math.min(
                    Math.round(progress * (panels.length - 1)),
                    panels.length - 1
                );
                setActiveDot(activeIdx);
            },
        },
    });

    // ── Dot click: scroll to matching panel position ────────────────
    dots.forEach((dot, i) => {
        dot.addEventListener('click', () => {
            const st = scrollTween.scrollTrigger;
            const total = st.end - st.start;
            const fraction = i / (panels.length - 1);
            window.scrollTo({ top: st.start + total * fraction, behavior: 'smooth' });
        });
    });

    // ── Panel content entrance animation ───────────────────────────
    panels.forEach((panel, i) => {
        const content = panel.querySelector('.panel-content');
        if (!content) return;
        gsap.from(content, {
            opacity: 0,
            x: 40,
            duration: 0.8,
            ease: 'power3.out',
            scrollTrigger: {
                trigger: panel,
                containerAnimation: scrollTween,
                start: 'left 80%',
                end: 'left 30%',
                scrub: true,
            },
        });
    });

    // ── Keyboard navigation for panels ─────────────────────────────
    document.addEventListener('keydown', e => {
        if (!scrollTween.scrollTrigger) return;
        const st = scrollTween.scrollTrigger;
        const total = st.end - st.start;
        const progress = st.progress;
        const current = Math.round(progress * (panels.length - 1));

        if (e.key === 'ArrowRight' && current < panels.length - 1) {
            e.preventDefault();
            const next = (current + 1) / (panels.length - 1);
            window.scrollTo({ top: st.start + total * next, behavior: 'smooth' });
        }
        if (e.key === 'ArrowLeft' && current > 0) {
            e.preventDefault();
            const prev = (current - 1) / (panels.length - 1);
            window.scrollTo({ top: st.start + total * prev, behavior: 'smooth' });
        }
    });

    // ── Smooth scroll for nav links ────────────────────────────────
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        });
    });

    // ── Force refresh after all images load ───────────────────────
    ScrollTrigger.refresh();
    window.addEventListener('load', () => ScrollTrigger.refresh());
});
