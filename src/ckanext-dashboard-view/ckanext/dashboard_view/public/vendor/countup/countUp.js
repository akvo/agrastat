function countUp(elementId, end, start = 0, duration = 2000) {
  let current = start;
  const range = end - start;
  const increment = range / (duration / 16); // Assuming ~60 FPS
  const element = document.getElementById(elementId);

  if (!element) {
    console.error(`Element with ID '${elementId}' not found.`);
    return;
  }

  function updateCount() {
    current += increment;
    if (
      (increment > 0 && current >= end) ||
      (increment < 0 && current <= end)
    ) {
      element.innerText = end;
    } else {
      element.innerText = Math.floor(current);
      requestAnimationFrame(updateCount);
    }
  }

  updateCount();
}
