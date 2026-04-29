<?php
/**
 * Admin-UI-Template für Werkzeuge → KI-Plugin-Helfer.
 *
 * @package KiEngineeringWerkstatt\WpPluginHelferRag
 */

if (!defined('ABSPATH')) {
    exit;
}

$settings = (array) get_option('wphr_settings', []);
$sidecar_url = $settings['sidecar_url'] ?? '';
?>

<div class="wrap wphr-helfer">
    <h1><?php esc_html_e('KI-Plugin-Helfer RAG', 'wp-plugin-helfer-rag'); ?></h1>

    <?php if (empty($sidecar_url)): ?>
        <div class="notice notice-warning">
            <p>
                <?php
                printf(
                    /* translators: %s: link to settings page */
                    esc_html__('Bitte zunächst die %s konfigurieren.', 'wp-plugin-helfer-rag'),
                    '<a href="' . esc_url(admin_url('options-general.php?page=wphr-settings')) . '">' .
                        esc_html__('Sidecar-URL', 'wp-plugin-helfer-rag') .
                    '</a>'
                );
                ?>
            </p>
        </div>
    <?php endif; ?>

    <p class="description">
        <?php esc_html_e(
            'Stelle eine Frage zu deiner Plugin-Doku oder lass den Helfer Code-Stellen suchen. Kommunikation läuft via WP-REST-API zum Python-Sidecar.',
            'wp-plugin-helfer-rag'
        ); ?>
    </p>

    <form id="wphr-frage-form" class="wphr-form">
        <label for="wphr-kontext"><?php esc_html_e('Kontext', 'wp-plugin-helfer-rag'); ?></label>
        <select id="wphr-kontext" name="kontext">
            <option value="doku"><?php esc_html_e('Plugin-Doku-RAG', 'wp-plugin-helfer-rag'); ?></option>
            <option value="code"><?php esc_html_e('Code-Search', 'wp-plugin-helfer-rag'); ?></option>
            <option value="issue"><?php esc_html_e('Issue-Triage', 'wp-plugin-helfer-rag'); ?></option>
        </select>

        <label for="wphr-frage"><?php esc_html_e('Frage', 'wp-plugin-helfer-rag'); ?></label>
        <textarea id="wphr-frage" name="frage" rows="3" required></textarea>

        <button type="submit" class="button button-primary">
            <?php esc_html_e('Frage senden', 'wp-plugin-helfer-rag'); ?>
        </button>
    </form>

    <div id="wphr-ergebnis" class="wphr-ergebnis" aria-live="polite"></div>

    <p class="wphr-disclaimer">
        <?php esc_html_e(
            '⚠️ Kein Rechtsrat. Antworten sind RAG-generiert und sollten manuell verifiziert werden. Logs und Caching laut Einstellungen.',
            'wp-plugin-helfer-rag'
        ); ?>
    </p>
</div>
