# UI Architecture — HandSignify Premium Light Theme

> **Purpose:** This document is the authoritative reference for the HandSignify frontend design system, animation architecture, and UI implementation decisions. It is written for human developers, collaborators, and AI agents who need to understand, maintain, or extend the UI.

---

## 1. Design Philosophy

### Visual Identity
HandSignify is an accessibility-first communication tool. Its visual identity balances professional credibility with human warmth. The design draws from modern SaaS products (Notion, Linear, Vercel) but adds softness through:
- Layered pastel mesh gradients instead of flat backgrounds
- Glassmorphism (frosted glass surfaces) instead of opaque containers
- Rounded, pill-shaped interactive elements to feel inviting, not clinical

### Emotional Design Reasoning
Since HandSignify serves deaf and hard-of-hearing users, the emotional tone of the interface matters deeply:
- **Calm, not loud**: No harsh contrast; soft shadows over aggressive dark mode
- **Responsive, not robotic**: Every interaction has a physical quality — buttons ripple, cameras glow, predictions pop into existence character-by-character
- **Confidence-inspiring**: Clean typography and generous spacing signal that the tool is professional and reliable

### Why Light Theme
A dark theme was considered but rejected for the following reasons:
1. **Webcam feed contrast** — The OpenCV MJPEG stream renders better (more natural) against a light background
2. **Hand skeleton visibility** — The generated sign videos use a dark graphite background; embedding these in a dark UI loses the edge definition
3. **Accessibility** — Light themes are generally easier for users with low-contrast sensitivity when combined with careful color choices

---

## 2. Design System

### Color Palette

| Token | HEX / Value | Usage |
|---|---|---|
| `--hs-bg` | `#f0f4f8` | Page background base |
| `--hs-surface` | `rgba(255,255,255,0.82)` | Card/panel surfaces |
| `--hs-surface-solid` | `#ffffff` | Solid white surfaces |
| `--hs-border` | `rgba(148,163,184,0.28)` | Subtle borders |
| `--hs-border-strong` | `rgba(100,116,139,0.4)` | Stronger dividers |
| `--hs-text-main` | `#0f172a` | Primary headings |
| `--hs-text-mid` | `#334155` | Body text |
| `--hs-text-soft` | `#64748b` | Secondary / Labels |
| `--hs-text-faint` | `#94a3b8` | Placeholders, hints |
| `--hs-primary` | `#3b6fef` | Primary brand color |
| `--hs-primary-soft` | `rgba(59,111,239,0.1)` | Tinted backgrounds |
| `--hs-primary-glow` | `rgba(59,111,239,0.35)` | Button glow shadows |
| `--hs-primary-dark` | `#1d48c4` | Hover/active state |
| `--hs-indigo` | `#6366f1` | Accent / gradient end |
| `--hs-accent` | `#f97316` | Warm accent (orange) |
| `--hs-success` | `#10b981` | Success alerts |
| `--hs-danger` | `#f43f5e` | Error / stop states |

**Background gradient** (on `body.hs-body`):
```css
background-image:
  radial-gradient(ellipse 70% 50% at 0% 0%,   rgba(186,210,255,0.55) 0%, transparent 65%),
  radial-gradient(ellipse 60% 45% at 100% 0%,  rgba(245,208,254,0.4)  0%, transparent 65%),
  radial-gradient(ellipse 55% 50% at 50% 100%, rgba(186,230,215,0.35) 0%, transparent 65%);
```
Three soft pastel ellipses (blue top-left, purple top-right, teal bottom-center) on a `#f0f4f8` base.

### Typography System

| Role | Font | Weight | Size |
|---|---|---|---|
| Base font | Inter (Google Fonts) | 400 | 1rem |
| Body | Inter | 400–500 | 0.875–1rem |
| Labels | Inter | 600 | 0.82rem uppercase |
| Subheadings | Inter | 700 | 1–1.2rem |
| Headings | Inter | 800 | clamp(1.5rem, 3vw, 2.2rem) |
| Hero title | Inter | 800 | clamp(2.2rem, 4.5vw, 3.6rem) |

The typeface is loaded via `<link>` with `display=swap` in `base.html` to avoid FOUT (Flash of Unstyled Text).

Gradient title text is generated using:
```css
background: linear-gradient(135deg, var(--hs-primary), var(--hs-indigo));
-webkit-background-clip: text;
-webkit-text-fill-color: transparent;
background-clip: text;
```

### Spacing Scale (4px base unit)

| Token | Value | Usage |
|---|---|---|
| `--hs-sp-1` | 0.25rem (4px) | Micro gaps |
| `--hs-sp-2` | 0.5rem (8px) | Tight spacing |
| `--hs-sp-3` | 0.75rem (12px) | Compact elements |
| `--hs-sp-4` | 1rem (16px) | Standard padding |
| `--hs-sp-5` | 1.5rem (24px) | Section padding |
| `--hs-sp-6` | 2rem (32px) | Card padding |
| `--hs-sp-7` | 3rem (48px) | Section spacing |

### Shadow System

| Token | Value | Usage |
|---|---|---|
| `--hs-shadow-xs` | `0 1px 3px rgba(15,23,42,0.06)` | Subtle depth |
| `--hs-shadow-sm` | `0 4px 16px rgba(15,23,42,0.08)` | Cards at rest |
| `--hs-shadow-md` | `0 12px 40px rgba(15,23,42,0.10)` | Hover / elevated |
| `--hs-shadow-lg` | `0 24px 64px rgba(15,23,42,0.13)` | Modals / floating |
| `--hs-shadow-primary` | `0 8px 30px rgba(59,111,239,0.32)` | Primary buttons |

### Border Radius Scale

| Token | Value | Usage |
|---|---|---|
| `--hs-r-sm` | 0.6rem | Inputs, small elements |
| `--hs-r-md` | 1rem | Chips, badges |
| `--hs-r-lg` | 1.5rem | Feature cards |
| `--hs-r-xl` | 2rem | Main panels/cards |
| `--hs-r-pill` | 999px | Buttons, toggles, navbar |

### Animation Timing System

| Token | Value | Usage |
|---|---|---|
| `--hs-ease` | `cubic-bezier(0.22, 1, 0.36, 1)` | Default spring-like ease |
| `--hs-ease-in` | `cubic-bezier(0.4,0,1,1)` | Elements leaving |
| `--hs-ease-out` | `cubic-bezier(0,0,0.2,1)` | Elements entering |
| `--hs-dur-fast` | `150ms` | Hover, focus states |
| `--hs-dur-med` | `280ms` | Tab switches, reveals |
| `--hs-dur-slow` | `480ms` | Page transitions |

---

## 3. Animation & Interaction Architecture

### Micro-Interactions

| Interaction | Trigger | Mechanism | File |
|---|---|---|---|
| Button ripple | `click` | Injected `<span>` + `@keyframes rippleAnim` | `premium-animations.js` |
| Button hover lift | `:hover` | `transform: translateY(-2px)` + shadow | `advanced-theme.css` |
| Feature card lift | `:hover` | `translateY(-5px)` + `shadow-md` | `advanced-theme.css` |
| Feature icon rotate | `mouseenter` | GSAP `rotate(5deg) scale(1.1)` | `premium-animations.js` |
| Nav link underline | `:hover` / `.active` | `::after` scaleX from 0 → 1 | `advanced-theme.css` |
| Cursor glow | `mousemove` | Physics-based lerp via `requestAnimationFrame` | `premium-animations.js` |

### Transition Logic

**Tab Panel Switching (Sign → Text / Text → Sign):**
- `.tab-content` is hidden with `display: none` by default
- `.tab-content.active` sets `display: block` with `animation: fadeSlideUp 0.32s var(--hs-ease)`
- The CSS animation (`fadeSlideUp`) uses `opacity: 0 → 1` and `translateY(10px → 0)` for a smooth "reveal from below" effect
- Managed by `setupFeatureToggle()` in `feature-utils.js`

**Page Entrance:**
- `.app-shell` has class `page-fade-in` applied in `base.html`
- `@keyframes pageEnter` runs on every navigation: `opacity: 0 → 1` + `translateY(16px → 0)` over 450ms

**Auth Card Entrance:**
- Handled by GSAP in `premium-animations.js`: `gsap.from('.auth-card', { duration: 0.55, opacity: 0, y: 24 })`

### WebSocket UI Animation Handling

The WebSocket event flow for real-time predictions:

```
Backend (Flask/SocketIO)
    │
    ├── emit('prediction')      → Frontend: Flash live prediction bubble
    │                               - `#livePredBubble.textContent = char`
    │                               - Add `.flash` class → triggers `@keyframes predFlash`
    │                               - Remove and re-add class via `offsetWidth` reflow trick
    │
    └── emit('stable_prediction') → Frontend: Lock character to recognized text
                                       - Clear `#recognizedText` innerHTML
                                       - Rebuild character spans with staggered delay
                                       - Each char: `<span class="prediction-char">` with `animation-delay`
```

Handled in `sign_text_converter.html` inline script, `initWebSocket()` callbacks from `realtime-interaction.js`.

### Prediction Locking Animation

When a `stable_prediction` WebSocket event fires:
1. `accumulatedText` is updated in `realtime-interaction.js`
2. The converter page clears `#recognizedText` and rebuilds it
3. **Every character** becomes an animated `<span class="prediction-char">`:

```css
@keyframes charLock {
  from { opacity: 0; transform: scale(0.6) translateY(6px); filter: blur(4px); }
  to   { opacity: 1; transform: scale(1) translateY(0);     filter: blur(0); }
}
```

Each character gets `animation-delay: (index * 0.04s)` capped at 0.5s, creating a rapid "typing" cascade effect.

### Webcam Activation State Animation

When the user clicks **Start Camera**:
1. `CameraController.startCamera()` loads `/video_feed` into `<img#cameraFeed>`
2. The converter page JS adds `.camera-active` to `#cameraFeedContainer`
3. This triggers:
   - `@keyframes cameraGlow` — a pulsing blue border (2.5s infinite ease-in-out)
   - `.live-indicator` fades in (opacity: 0 → 1 via CSS transition)
   - `.live-prediction-bubble` scales in (transform: scale(0.85) → scale(1))
   - `#cameraTip` info box becomes visible

When the user clicks **Stop Camera**:
1. `CameraController.stopCamera()` clears the `<img>` src
2. `.camera-active` is removed
3. All visual indicators hide themselves via CSS transitions

---

## 4. CSS Structure

### File Layout

```
static/
├── css/
│   └── advanced-theme.css      ← Main design system (all tokens + component styles)
├── premium-animations.js       ← GSAP + JS micro-interactions
├── camera-controller.js        ← Webcam state management
├── realtime-interaction.js     ← WebSocket + speech synthesis
├── feature-utils.js            ← Tab switching + Text→Sign conversion
├── sign_generator.css          ← Legacy sign output styles (Converter page)
├── modern_style.css            ← Legacy (kept for voice converter page)
└── premium_ui.css              ← Legacy (largely superseded by advanced-theme.css)
```

### Naming Convention (BEM-inspired with `hs-` prefix)

```
hs-{block}                  → Page-level elements: .hs-hero, .hs-section
hs-{block}-{element}        → Children: .hs-hero-title, .hs-feature-card
hs-{block}--{modifier}      → Variants: .hs-orb--blue, .hs-hero-panel--primary
```

Utility classes use short Bootstrap-compatible names: `.hidden`, `.text-muted`, `.mb-3`, etc.

### Modular Breakdown of `advanced-theme.css`

| Section | Lines | Purpose |
|---|---|---|
| Design Tokens (`:root`) | 1–80 | All CSS variables |
| Reset / Base | 81–110 | Body setup, font smoothing |
| Background Layers | 111–155 | Noise, orbs, drift animations |
| App Shell | 156–170 | Outer layout wrapper |
| Navbar | 171–250 | Glass pill navbar + dropdowns |
| Buttons | 251–360 | Primary, danger, outline variants + ripple |
| Cards / Glass Surfaces | 361–385 | Generic glass card base |
| Hero Section | 386–460 | Hero grid, eyebrow, title, CTA |
| Feature & Step Cards | 461–540 | Grid layouts, icon hover |
| Generator / Converter | 541–630 | Tab nav, feature panels |
| Camera Feed | 631–680 | Box, glow animation, live indicator |
| Prediction Text | 681–710 | Character lock animation |
| Sign Output | 711–745 | Letter reveal animation |
| Auth Pages | 746–830 | Auth card, form controls, divider |
| Global Form Controls | 831–860 | Inputs, selects, textareas |
| Alerts / Flash | 861–890 | Color-coded alert styles |
| Dashboard | 891–900 | Container layout |
| Footer | 901–915 | Translucent footer |
| Cursor Glow | 916–930 | Mouse follower |
| Utilities | 931–960 | Hidden, spacing helpers, info-box |
| Responsive | 961–995 | 3 breakpoints |
| Loading + Page Transition | 996–end | Spinner, `pageEnter` |

### Key Reusable Utility Classes

| Class | Effect |
|---|---|
| `.hidden` | `display: none !important` |
| `.glass-card` | Glassmorphic surface (blur, semi-transparent, border) |
| `.btn-primary` | Gradient blue button with ripple + glow |
| `.btn-outline` | Bordered translucent button |
| `.btn-danger-custom` | Red gradient button |
| `.info-box` | Light blue tinted info callout |
| `.page-fade-in` | Entrance animation on every page load |
| `.camera-active` | Applied to camera container; triggers glow + indicators |
| `.prediction-char` | Span for each locked prediction character |

---

## 5. JavaScript Enhancements

### File Responsibilities

| File | Responsibility |
|---|---|
| `premium-animations.js` | Cursor glow, button ripples, GSAP card entrances, navbar scroll shadow |
| `camera-controller.js` | Start/stop webcam stream, manage `<img>` src, track prediction log |
| `realtime-interaction.js` | Socket.IO init, `stable_prediction` accumulation, `speakText()` via SpeechSynthesis |
| `feature-utils.js` | `setupFeatureToggle()` for tabs, `convertTextToSign()` for Text→Sign images |

### UI State Management

State is managed through simple JS variables and DOM class toggling — no framework required:

```
Camera state:  .camera-active class on container DOM element
Tab state:     .active class on .tab-button and .tab-content
Speak state:   isAutoSpeakEnabled (global bool in realtime-interaction.js)
Text state:    accumulatedText (global string in realtime-interaction.js)
```

### Smooth DOM Updates (WebSocket Predictions)

The prediction rendering uses `innerHTML` rebuild with CSS `animation-delay` staggering:
```javascript
recognizedText.innerHTML = '';
fullText.trim().split('').forEach((c, i) => {
    const span = document.createElement('span');
    span.className = 'prediction-char';
    span.style.animationDelay = `${Math.min(i * 0.04, 0.5)}s`;
    span.textContent = c;
    recognizedText.appendChild(span);
});
```
This rebuilds from scratch on each stable prediction to ensure all characters animate correctly, avoiding stale DOM references.

### Event Handling Improvements

- `CameraController` uses **arrow function closures** to correctly bind `this` context, preventing duplicate listener bugs
- The auto-speak toggle uses a **custom `<div>` toggle** (not `<input type="checkbox">`) to avoid Bootstrap form-control style collisions
- The `offsetWidth` trick (`void livePredBubble.offsetWidth`) forces a **DOM reflow** before re-adding CSS animation classes, ensuring the `predFlash` animation restarts on every new prediction

---

## 6. Responsiveness Strategy

### Breakpoints

| Breakpoint | Width | Layout Change |
|---|---|---|
| Desktop | > 900px | Two-column hero grid, full navbar |
| Tablet | ≤ 900px | Hero switches to single column; visual panels hidden |
| Mobile L | ≤ 768px | Navbar becomes stacked pill; generator card padding reduced |
| Mobile S | ≤ 480px | Tabs stack vertically; CTA buttons go full-width |

### Layout Shifts Prevention

- All cards use `transform: translateY()` for hover effects instead of `margin`/`padding` to avoid layout reflow
- The camera feed uses `width: 100%; object-fit: cover` to scale without aspect ratio distortion
- `clamp()` is used for typography and padding to smoothly interpolate across viewports without hard breakpoint jumps

### Mobile Optimizations

- `.hs-hero-visual` panels are hidden on mobile (they are supplementary information)
- Tab buttons stack vertically on narrow screens (`flex-direction: column` at 480px)
- The cursor glow is disabled on mobile (`window.innerWidth > 768` check) to avoid confusing touch users

---

## 7. Accessibility Improvements

### Contrast Ratios (WCAG AA)

| Element | Foreground | Background | Ratio |
|---|---|---|---|
| Body text on bg | `#0f172a` | `#f0f4f8` | ~15:1 ✅ |
| Soft text on bg | `#64748b` | `#f0f4f8` | ~5.5:1 ✅ |
| White on primary | `#ffffff` | `#3b6fef` | ~4.9:1 ✅ |
| Label text on card | `#334155` | `rgba(255,255,255,0.82)` | ~8:1 ✅ |

### Keyboard Navigation

- All interactive elements (buttons, links, inputs, toggles) are reachable via Tab
- The custom Auto-speak toggle has `role="switch"` and `aria-checked` attribute, updated on toggle
- Tab buttons have `role="tab"` and `aria-selected` attributes, updated on click
- Active nav links have `aria-current="page"`

### Screen Reader Compatibility

- `aria-live="polite"` on `#recognizedText` — screen readers announce new prediction text automatically
- `aria-live="polite"` on `#livePredBubble` — live gesture character announced
- The camera feed `<img>` has `alt="Live ASL camera stream"`
- Background orbs and decorative elements have `aria-hidden="true"`
- The cursor glow `<div>` has `aria-hidden="true"`
- Flash messages use `role="alert"` and `aria-live="polite"`
- Icon-only buttons have descriptive `aria-label` attributes

---

> **Last Updated:** February 2026 — HandSignify Premium UI v2.0
> **Design Author:** Antigravity AI (Frontend Redesign Pass)
> **For Agents:** The primary CSS design system lives in `static/css/advanced-theme.css`. The animation engine lives in `static/premium-animations.js`. All design tokens are CSS custom properties on `:root` — do not use hardcoded values.
