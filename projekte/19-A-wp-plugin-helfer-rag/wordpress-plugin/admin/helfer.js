/**
 * Admin-Frontend für KI-Plugin-Helfer.
 * Sendet Frage an WP-REST-Endpoint /ki-helfer/v1/frage und rendert Antwort + Quellen.
 */
(function () {
    'use strict';

    const form = document.getElementById('wphr-frage-form');
    const ergebnis = document.getElementById('wphr-ergebnis');
    if (!form || !ergebnis || typeof wphrConfig === 'undefined') {
        return;
    }

    form.addEventListener('submit', async function (event) {
        event.preventDefault();

        const frage = document.getElementById('wphr-frage').value.trim();
        const kontext = document.getElementById('wphr-kontext').value;
        if (frage.length < 3) {
            return;
        }

        ergebnis.innerHTML = '<p class="wphr-loading">' + wphrConfig.i18n.loading + '</p>';

        try {
            const response = await wp.apiFetch({
                path: 'ki-helfer/v1/frage',
                method: 'POST',
                data: { frage: frage, kontext: kontext },
            });
            renderAntwort(response);
        } catch (err) {
            const detail = (err && err.message) ? err.message : wphrConfig.i18n.error;
            ergebnis.innerHTML = '<p class="wphr-error">' + escapeHtml(detail) + '</p>';
        }
    });

    function renderAntwort(antwort) {
        if (!antwort || typeof antwort !== 'object') {
            ergebnis.innerHTML = '<p class="wphr-error">' + wphrConfig.i18n.error + '</p>';
            return;
        }

        const text = escapeHtml(antwort.antwort || '');
        const quellen = Array.isArray(antwort.quellen) ? antwort.quellen : [];
        const konfidenz = typeof antwort.konfidenz === 'number'
            ? antwort.konfidenz.toFixed(2)
            : '–';

        let quellenHtml = '';
        if (quellen.length > 0) {
            quellenHtml += '<h3>Quellen</h3><ul class="wphr-quellen">';
            for (const q of quellen) {
                const datei = escapeHtml(q.datei || '');
                const ausschnitt = escapeHtml((q.ausschnitt || '').substring(0, 300));
                const score = typeof q.score === 'number' ? q.score.toFixed(2) : '–';
                quellenHtml += `<li><strong>${datei}</strong> <em>(score ${score})</em><br><code>${ausschnitt}</code></li>`;
            }
            quellenHtml += '</ul>';
        }

        ergebnis.innerHTML = `
            <h2>Antwort <span class="wphr-konfidenz">(Konfidenz ${konfidenz})</span></h2>
            <p class="wphr-antwort">${text}</p>
            ${quellenHtml}
        `;
    }

    function escapeHtml(s) {
        return String(s)
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#39;');
    }
})();
