<?php
/**
 * REST-Endpoint /wp-json/ki-helfer/v1/frage — leitet an den Python-Sidecar weiter.
 *
 * @package KiEngineeringWerkstatt\WpPluginHelferRag
 */

declare(strict_types=1);

if (!defined('ABSPATH')) {
    exit;
}

final class Wphr_Rest
{
    private const NAMESPACE = 'ki-helfer/v1';

    public function register(): void
    {
        add_action('rest_api_init', [$this, 'register_routes']);
    }

    public function register_routes(): void
    {
        register_rest_route(self::NAMESPACE, '/frage', [
            'methods'             => 'POST',
            'callback'            => [$this, 'handle_frage'],
            'permission_callback' => [$this, 'check_permission'],
            'args'                => [
                'frage' => [
                    'type'              => 'string',
                    'required'          => true,
                    'sanitize_callback' => 'sanitize_textarea_field',
                    'validate_callback' => static fn ($val) => is_string($val) && strlen($val) >= 3 && strlen($val) <= 2000,
                ],
                'kontext' => [
                    'type'              => 'string',
                    'required'          => false,
                    'sanitize_callback' => 'sanitize_text_field',
                    'default'           => 'doku',
                ],
            ],
        ]);

        register_rest_route(self::NAMESPACE, '/health', [
            'methods'             => 'GET',
            'callback'            => [$this, 'handle_health'],
            'permission_callback' => [$this, 'check_permission'],
        ]);
    }

    public function check_permission(): bool
    {
        return current_user_can('manage_options');
    }

    public function handle_frage(WP_REST_Request $request): WP_REST_Response
    {
        $settings    = (array) get_option('wphr_settings', []);
        $sidecar_url = $settings['sidecar_url'] ?? 'http://localhost:8765';
        $api_key     = $settings['sidecar_api_key'] ?? '';

        $payload = [
            'frage'   => (string) $request->get_param('frage'),
            'kontext' => (string) ($request->get_param('kontext') ?: 'doku'),
        ];

        $headers = ['Content-Type' => 'application/json'];
        if ($api_key !== '') {
            $headers['Authorization'] = 'Bearer ' . $api_key;
        }

        $response = wp_remote_post(trailingslashit($sidecar_url) . 'frage', [
            'headers' => $headers,
            'body'    => wp_json_encode($payload),
            'timeout' => 30,
        ]);

        if (is_wp_error($response)) {
            return new WP_REST_Response([
                'fehler' => 'sidecar_unreachable',
                'detail' => $response->get_error_message(),
            ], 502);
        }

        $code = wp_remote_retrieve_response_code($response);
        $body = (string) wp_remote_retrieve_body($response);

        if ($code !== 200) {
            return new WP_REST_Response([
                'fehler'   => 'sidecar_error',
                'http'     => $code,
                'sidecar'  => json_decode($body, true) ?? $body,
            ], 502);
        }

        $decoded = json_decode($body, true);
        if (!is_array($decoded)) {
            return new WP_REST_Response([
                'fehler' => 'invalid_sidecar_response',
                'body'   => substr($body, 0, 200),
            ], 502);
        }

        // Optional: Audit-Log wenn aktiviert (nur Hash der Frage, keine Klartext-Persistenz).
        if (!empty($settings['log_queries'])) {
            $hash = wp_hash($payload['frage']);
            do_action('wphr_query_logged', $hash, $payload['kontext'], time());
        }

        return new WP_REST_Response($decoded, 200);
    }

    public function handle_health(WP_REST_Request $request): WP_REST_Response
    {
        $settings    = (array) get_option('wphr_settings', []);
        $sidecar_url = $settings['sidecar_url'] ?? 'http://localhost:8765';

        $response = wp_remote_get(trailingslashit($sidecar_url) . 'health', ['timeout' => 5]);
        $reachable = !is_wp_error($response) && wp_remote_retrieve_response_code($response) === 200;

        return new WP_REST_Response([
            'plugin_version'   => WPHR_VERSION,
            'sidecar_url'      => $sidecar_url,
            'sidecar_erreichbar' => $reachable,
        ], 200);
    }
}
