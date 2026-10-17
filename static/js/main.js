// Show spinner on either prediction form.
const predictionForm = document.getElementById('predictForm') || document.getElementById('priceForm');
if (predictionForm) {
predictionForm.addEventListener('submit', function () {
  const btn = document.getElementById('submitBtn');
  const spinner = document.getElementById('btnSpinner');
  const label = btn?.querySelector('span');
  if (label) label.textContent = 'Predicting...';
  if (spinner) spinner.style.display = 'inline-block';
  if (btn) btn.disabled = true;
});
}

// Scroll to result if present
function filterSelectOptions(selectElement, allowedValues) {
  if (!selectElement) return;

  const currentValue = selectElement.value;
  Array.from(selectElement.options).forEach((option) => {
    if (!option.value || option.value === '') {
      option.hidden = false;
      option.disabled = false;
      return;
    }

    const isAllowed = !allowedValues || allowedValues.includes(option.value);
    option.hidden = !isAllowed;
    option.disabled = !isAllowed;
  });

  const isCurrentValueValid = !currentValue || !allowedValues || allowedValues.includes(currentValue);
  if (!isCurrentValueValid) {
    selectElement.value = '';
  }
}

function applyBrandSpecificOptions() {
  const brandSelect = document.getElementById('brand');
  if (!brandSelect) return;

  const featureDataElement = document.getElementById('brand-feature-data');
  if (!featureDataElement) return;

  try {
    const featureData = JSON.parse(featureDataElement.textContent || '{}');
    const selectedBrand = brandSelect.value;
    const brandRules = featureData[selectedBrand] || null;

    const cpuSelect = document.getElementById('cpu');
    const osSelect = document.getElementById('os');
    const graphicsSelect = document.getElementById('graphics');

    filterSelectOptions(cpuSelect, brandRules ? brandRules.cpu : null);
    filterSelectOptions(osSelect, brandRules ? brandRules.os : null);
    filterSelectOptions(graphicsSelect, brandRules ? brandRules.graphics : null);
  } catch (error) {
    console.warn('Brand feature metadata invalid:', error);
  }
}

if (document.getElementById('brand')) {
  document.getElementById('brand').addEventListener('change', applyBrandSpecificOptions);
}

window.addEventListener('DOMContentLoaded', function () {
  applyBrandSpecificOptions();
});

const result = document.querySelector('.result-card');
if (result) {
  result.scrollIntoView({ behavior: 'smooth', block: 'start' });
}
