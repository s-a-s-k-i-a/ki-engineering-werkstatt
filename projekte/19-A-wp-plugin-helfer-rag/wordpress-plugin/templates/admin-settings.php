<?php
/**
 * Settings-Template für Einstellungen → KI-Plugin-Helfer.
 *
 * @package KiEngineeringWerkstatt\WpPluginHelferRag
 */

if (!defined('ABSPATH')) {
    exit;
}

$settings = (array) get_option('wphr_settings', []);
?>

<div class="wrap">
    <h1><?php esc_html_e('KI-Plugin-Helfer · Einstellungen', 'wp-plugin-helfer-rag'); ?></h1>

    <p>
        <?php esc_html_e(
            'Konfiguriere die URL deines Python-Sidecars (FastAPI). Standard: http://localhost:8765 für lokales Docker-Compose-Setup.',
            'wp-plugin-helfer-rag'
        ); ?>
    </p>

    <form method="post" action="options.php">
        <?php settings_fields('wphr_settings_group'); ?>

        <table class="form-table" role="presentation">
            <tr>
                <th scope="row">
                    <label for="wphr-sidecar-url"><?php esc_html_e('Sidecar-URL', 'wp-plugin-helfer-rag'); ?></label>
                </th>
                <td>
                    <input
                        id="wphr-sidecar-url"
                        type="url"
                        class="regular-text"
                        name="wphr_settings[sidecar_url]"
                        value="<?php echo esc_attr($settings['sidecar_url'] ?? 'http://localhost:8765'); ?>"
                        required
                    />
                    <p class="description">
                        <?php esc_html_e('Adresse, unter der dein Python-Sidecar läuft (z.B. localhost im Compose, oder eigener EU-Server).', 'wp-plugin-helfer-rag'); ?>
                    </p>
                </td>
            </tr>

            <tr>
                <th scope="row">
                    <label for="wphr-api-key"><?php esc_html_e('Sidecar API-Key (optional)', 'wp-plugin-helfer-rag'); ?></label>
                </th>
                <td>
                    <input
                        id="wphr-api-key"
                        type="password"
                        class="regular-text"
                        name="wphr_settings[sidecar_api_key]"
                        value="<?php echo esc_attr($settings['sidecar_api_key'] ?? ''); ?>"
                        autocomplete="new-password"
                    />
                    <p class="description">
                        <?php esc_html_e('Falls Sidecar mit Bearer-Token geschützt ist. Wird via Authorization-Header gesendet.', 'wp-plugin-helfer-rag'); ?>
                    </p>
                </td>
            </tr>

            <tr>
                <th scope="row">
                    <label for="wphr-max-tokens"><?php esc_html_e('Max. Query-Tokens', 'wp-plugin-helfer-rag'); ?></label>
                </th>
                <td>
                    <input
                        id="wphr-max-tokens"
                        type="number"
                        min="100"
                        max="8000"
                        step="100"
                        name="wphr_settings[max_query_tokens]"
                        value="<?php echo esc_attr((string) ($settings['max_query_tokens'] ?? 2000)); ?>"
                    />
                </td>
            </tr>

            <tr>
                <th scope="row">
                    <label for="wphr-log"><?php esc_html_e('Query-Hashes loggen', 'wp-plugin-helfer-rag'); ?></label>
                </th>
                <td>
                    <input
                        id="wphr-log"
                        type="checkbox"
                        name="wphr_settings[log_queries]"
                        value="1"
                        <?php checked(!empty($settings['log_queries'])); ?>
                    />
                    <span class="description">
                        <?php esc_html_e('Loggt nur SHA-Hashes der Fragen für Audit-Zwecke (kein Klartext, DSGVO-konform). Action-Hook: wphr_query_logged.', 'wp-plugin-helfer-rag'); ?>
                    </span>
                </td>
            </tr>
        </table>

        <?php submit_button(); ?>
    </form>
</div>
