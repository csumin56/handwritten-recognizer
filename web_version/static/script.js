// Created: 2026-01-29 18:30

const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
const resultDiv = document.getElementById('result');
const predictBtn = document.getElementById('predictBtn');
const clearBtn = document.getElementById('clearBtn');

const BRUSH_COLOR = '#e94560';
const CELL_SIZE = 14;
let isDrawing = false;
let hasDrawn = false;

// Initialize canvas
ctx.fillStyle = '#0f0f1a';
ctx.fillRect(0, 0, canvas.width, canvas.height);

function getPosition(e) {
    const rect = canvas.getBoundingClientRect();
    const scaleX = canvas.width / rect.width;
    const scaleY = canvas.height / rect.height;

    if (e.touches) {
        return {
            x: (e.touches[0].clientX - rect.left) * scaleX,
            y: (e.touches[0].clientY - rect.top) * scaleY
        };
    }
    return {
        x: (e.clientX - rect.left) * scaleX,
        y: (e.clientY - rect.top) * scaleY
    };
}

function drawBrush(x, y) {
    const col = Math.floor(x / CELL_SIZE);
    const row = Math.floor(y / CELL_SIZE);

    ctx.fillStyle = BRUSH_COLOR;

    // 3x3 brush
    for (let dr = -1; dr <= 1; dr++) {
        for (let dc = -1; dc <= 1; dc++) {
            const rr = row + dr;
            const cc = col + dc;
            if (rr >= 0 && rr < 28 && cc >= 0 && cc < 28) {
                ctx.fillRect(cc * CELL_SIZE, rr * CELL_SIZE, CELL_SIZE, CELL_SIZE);
            }
        }
    }
    hasDrawn = true;
}

function startDrawing(e) {
    e.preventDefault();
    isDrawing = true;
    const pos = getPosition(e);
    drawBrush(pos.x, pos.y);
}

function draw(e) {
    e.preventDefault();
    if (!isDrawing) return;
    const pos = getPosition(e);
    drawBrush(pos.x, pos.y);
}

function stopDrawing() {
    isDrawing = false;
}

// Mouse events
canvas.addEventListener('mousedown', startDrawing);
canvas.addEventListener('mousemove', draw);
canvas.addEventListener('mouseup', stopDrawing);
canvas.addEventListener('mouseleave', stopDrawing);

// Touch events
canvas.addEventListener('touchstart', startDrawing);
canvas.addEventListener('touchmove', draw);
canvas.addEventListener('touchend', stopDrawing);

// Predict button
predictBtn.addEventListener('click', async () => {
    if (!hasDrawn) {
        resultDiv.textContent = 'Please draw a digit first';
        resultDiv.classList.remove('success');
        return;
    }

    const imageData = canvas.toDataURL('image/png');

    try {
        const response = await fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ image: imageData })
        });

        const data = await response.json();

        if (data.error) {
            resultDiv.textContent = 'Error: ' + data.error;
            resultDiv.classList.remove('success');
        } else {
            resultDiv.textContent = `Prediction: ${data.prediction}  |  Confidence: ${data.confidence}%`;
            resultDiv.classList.add('success');
        }
    } catch (err) {
        resultDiv.textContent = 'Error connecting to server';
        resultDiv.classList.remove('success');
    }
});

// Clear button
clearBtn.addEventListener('click', () => {
    ctx.fillStyle = '#0f0f1a';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    resultDiv.textContent = 'Draw a digit and press Predict';
    resultDiv.classList.remove('success');
    hasDrawn = false;
});
