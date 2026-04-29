<?php
/**
 * Plugin-Hauptklasse — Singleton-Container, der alle Komponenten registriert.
 *
 * @package KiEngineeringWerkstatt\WpPluginHelferRag
 */

declare(strict_types=1);

if (!defined('ABSPATH')) {
    exit;
}

final class Wphr_Plugin
{
    private static ?Wphr_Plugin $instance = null;

    public static function instance(): Wphr_Plugin
    {
        if (self::$instance === null) {
            self::$instance = new self();
        }
        return self::$instance;
    }

    public function run(): void
    {
        // Übersetzungen laden.
        add_action('init', [$this, 'load_textdomain']);

        // Admin-Seite registrieren (nur im Backend).
        if (is_admin()) {
            (new Wphr_Admin())->register();
        }

        // REST-Endpoint registrieren.
        (new Wphr_Rest())->register();
    }

    public function load_textdomain(): void
    {
        load_plugin_textdomain(
            'wp-plugin-helfer-rag',
            false,
            dirname(WPHR_PLUGIN_BASENAME) . '/languages'
        );
    }

    public static function activate(): void
    {
        // Default-Optionen anlegen — ohne Sidecar-URL läuft das Plugin noch nicht.
        if (get_option('wphr_settings') === false) {
            add_option('wphr_settings', [
                'sidecar_url'      => 'http://localhost:8765',
                'sidecar_api_key'  => '',
                'max_query_tokens' => 2000,
                'log_queries'      => false,
            ]);
        }
    }

    public static function deactivate(): void
    {
        // Aktuell kein Cleanup — Optionen bleiben für Wiedereinrichtung.
    }
}
