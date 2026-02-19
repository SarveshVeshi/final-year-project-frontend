// HandSignify Frontend Motion System
// - Hero reveal, section scroll animations, magnetic buttons, cursor glow

(function () {
  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function initCursorGlow() {
    const glow = document.createElement('div');
    glow.className = 'cursor-glow';
    document.body.appendChild(glow);

    let visible = false;
    window.addEventListener('mousemove', (e) => {
      if (!visible) {
        glow.style.opacity = '1';
        visible = true;
      }
      glow.style.left = `${e.clientX}px`;
      glow.style.top = `${e.clientY}px`;
    });

    window.addEventListener('mouseleave', () => {
      glow.style.opacity = '0';
      visible = false;
    });
  }

  function initMagneticButtons() {
    const selector =
      '.btn-primary, .btn-outline, .btn-generate, .btn-danger-custom, .nav-link, .navbar-brand';
    const buttons = Array.from(document.querySelectorAll(selector));
    if (!buttons.length) return;

    const strength = 18;

    buttons.forEach((btn) => {
      btn.style.willChange = 'transform';
      btn.addEventListener('mousemove', (e) => {
        const rect = btn.getBoundingClientRect();
        const x = e.clientX - rect.left - rect.width / 2;
        const y = e.clientY - rect.top - rect.height / 2;
        const dx = (x / rect.width) * strength;
        const dy = (y / rect.height) * strength;
        btn.style.transform = `translate(${dx}px, ${dy}px)`;
      });

      btn.addEventListener('mouseleave', () => {
        btn.style.transform = 'translate(0, 0)';
      });
    });
  }

  function initGsapAnimations() {
    if (typeof gsap === 'undefined' || prefersReducedMotion) {
      // Fallback: mark elements visible without animation
      document.querySelectorAll('[data-animate]').forEach((el) => {
        el.style.opacity = 1;
        el.style.transform = 'none';
      });
      return;
    }

    // Hero reveal
    const hero = document.querySelector('.hero-section .glass-hero');
    if (hero) {
      gsap.from(hero, {
        duration: 1.1,
        opacity: 0,
        y: 40,
        filter: 'blur(10px)',
        ease: 'power3.out',
      });
    }

    // Feature cards stagger
    const featureCards = document.querySelectorAll('.hero-section .card, .generator-card .card');
    if (featureCards.length) {
      gsap.from(featureCards, {
        duration: 0.9,
        opacity: 0,
        y: 30,
        stagger: 0.08,
        delay: 0.2,
        ease: 'power2.out',
      });
    }

    // Scroll-triggered sections
    if (typeof ScrollTrigger !== 'undefined') {
      gsap.utils.toArray('[data-animate="section"]').forEach((section) => {
        gsap.from(section, {
          opacity: 0,
          y: 40,
          scale: 0.98,
          duration: 0.8,
          ease: 'power2.out',
          scrollTrigger: {
            trigger: section,
            start: 'top 78%',
          },
        });
      });
    }
  }

  document.addEventListener('DOMContentLoaded', () => {
    initCursorGlow();
    initMagneticButtons();
    initGsapAnimations();
  });
})();

