/**
 * Premium Animations - GSAP Implementation
 * Adds smooth, professional animations throughout the HandSignify application
 */

// Wait for GSAP and DOM to be ready
document.addEventListener('DOMContentLoaded', () => {
    // Check if GSAP is loaded
    if (typeof gsap === 'undefined') {
        console.warn('GSAP not loaded - animations disabled');
        return;
    }

    // ==========================================
    // 1. PAGE ENTRANCE ANIMATIONS
    // ==========================================

    // Fade in and slide up animation for main content
    // Fade in and slide up animation for main content with ScrollTrigger re-trigger
    if (typeof ScrollTrigger !== 'undefined') {
        gsap.from('header.main-container', {
            scrollTrigger: {
                trigger: 'header.main-container',
                start: 'top 80%', // Start animation when top of element hits 80% of viewport
                end: 'bottom 20%', // Define end trigger
                toggleActions: 'play reverse play reverse' // Play on enter, reverse on leave, play on enter back, reverse on leave back
            },
            duration: 0.8,
            opacity: 0,
            y: 30,
            ease: 'power3.out'
        });
    } else {
        // Fallback if ScrollTrigger is not available
        gsap.from('header.main-container', {
            duration: 0.8,
            opacity: 0,
            y: 30,
            ease: 'power3.out',
            delay: 0.2
        });
    }

    // Stagger animation for feature cards
    gsap.from('.card', {
        duration: 0.6,
        opacity: 0,
        y: 40,
        stagger: 0.15,
        ease: 'power2.out',
        delay: 0.4,
        clearProps: 'all' // Allow hover effects to work properly
    });

    // Animate team cards if they exist
    if (document.querySelector('.team-card')) {
        gsap.from('.team-card', {
            duration: 0.7,
            opacity: 0,
            y: 50,
            stagger: 0.1,
            ease: 'back.out(1.2)',
            delay: 0.3,
            clearProps: 'all'
        });
    }

    // ==========================================
    // 2. SCROLL-TRIGGERED ANIMATIONS
    // ==========================================

    // Register ScrollTrigger plugin if available
    if (typeof ScrollTrigger !== 'undefined') {
        gsap.registerPlugin(ScrollTrigger);

        // Animate sections on scroll
        const sections = document.querySelectorAll('section:not(.mb-5)');
        sections.forEach((section, index) => {
            gsap.from(section, {
                scrollTrigger: {
                    trigger: section,
                    start: 'top 80%',
                    toggleActions: 'play none none reverse'
                },
                duration: 0.8,
                opacity: 0,
                y: 30,
                ease: 'power2.out'
            });
        });

        // Parallax effect for hero section
        const hero = document.querySelector('header.main-container');
        if (hero) {
            gsap.to(hero, {
                scrollTrigger: {
                    trigger: hero,
                    start: 'top top',
                    end: 'bottom top',
                    scrub: true
                },
                y: -50,
                // opacity: 0.8,  <-- REMOVED to avoid conflict with entrance animation
                ease: 'none'
            });
        }
    }

    // ==========================================
    // 3. BUTTON GLOW PULSE ANIMATION
    // ==========================================

    const primaryButtons = document.querySelectorAll('.btn-primary:not(input)');
    primaryButtons.forEach(btn => {
        // Add subtle pulse on hover
        btn.addEventListener('mouseenter', () => {
            gsap.to(btn, {
                duration: 0.6,
                boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05), 0 0 20px rgba(37, 99, 235, 0.4), 0 0 40px rgba(37, 99, 235, 0.2)',
                repeat: -1,
                yoyo: true,
                ease: 'power1.inOut'
            });
        });

        btn.addEventListener('mouseleave', () => {
            gsap.killTweensOf(btn);
            gsap.to(btn, {
                duration: 0.3,
                boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
                ease: 'power2.out'
            });
        });
    });

    // ==========================================
    // 4. FLOATING BACKGROUND BLOBS
    // ==========================================

    // Create floating blobs container if not exists
    if (!document.querySelector('.floating-blobs-container')) {
        const blobsContainer = document.createElement('div');
        blobsContainer.className = 'floating-blobs-container';
        blobsContainer.style.cssText = 'position: fixed; top: 0; left: 0; width: 100%; height: 100%; overflow: hidden; pointer-events: none; z-index: -1;';

        // Create two subtle floating blobs
        const blob1 = document.createElement('div');
        blob1.className = 'floating-blob floating-blob-1';

        const blob2 = document.createElement('div');
        blob2.className = 'floating-blob floating-blob-2';

        blobsContainer.appendChild(blob1);
        blobsContainer.appendChild(blob2);
        document.body.appendChild(blobsContainer);
    }

    // ==========================================
    // 5. MICRO-INTERACTIONS
    // ==========================================

    // Add hover lift effect to all cards
    const cards = document.querySelectorAll('.card, .team-card');
    cards.forEach(card => {
        card.addEventListener('mouseenter', () => {
            gsap.to(card, {
                duration: 0.3,
                y: -8,
                boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
                ease: 'power2.out'
            });
        });

        card.addEventListener('mouseleave', () => {
            gsap.to(card, {
                duration: 0.3,
                y: 0,
                boxShadow: '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
                ease: 'power2.out'
            });
        });
    });

    // Icon rotation on hover
    const icons = document.querySelectorAll('[data-lucide]');
    icons.forEach(icon => {
        icon.parentElement.addEventListener('mouseenter', () => {
            gsap.to(icon, {
                duration: 0.5,
                rotation: 10,
                scale: 1.1,
                ease: 'back.out(2)'
            });
        });

        icon.parentElement.addEventListener('mouseleave', () => {
            gsap.to(icon, {
                duration: 0.4,
                rotation: 0,
                scale: 1,
                ease: 'power2.out'
            });
        });
    });

    // ==========================================
    // 6. NAVBAR SCROLL EFFECT
    // ==========================================

    const navbar = document.querySelector('.navbar');
    if (navbar && typeof ScrollTrigger !== 'undefined') {
        ScrollTrigger.create({
            start: 'top -80',
            end: 99999,
            toggleClass: {
                className: 'navbar-scrolled',
                targets: navbar
            }
        });

        // Add navbar scrolled styles
        const style = document.createElement('style');
        style.textContent = `
            .navbar-scrolled {
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06) !important;
                transition: box-shadow 0.3s ease;
            }
        `;
        document.head.appendChild(style);
    }

    // ==========================================
    // 7. VIDEO BACKGROUND OPTIMIZATION
    // ==========================================

    const videoBackground = document.querySelector('.video-background video');
    if (videoBackground) {
        // Ensure video is playing
        videoBackground.play().catch(err => {
            console.log('Video autoplay prevented:', err);
        });

        // Pause video when not in viewport to save resources
        if (typeof IntersectionObserver !== 'undefined') {
            const videoObserver = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        videoBackground.play();
                    } else {
                        videoBackground.pause();
                    }
                });
            });
            videoObserver.observe(videoBackground);
        }
    }

    console.log('✨ Premium animations initialized');
});
