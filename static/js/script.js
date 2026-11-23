// fait avec ai
document.addEventListener("DOMContentLoaded", function () {
  // 1. On récupère tous les menus déroulants d'ingrédients
  const selects = document.querySelectorAll(
    "#ingredient1, #ingredient2, #ingredient3, #ingredient4",
  );

  function mettreAJourOptions() {
    // 2. On récupère toutes les valeurs actuellement sélectionnées (en ignorant les champs vides)
    const valeursChoisies = Array.from(selects)
      .map((select) => select.value)
      .filter((val) => val !== "");

    // 3. On parcourt chaque menu déroulant
    selects.forEach((select) => {
      const valeurActuelle = select.value;
      const options = select.querySelectorAll("option");

      options.forEach((option) => {
        // On ne désactive jamais l'option vide par défaut
        if (option.value === "") return;

        // Si la valeur est choisie ailleurs ET que ce n'est pas la valeur actuelle de ce menu précis
        if (
          valeursChoisies.includes(option.value) &&
          option.value !== valeurActuelle
        ) {
          option.disabled = true;
        } else {
          option.disabled = false;
        }
      });
    });
  }

  // 4. On écoute le changement sur chacun des menus
  selects.forEach((select) => {
    select.addEventListener("change", mettreAJourOptions);
  });

  // 5. On lance la fonction une première fois au chargement
  mettreAJourOptions();
});
