document.addEventListener('DOMContentLoaded', function() {
    // Récupérer les couleurs actives du localStorage
    const activeThemeColor = localStorage.getItem('activeThemeColor');
    const activeTextColor = localStorage.getItem('activeTextColor');
    
    // Fonction pour appliquer les couleurs de fond
    function applyBackgroundColor(color) {
        document.documentElement.style.backgroundColor = color;
        document.body.style.backgroundColor = color;
        document.querySelector('#container').style.backgroundColor = color;
        document.querySelector('#header').style.backgroundColor = color;
        document.querySelector('#content').style.backgroundColor = color;
    }

    // Fonction pour appliquer la couleur du texte
    function applyTextColor(color) {
        document.documentElement.style.color = color;
        document.body.style.color = color;
        document.querySelectorAll('a, p, span, h1, h2, h3, h4, h5, h6, label, td, th').forEach(element => {
            element.style.color = color;
        });
    }
    
    // Appliquer les couleurs si elles existent
    if (activeThemeColor) {
        applyBackgroundColor(activeThemeColor);
    }
    if (activeTextColor) {
        applyTextColor(activeTextColor);
    }

    const form = document.querySelector('form');
    const themeId = form?.dataset?.themeId;
    const isActiveCheckbox = document.querySelector('input[name="is_active"]');
    
    // Fonction pour mettre à jour les couleurs
    function updateColors(bgColor, textColor, themeId) {
        if (isActiveCheckbox && isActiveCheckbox.checked) {
            applyBackgroundColor(bgColor);
            applyTextColor(textColor);
            localStorage.setItem('activeThemeColor', bgColor);
            localStorage.setItem('activeTextColor', textColor);
        }
    }

    // Appliquer les couleurs si le thème est actif
    if (isActiveCheckbox) {
        isActiveCheckbox.addEventListener('change', function() {
            const primaryColorPicker = document.querySelector('input[name="primary_color"]');
            const secondaryColorPicker = document.querySelector('input[name="secondary_color"]');
            if (this.checked && primaryColorPicker && secondaryColorPicker) {
                updateColors(primaryColorPicker.value, secondaryColorPicker.value, themeId);
            }
        });
    }

    // Mise à jour en temps réel lors du changement de couleur primaire
    const primaryColorInput = document.querySelector('input[name="primary_color"]');
    if (primaryColorInput) {
        primaryColorInput.addEventListener('input', function(e) {
            if (isActiveCheckbox && isActiveCheckbox.checked) {
                applyBackgroundColor(e.target.value);
                localStorage.setItem('activeThemeColor', e.target.value);
            }
        });
    }

    // Mise à jour en temps réel lors du changement de couleur secondaire
    const secondaryColorInput = document.querySelector('input[name="secondary_color"]');
    if (secondaryColorInput) {
        secondaryColorInput.addEventListener('input', function(e) {
            if (isActiveCheckbox && isActiveCheckbox.checked) {
                applyTextColor(e.target.value);
                localStorage.setItem('activeTextColor', e.target.value);
            }
        });
    }
});