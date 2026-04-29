<?php
/**
 * Admin-UI — registriert die Werkzeuge-Submenu-Seite + Settings.
 *
 * @package KiEngineeringWerkstatt\WpPluginHelferRag
 */

declare(strict_types=1);

if (!defined('ABSPATH')) {
    exit;
}

final class Wphr_Admin
{
    public function register(): void
    {
        add_action('admin_menu', [$this, 'add_menu']);
        add_action('admin_init', [$this, 'register_settings']);
        add_action('admin_enqueue_scripts', [$this, 'enqueue_assets']);
    }

    public function add_menu(): void
    {
        add_management_page(
            __('KI-Plugin-Helfer', 'wp-plugin-helfer-rag'),
            __('KI-Plugin-Helfer', 'wp-plugin-helfer-rag'),
            'manage_options',
            'wphr-helfer',
            [$this, 'render_page']
        );

        add_options_page(
            __('KI-Plugin-Helfer Einstellungen', 'wp-plugin-helfer-rag'),
            __('KI-Plugin-Helfer', 'wp-plugin-helfer-rag'),
            'manage_options',
            'wphr-settings',
            [$this, 'render_settings']
        );
    }

    public function register_settings(): void
    {
        register_setting(
            'wphr_settings_group',
            'wphr_settings',
            [
                'type'              => 'array',
                'sanitize_callback' => [$this, 'sanitize_settings'],
                'default'           => [],
            ]
        );
    }

    public function sanitize_settings(array $input): array
    {
        return [
            'sidecar_url'      => esc_url_raw($input['sidecar_url'] ?? 'http://localhost:8765'),
            'sidecar_api_key'  => sanitize_text_field($input['sidecar_api_key'] ?? ''),
            'max_query_tokens' => max(100, min(8000, absint($input['max_query_tokens'] ?? 2000))),
            'log_queries'      => !empty($input['log_queries']),
        ];
    }

    public function enqueue_assets(string $hook): void
    {
        if ($hook !== 'tools_page_wphr-helfer') {
            return;
        }
        wp_enqueue_script(
            'wphr-helfer',
            WPHR_PLUGIN_URL . 'admin/helfer.js',
            ['wp-api-fetch'],
            WPHR_VERSION,
            true
        );
        wp_localize_script('wphr-helfer', 'wphrConfig', [
            'restNonce' => wp_create_nonce('wp_rest'),
            'restRoot'  => esc_url_raw(rest_url('ki-helfer/v1/')),
            'i18n'      => [
                'placeholder' => __('Frage zu deinem Plugin eingeben…', 'wp-plugin-helfer-rag'),
                'submit'      => __('Frage senden', 'wp-plugin-helfer-rag'),
                'loading'     => __('Sidecar antwortet…', 'wp-plugin-helfer-rag'),
                'error'       => __('Fehler beim Sidecar-Aufruf.', 'wp-plugin-helfer-rag'),
            ],
        ]);
        wp_enqueue_style(
            'wphr-helfer',
            WPHR_PLUGIN_URL . 'admin/helfer.css',
            [],
            WPHR_VERSION
        );
    }

    public function render_page(): void
    {
        if (!current_user_can('manage_options')) {
            wp_die(esc_html__('Keine Berechtigung.', 'wp-plugin-helfer-rag'));
        }
        require WPHR_PLUGIN_DIR . 'templates/admin-helfer.php';
    }

    public function render_settings(): void
    {
        if (!current_user_can('manage_options')) {
            wp_die(esc_html__('Keine Berechtigung.', 'wp-plugin-helfer-rag'));
        }
        require WPHR_PLUGIN_DIR . 'templates/admin-settings.php';
    }
}
