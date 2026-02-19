// sign-voice.js
// Speech Synthesis for Sign → Voice feature
// Uses browser Web Speech API (speechSynthesis) to convert predicted sign text to speech

class SignVoiceController {
    constructor(config) {
        this.speakButton = document.getElementById(config.speakButtonId);
        this.predictionDisplay = document.getElementById(config.predictionDisplayId);
        this.voiceSelect = document.getElementById(config.voiceSelectId) || null;
        this.rateControl = document.getElementById(config.rateControlId) || null;
        this.pitchControl = document.getElementById(config.pitchControlId) || null;

        // Speech synthesis settings
        this.rate = 1.0; // Speed (0.1 to 10)
        this.pitch = 1.0; // Pitch (0 to 2)
        this.volume = 1.0; // Volume (0 to 1)
        this.voice = null;
        this.availableVoices = [];

        // Check browser support
        if (!('speechSynthesis' in window)) {
            console.error('SignVoiceController: Speech Synthesis not supported in this browser');
            this.showUnsupportedMessage();
            return;
        }

        this.init();
    }

    init() {
        // Load available voices
        this.loadVoices();

        // Setup event listeners for voice selection changes
        if (window.speechSynthesis.onvoiceschanged !== undefined) {
            window.speechSynthesis.onvoiceschanged = () => this.loadVoices();
        }

        // Bind speak button
        if (this.speakButton) {
            this.speakButton.addEventListener('click', () => this.speak());
        }

        // Bind voice controls if they exist
        if (this.voiceSelect) {
            this.voiceSelect.addEventListener('change', (e) => {
                this.voice = this.availableVoices[e.target.value];
            });
        }

        if (this.rateControl) {
            this.rateControl.addEventListener('change', (e) => {
                this.rate = parseFloat(e.target.value);
            });
        }

        if (this.pitchControl) {
            this.pitchControl.addEventListener('change', (e) => {
                this.pitch = parseFloat(e.target.value);
            });
        }

        console.log('SignVoiceController: Initialized successfully');
    }

    loadVoices() {
        this.availableVoices = window.speechSynthesis.getVoices();

        // Filter to English voices
        const englishVoices = this.availableVoices.filter(voice => voice.lang.startsWith('en'));

        // Set default voice (prefer US English)
        const defaultVoice = englishVoices.find(voice => voice.lang === 'en-US') || englishVoices[0];
        this.voice = defaultVoice;

        // Populate voice select dropdown if it exists
        if (this.voiceSelect && englishVoices.length > 0) {
            this.voiceSelect.innerHTML = '';
            englishVoices.forEach((voice, index) => {
                const option = document.createElement('option');
                option.value = this.availableVoices.indexOf(voice);
                option.textContent = `${voice.name} (${voice.lang})`;
                if (voice === defaultVoice) {
                    option.selected = true;
                }
                this.voiceSelect.appendChild(option);
            });
        }
    }

    speak(text = null) {
        // Cancel any ongoing speech
        window.speechSynthesis.cancel();

        // Get text from parameter or prediction display
        let textToSpeak = text;
        if (!textToSpeak && this.predictionDisplay) {
            textToSpeak = this.predictionDisplay.textContent.trim();
        }

        if (!textToSpeak) {
            console.warn('SignVoiceController: No text to speak');
            return;
        }

        // Create speech utterance
        const utterance = new SpeechSynthesisUtterance(textToSpeak);
        utterance.voice = this.voice;
        utterance.rate = this.rate;
        utterance.pitch = this.pitch;
        utterance.volume = this.volume;
        utterance.lang = 'en-US';

        // Event handlers
        utterance.onstart = () => {
            console.log('SignVoiceController: Started speaking:', textToSpeak);
            if (this.speakButton) {
                this.speakButton.textContent = 'Speaking...';
                this.speakButton.disabled = true;
            }
        };

        utterance.onend = () => {
            console.log('SignVoiceController: Finished speaking');
            if (this.speakButton) {
                this.speakButton.textContent = 'Speak';
                this.speakButton.disabled = false;
            }
        };

        utterance.onerror = (event) => {
            console.error('SignVoiceController: Speech error:', event.error);
            if (this.speakButton) {
                this.speakButton.textContent = 'Speak';
                this.speakButton.disabled = false;
            }
        };

        // Speak the text
        window.speechSynthesis.speak(utterance);
    }

    stop() {
        window.speechSynthesis.cancel();
        if (this.speakButton) {
            this.speakButton.textContent = 'Speak';
            this.speakButton.disabled = false;
        }
    }

    updatePredictionDisplay(text) {
        if (this.predictionDisplay) {
            this.predictionDisplay.textContent = text;
        }
    }

    showUnsupportedMessage() {
        if (this.speakButton) {
            this.speakButton.disabled = true;
            this.speakButton.textContent = 'Not Supported';
            this.speakButton.title = 'Speech synthesis not supported in this browser';
        }
    }

    // Utility to speak immediately (for simple use cases)
    static speakNow(text, options = {}) {
        if (!('speechSynthesis' in window)) {
            console.warn('Speech synthesis not supported');
            return;
        }

        const utterance = new SpeechSynthesisUtterance(text);
        utterance.rate = options.rate || 1.0;
        utterance.pitch = options.pitch || 1.0;
        utterance.volume = options.volume || 1.0;
        utterance.lang = options.lang || 'en-US';

        window.speechSynthesis.speak(utterance);
    }
}

// Global initialization helper
function initSignVoiceController(config) {
    if (!config.speakButtonId) {
        console.error('SignVoiceController: Missing required speakButtonId');
        return null;
    }

    return new SignVoiceController(config);
}

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { SignVoiceController, initSignVoiceController };
}
