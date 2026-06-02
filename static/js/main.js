// Show spinner on form submit
document.getElementById('predictForm').addEventListener('submit', function () {
  const btn = document.getElementById('submitBtn');
  const loader = document.getElementById('btnLoader');
  btn.querySelector('span').textContent = 'Predicting...';
  loader.style.display = 'inline-block';
  btn.disabled = true;
});

// Scroll to result if present
const result = document.querySelector('.result-card');
if (result) {
  result.scrollIntoView({ behavior: 'smooth', block: 'start' });
}
