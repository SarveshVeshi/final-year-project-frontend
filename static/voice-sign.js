// voice-sign.js - Speech Recognition for ASL Translator
// Uses Web Speech API to convert voice to text, then displays ASL signs

(function () {
    'use strict';

    // Speech Recognition Setup
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    let recognition = null;
    let isListening = false;

    // DOM Elements
    let microphoneButton, startBtn, stopBtn, listeningIndicator,
        transcriptSection, transcriptDisplay, browserWarning,
        voiceErrorMessage, voiceSignOutput;

    // Initialize when DOM is ready
    document.addEventListener('DOMContentLoaded', function () {
        initializeElements();
        setupTabSwitching();
        checkBrowserCompatibility();

        if (SpeechRecognition) {
            initVoiceRecognition();
        }
    });

    function initializeElements() {
        // Get all DOM elements
        microphoneButton = document.getElementById('microphoneButton');
        startBtn = document.getElementById('startListeningBtn');
        stopBtn = document.getElementById('stopListeningBtn');
        listeningIndicator = document.getElementById('listeningIndicator');
        transcriptSection = document.getElementById('transcriptSection');
        transcriptDisplay = document.getElementById('transcriptDisplay');
        browserWarning = document.getElementById('browserWarning');
        voiceErrorMessage = document.getElementById('voiceErrorMessage');
        voiceSignOutput = document.getElementById('voiceSignOutput');
    }

    function setupTabSwitching() {
        const tabButtons = document.querySelectorAll('.tab-button');

        tabButtons.forEach(button => {
            button.addEventListener('click', function () {
                const targetTab = this.getAttribute('data-tab');
                switchTab(targetTab);

                // Update active state on buttons
                tabButtons.forEach(btn => btn.classList.remove('active'));
                this.classList.add('active');
            });
        });
    }

    function switchTab(targetTabId) {
        // Hide all tabs
        const allTabs = document.querySelectorAll('.tab-content');
        allTabs.forEach(tab => tab.classList.remove('active'));

        // Show target tab
        const targetTab = document.getElementById(targetTabId);
        if (targetTab) {
            targetTab.classList.add('active');
        }

        // Stop listening if switching away from voice tab
        if (targetTabId !== 'voiceSignTab' && isListening) {
            stopListening();
        }
    }

    function checkBrowserCompatibility() {
        if (!SpeechRecognition) {
            browserWarning.classList.remove('hidden');
            startBtn.disabled = true;
            startBtn.style.opacity = '0.5';
            startBtn.style.cursor = 'not-allowed';
        }
    }

    function initVoiceRecognition() {
        recognition = new SpeechRecognition();

        // Configuration
        recognition.lang = 'en-US';
        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.maxAlternatives = 1;

        // Event Handlers
        recognition.onstart = function () {
            isListening = true;
            microphoneButton.classList.add('mic-active');
            listeningIndicator.classList.remove('hidden');
            startBtn.classList.add('hidden');
            stopBtn.classList.remove('hidden');
            voiceErrorMessage.classList.add('hidden');
        };

        recognition.onresult = function (event) {
            const transcript = event.results[0][0].transcript;
            handleTranscript(transcript);
        };

        recognition.onerror = function (event) {
            handleError(event.error);
        };

        recognition.onend = function () {
            stopListening();
        };

        // Button event listeners
        startBtn.addEventListener('click', startListening);
        stopBtn.addEventListener('click', stopListening);
    }

    function startListening() {
        if (!recognition) {
            showError('Speech recognition is not available.');
            return;
        }

        try {
            // Clear previous results
            voiceSignOutput.innerHTML = '';
            voiceSignOutput.classList.add('hidden');
            transcriptSection.classList.add('hidden');
            voiceErrorMessage.classList.add('hidden');

            recognition.start();
        } catch (error) {
            showError('Could not start speech recognition. Please try again.');
        }
    }

    function stopListening() {
        if (recognition && isListening) {
            recognition.stop();
        }

        // Reset UI
        isListening = false;
        microphoneButton.classList.remove('mic-active');
        listeningIndicator.classList.add('hidden');
        startBtn.classList.remove('hidden');
        stopBtn.classList.add('hidden');
    }

    function handleTranscript(transcript) {
        // Clean the transcript: uppercase and keep only A-Z, 0-9, and spaces
        const cleanedText = transcript.toUpperCase().replace(/[^A-Z0-9 ]/g, '');

        // Display transcript
        transcriptDisplay.textContent = cleanedText;
        transcriptSection.classList.remove('hidden');

        // Check if there's any valid content
        if (!cleanedText.trim() || !/[A-Z0-9]/.test(cleanedText)) {
            showError('No valid text recognized. Please speak clearly and try again.');
            return;
        }

        // Convert text to sign images - use the same logic as convertTextToSign but target voiceSignOutput
        const words = cleanedText.split(' ');
        voiceSignOutput.innerHTML = ''; // Clear previous output

        // Process each word
        words.forEach((word, wordIndex) => {
            if (!word.trim()) return;

            const wordContainer = document.createElement('div');
            wordContainer.className = 'word-container';

            for (let i = 0; i < word.length; i++) {
                const char = word[i];

                if (/[A-Z0-9]/.test(char)) {
                    const img = document.createElement('img');
                    img.className = 'letter-image';
                    img.src = `/static/asl-images/${char}.png`;
                    img.alt = `ASL sign for ${char}`;
                    img.title = char;

                    const calculatedDelay = (wordIndex * 0.1) + (i * 0.05);
                    img.style.animationDelay = `${Math.min(calculatedDelay, 1.5)}s`;

                    img.onerror = function () {
                        const placeholder = document.createElement('div');
                        placeholder.className = 'letter-image missing';
                        placeholder.textContent = char;
                        placeholder.title = char;
                        placeholder.style.animationDelay = this.style.animationDelay;
                        this.parentNode.replaceChild(placeholder, this);
                    };

                    wordContainer.appendChild(img);
                }
            }

            if (wordContainer.children.length > 0) {
                voiceSignOutput.appendChild(wordContainer);
            }
        });

        // Show output container if there's content
        if (voiceSignOutput.children.length > 0) {
            voiceSignOutput.classList.remove('hidden');
            voiceSignOutput.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
    }

    function handleError(error) {
        let errorMessage = 'An error occurred with speech recognition.';

        switch (error) {
            case 'no-speech':
                errorMessage = 'No speech was detected. Please try again.';
                break;
            case 'audio-capture':
                errorMessage = 'No microphone was found. Please check your device.';
                break;
            case 'not-allowed':
                errorMessage = 'Microphone permission denied. Please allow microphone access.';
                break;
            case 'network':
                errorMessage = 'Network error occurred. Please check your connection.';
                break;
            case 'aborted':
                // User stopped - not an error
                return;
        }

        showError(errorMessage);
        stopListening();
    }

    function showError(message) {
        voiceErrorMessage.textContent = message;
        voiceErrorMessage.classList.remove('hidden');

        // Auto-hide after 5 seconds
        setTimeout(function () {
            voiceErrorMessage.classList.add('hidden');
        }, 5000);
    }

})();
