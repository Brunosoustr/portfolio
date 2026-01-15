// Aguarda o carregamento completo da página, incluindo imagens
window.onload = () => {
    gsap.registerPlugin(ScrollTrigger);

    // --- Animação Profissional e Robusta ---

    // 1. Header com Scrub
    // O header desaparece suavemente conforme o usuário rola para baixo
    gsap.to('.project-header', {
        autoAlpha: 0, // Anima opacidade e visibilidade
        scrollTrigger: {
            trigger: '.project-header',
            start: 'top top',
            end: '+=150', // Desaparece nos primeiros 150px de scroll
            scrub: true,
        },
    });

    // 2. Animação para Seções de Análise
    // Cada seção aparece de forma elegante e escalonada
    document.querySelectorAll('.analysis-section').forEach(section => {
        const contentElements = section.querySelectorAll('.text, .chart');
        
        gsap.from(contentElements, {
            autoAlpha: 0,
            y: 50,
            duration: 0.8,
            stagger: 0.2, // Anima texto e gráfico com um pequeno atraso entre eles
            ease: 'power3.out',
            scrollTrigger: {
                trigger: section,
                start: 'top 75%', // Começa a animação um pouco antes
                toggleActions: 'play reverse play reverse',
            },
        });
    });

    // 3. Animação para os Cards de Ferramentas
    // Garante que a animação comece de forma limpa e escalonada
    gsap.from('.tool-card', {
        autoAlpha: 0,
        y: 50,
        duration: 0.7,
        stagger: 0.15,
        ease: 'power3.out',
        scrollTrigger: {
            trigger: '.tool-section',
            start: 'top 80%',
            toggleActions: 'play reverse play reverse',
        },
    });

    // Força o ScrollTrigger a recalcular as posições após tudo estar carregado.
    // Isso é CRUCIAL para evitar que as animações quebrem por causa do carregamento de imagens.
    ScrollTrigger.refresh();
};