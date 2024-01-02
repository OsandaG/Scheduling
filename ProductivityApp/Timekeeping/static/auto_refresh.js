let reloadTimer; // Initialize the timer variable

// Function to reload the page
function reloadPage() {
  location.reload();
}

// Function to check if any excluded input field has focus
function isInputFocused() {
  const excludedTypes = ['checkbox', 'radio', 'button']; // Add input types to exclude
  const inputFields = document.querySelectorAll('input');

  for (const inputField of inputFields) {
    if (!excludedTypes.includes(inputField.type) && inputField === document.activeElement) {
      return true;
    }
  }
  return false;
}

// Function to start the timer for reloading the page
function startReloadTimer() {
  // Check if no excluded input field has focus
  if (!isInputFocused()) {
    reloadTimer = setTimeout(reloadPage, 60000); // Reload every 1 minute (60,000 milliseconds)
  }
}

// Event listener to cancel the timer if an excluded input field gains focus
document.addEventListener('focusin', () => {
  clearTimeout(reloadTimer); // Cancel the timer when an excluded input field gains focus
});

// Event listener to restart the timer when an excluded input field loses focus
document.addEventListener('focusout', startReloadTimer);

// Initial start of the timer
startReloadTimer();
