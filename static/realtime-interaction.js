/**
 * realtime-interaction.js
 * Handles WebSocket connections and Speech Synthesis for HandSignify.
 * Dependencies: Socket.IO client
 */

let socket = null;
let accumulatedText = "";
let isAutoSpeakEnabled = true;

/**
 * Initializes WebSocket connection.
 * @param {object} callbacks - { onPrediction: fn, onStablePrediction: fn, onError: fn }
 */
let pollInterval = null;

function initWebSocket(callbacks = {}) {
    console.log('🔄 Initializing Prediction Poller (Browser Bridge Mode)');
    
    if (pollInterval) {
        clearInterval(pollInterval);
    }

    let lastChar = "";
    let charCount = 0;
    const STABILITY_THRESHOLD = 5; // signs needed to consider "stable"

    pollInterval = setInterval(async () => {
        try {
            const response = await fetch('http://127.0.0.1:5001/prediction');
            const data = await response.json();
            const char = data.prediction;

            if (callbacks.onPrediction) {
                callbacks.onPrediction(char);
            }

            // Stability check for auto-accumulation
            if (char !== "None" && char !== "Hand Detected") {
                if (char === lastChar) {
                    charCount++;
                } else {
                    lastChar = char;
                    charCount = 1;
                }

                if (charCount === STABILITY_THRESHOLD) {
                    console.log('✅ Stable prediction detected:', char);
                    accumulatedText += char + " ";
                    if (callbacks.onStablePrediction) {
                        callbacks.onStablePrediction(char, accumulatedText);
                    }
                    if (isAutoSpeakEnabled && window.speechSynthesis) {
                        speakText(char);
                    }
                    charCount = 0; // Reset after accumulation
                }
            } else {
                charCount = 0;
            }

        } catch (error) {
            // console.error('Poller error:', error);
            if (callbacks.onError) callbacks.onError(error);
        }
    }, 200); // 5Hz polling
}

function disconnectWebSocket() {
    if (pollInterval) {
        clearInterval(pollInterval);
        pollInterval = null;
        console.log('Poller stopped');
    }
}

/**
 * Speaks text using browser Speech Synthesis.
 * @param {string} text - Text to speak
 * @param {object} settings - { rate: number, pitch: number, volume: number }
 */
function speakText(text, settings = {}) {
    if (!window.speechSynthesis || !text) return;

    const utterance = new SpeechSynthesisUtterance(text);

    // Get live values from UI if IDs are standard, or use passed settings
    const rateEl = document.getElementById('speechRate');
    const pitchEl = document.getElementById('speechPitch');

    utterance.rate = settings.rate || (rateEl ? parseFloat(rateEl.value) : 1.0);
    utterance.pitch = settings.pitch || (pitchEl ? parseFloat(pitchEl.value) : 1.0);
    utterance.volume = settings.volume || 1.0;

    window.speechSynthesis.speak(utterance);
}

function clearAccumulatedText() {
    accumulatedText = "";
}

function getAccumulatedText() {
    return accumulatedText;
}

// Export for module usage (if needed)
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        initWebSocket,
        disconnectWebSocket,
        speakText,
        clearAccumulatedText,
        getAccumulatedText
    };
}
