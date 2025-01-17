// Example: Dynamic typing effect for hero section
const text = "Ping Reducer 2.0 is here to boost your gaming performance with minimal lag.";
let index = 0;

function typeText() {
    if (index < text.length) {
        document.querySelector('.hero-text p').innerText += text[index];
        index++;
        setTimeout(typeText, 100);  // Adjust typing speed here
    }
}

window.onload = function () {
    typeText();  // Start typing on page load
};
