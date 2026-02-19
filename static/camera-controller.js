// camera-controller.js
// Modularized camera controller for ASL Translator
// Prevents duplicate event listeners and enables reuse across multiple pages

class CameraController {
    constructor(config) {
        this.startButton = document.getElementById(config.startButtonId);
        this.stopButton = document.getElementById(config.stopButtonId);
        this.feedElement = document.getElementById(config.feedElementId);
        this.container = document.getElementById(config.containerId);
        this.videoFeedUrl = config.videoFeedUrl;
        this.onPrediction = config.onPrediction || null; // Optional callback for predictions
        this.predictionLog = [];
        this.isInitialized = false;

        this.init();
    }

    init() {
        // Guard against missing elements
        if (!this.startButton || !this.stopButton || !this.feedElement || !this.container) {
            console.warn('CameraController: Required elements not found. Check element IDs.');
            return;
        }

        // Guard against double initialization
        if (this.isInitialized) {
            console.warn('CameraController: Already initialized');
            return;
        }

        // Bind event listeners (arrow functions maintain 'this' context)
        this.startButton.addEventListener('click', () => this.startCamera());
        this.stopButton.addEventListener('click', () => this.stopCamera());

        this.isInitialized = true;
        console.log('CameraController: Initialized successfully');
    }

    startCamera() {
        if (!this.feedElement || !this.container) return;

        // Show camera container
        this.container.classList.remove('hidden');
        this.container.style.display = 'flex';

        // Start video feed stream
        this.feedElement.src = this.videoFeedUrl;

        // Update button visibility
        this.stopButton.classList.remove('hidden');
        this.stopButton.style.display = 'inline-block';
        this.startButton.style.display = 'none';

        console.log('CameraController: Camera started');
    }

    stopCamera() {
        if (!this.feedElement || !this.container) return;

        // Hide camera container
        this.container.classList.add('hidden');
        this.container.style.display = 'none';

        // Stop video stream by clearing src
        this.feedElement.src = '';

        // Update button visibility
        this.stopButton.classList.add('hidden');
        this.stopButton.style.display = 'none';
        this.startButton.style.display = 'inline-block';

        console.log('CameraController: Camera stopped');
    }

    // Method to capture ML model predictions (for Sign → Voice feature)
    capturePrediction(text) {
        if (!text) return;

        // Store in prediction log (keep last 10)
        this.predictionLog.push({
            text: text,
            timestamp: new Date().toISOString()
        });

        if (this.predictionLog.length > 10) {
            this.predictionLog.shift(); // Remove oldest
        }

        // Call custom callback if provided
        if (this.onPrediction && typeof this.onPrediction === 'function') {
            this.onPrediction(text);
        }
    }

    // Get the most recent prediction
    getLatestPrediction() {
        if (this.predictionLog.length === 0) return null;
        return this.predictionLog[this.predictionLog.length - 1].text;
    }

    // Get all predictions
    getAllPredictions() {
        return this.predictionLog;
    }

    // Clear prediction log
    clearPredictions() {
        this.predictionLog = [];
    }
}

// Global initialization helper function
function initCameraController(config) {
    // Validate required config
    if (!config.startButtonId || !config.stopButtonId || !config.feedElementId || !config.containerId) {
        console.error('CameraController: Missing required configuration');
        return null;
    }

    return new CameraController(config);
}

// Export for module usage (if needed)
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { CameraController, initCameraController };
}
