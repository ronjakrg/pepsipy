document.addEventListener('DOMContentLoaded', () => {
  // For (un-)selecting checkboxes in forms
  document.querySelectorAll('.js-toggle-checkboxes').forEach(btn =>
    btn.addEventListener('click', () => {
      const checked = btn.dataset.checked === 'true';
      btn.closest('form')
        .querySelectorAll('input[type="checkbox"]')
        .forEach(cb => cb.checked = checked);
    })
  );
  // For updating color picker labels
  const colorInputs = document.querySelectorAll('.custom-color-input');
  colorInputs.forEach(input => {
    input.addEventListener('input', (event) => {
            const newColor = event.target.value;
            const labelElement = event.target.parentElement;
            labelElement.style.backgroundColor = newColor;
        });
  });
});