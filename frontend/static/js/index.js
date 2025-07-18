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
});