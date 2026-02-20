/**
 * premium-animations.js — HandSignify v2.0
 * Smooth entrance animations, micro-interactions, and cursor glow.
 * Depends on: GSAP (optional, gracefully degrades)
 */

(function () {
    'use strict';

    /* ── Cursor glow (desktop only) ─────────────────────── */
    const glow = document.getElementById('cursorGlow');
    if (glow && window.innerWidth > 768) {
        let glowX = -200, glowY = -200;
        let rafId;

        document.addEventListener('mousemove', (e) => {
            const dx = e.clientX - glowX;
            const dy = e.clientY - glowY;
            cancelAnimationFrame(rafId);
            rafId = requestAnimationFrame(() => {
                glowX += dx * 0.12;
                glowY += dy * 0.12;
                glow.style.left = glowX + 'px';
                glow.style.top  = glowY + 'px';
                glow.style.opacity = '1';
            });
        });

        document.addEventListener('mouseleave', () => {
            glow.style.opacity = '0';
        });
    }

    /* ── Navbar scroll shadow ───────────────────────────── */
    const navbar = document.querySelector('.navbar');
    if (navbar) {
        const observer = new IntersectionObserver(
            ([e]) => navbar.classList.toggle('navbar-scrolled', e.intersectionRatio < 1),
            { threshold: [1], rootMargin: '-1px 0px 0px 0px' }
        );
        const sentinel = document.createElement('div');
        sentinel.style.height = '1px';
        document.body.prepend(sentinel);
        observer.observe(sentinel);
    }

    /* ── Wait for DOM ───────────────────────────────────── */
    document.addEventListener('DOMContentLoaded', () => {

        /* ── Lucide Icons ───────────────────────────────── */
        if (typeof lucide !== 'undefined') lucide.createIcons();

        /* ── Button ripple effect ───────────────────────── */
        document.querySelectorAll('.btn-primary, .btn-generate, .btn-danger-custom').forEach(btn => {
            btn.addEventListener('click', function (e) {
                const ripple = document.createElement('span');
                const rect   = btn.getBoundingClientRect();
                const size   = Math.max(rect.width, rect.height);
                ripple.style.cssText = `
                    position:absolute;
                    border-radius:50%;
                    background:rgba(255,255,255,0.35);
                    width:${size}px;height:${size}px;
                    left:${e.clientX - rect.left - size/2}px;
                    top:${e.clientY - rect.top  - size/2}px;
                    transform:scale(0);
                    animation:rippleAnim 0.55s ease-out forwards;
                    pointer-events:none;
                `;
                btn.style.position = 'relative';
                btn.style.overflow = 'hidden';
                btn.appendChild(ripple);
                ripple.addEventListener('animationend', () => ripple.remove());
            });
        });

        /* Inject ripple keyframes once */
        if (!document.getElementById('ripple-style')) {
            const st = document.createElement('style');
            st.id = 'ripple-style';
            st.textContent = '@keyframes rippleAnim{to{transform:scale(3.5);opacity:0;}}';
            document.head.appendChild(st);
        }

        /* ── Stagger entrance for feature cards ─────────── */
        const cards = document.querySelectorAll(
            '.hs-feature-card, .hs-step-card, .hs-hero-panel, .card, .team-card'
        );

        if (typeof gsap !== 'undefined' && cards.length) {
            gsap.registerPlugin(ScrollTrigger);

            cards.forEach((card, i) => {
                gsap.from(card, {
                    scrollTrigger: {
                        trigger: card,
                        start: 'top 88%',
                        once: true,
                    },
                    duration: 0.55,
                    opacity: 0,
                    y: 28,
                    delay: (i % 4) * 0.08,
                    ease: 'power2.out',
                    clearProps: 'all'
                });
            });

            /* Hero copy fade-in */
            const heroCopy = document.querySelector('.hs-hero-copy');
            if (heroCopy) {
                gsap.from(heroCopy.children, {
                    duration: 0.7,
                    opacity: 0,
                    y: 22,
                    stagger: 0.1,
                    ease: 'power3.out',
                    delay: 0.1,
                    clearProps: 'all'
                });
            }
        } else if (!typeof gsap !== 'undefined') {
            /* CSS-only fallback: just show everything */
            cards.forEach(c => c.style.opacity = '1');
        }

        /* ── Feature card icon hover ────────────────────── */
        document.querySelectorAll('.hs-feature-card').forEach(card => {
            const icon = card.querySelector('.hs-feature-icon');
            if (!icon) return;
            card.addEventListener('mouseenter', () => {
                if (typeof gsap !== 'undefined') {
                    gsap.to(icon, { duration: 0.3, scale: 1.1, rotate: 5, ease: 'back.out(2)' });
                }
            });
            card.addEventListener('mouseleave', () => {
                if (typeof gsap !== 'undefined') {
                    gsap.to(icon, { duration: 0.25, scale: 1, rotate: 0, ease: 'power2.out' });
                }
            });
        });

        /* ── Auth card entrance ───────────────────────── */
        const authCard = document.querySelector('.auth-card');
        if (authCard && typeof gsap !== 'undefined') {
            gsap.from(authCard, {
                duration: 0.55,
                opacity: 0,
                y: 24,
                ease: 'power3.out',
                clearProps: 'all'
            });
        }

        /* ── Generator card entrance ─────────────────── */
        const genCard = document.querySelector('.generator-card');
        if (genCard && typeof gsap !== 'undefined') {
            gsap.from(genCard, {
                duration: 0.5,
                opacity: 0,
                y: 20,
                ease: 'power2.out',
                clearProps: 'all'
            });
        }

        console.log('✨ HandSignify premium animations v2.0 ready');
    });
})();
