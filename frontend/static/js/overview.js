document.addEventListener('DOMContentLoaded', () => {
  // For submitting metadata aspects and filling them into choice field
  const features = document.getElementById("forms");
  const btn = document.getElementById("btn-metadata");
  if (!sessionStorage.getItem("first_loaded")) {
    features.classList.add("invisible");
  }

  btn.addEventListener("click", function() {
    const data = new FormData(document.querySelector("form"));
    fetch("fill_metadata_options", {
      method: "POST",
      headers: {
        "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value,
      },
      body: data,
    })
      .then((response) => response.json())
      .then((data) => {
        const fields = document.querySelectorAll(
          "select[name$='compare_features_metadata'], select[name$='compare_feature_metadata']"
        );
        fields.forEach((field) => {
          field.innerHTML = "";
          data.metadata.forEach((elem) => {
            const option = document.createElement("option");
            option.value = elem;
            option.textContent = elem;
            field.appendChild(option);
          });
        });
        sessionStorage.setItem("first_loaded", "true");
        features.classList.remove("invisible")
      });
  });

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