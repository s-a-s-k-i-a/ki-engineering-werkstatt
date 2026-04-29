<?php
/**
 * Plugin Name:       KI-Plugin-Helfer RAG
 * Plugin URI:        https://github.com/s-a-s-k-i-a/ki-engineering-werkstatt/tree/main/projekte/19-A-wp-plugin-helfer-rag
 * Description:       RAG-basierter Plugin-Doku-Helfer + Code-Search + Issue-Triage. Spricht über REST mit einem selbst gehosteten Python-Sidecar (vLLM/Ollama + Qdrant). DSGVO-konform — keine Daten verlassen deine Infrastruktur.
 * Version:           0.1.0
 * Requires at least: 6.6
 * Requires PHP:      8.1
 * Author:            Saskia Teichmann (isla-stud.io / citelayer®)
 * Author URI:        https://isla-stud.io
 * License:           MIT
 * License URI:       https://opensource.org/licenses/MIT
 * Text Domain:       wp-plugin-helfer-rag
 * Domain Path:       /languages
 *
 * @package KiEngineeringWerkstatt\WpPluginHelferRag
 */

declare(strict_types=1);

if (!defined('ABSPATH')) {
    exit; // Direkt-Zugriff verboten.
}

define('WPHR_VERSION', '0.1.0');
define('WPHR_PLUGIN_DIR', plugin_dir_path(__FILE__));
define('WPHR_PLUGIN_URL', plugin_dir_url(__FILE__));
define('WPHR_PLUGIN_BASENAME', plugin_basename(__FILE__));

// PSR-4-ähnlicher Auto-Loader für `includes/class-*.php`.
spl_autoload_register(static function (string $class): void {
    if (strpos($class, 'Wphr_') !== 0) {
        return;
    }
    $file = WPHR_PLUGIN_DIR . 'includes/class-' . strtolower(str_replace('_', '-', substr($class, 5))) . '.php';
    if (is_readable($file)) {
        require_once $file;
    }
});

/**
 * Plugin-Bootstrap.
 */
function wphr_bootstrap(): void
{
    Wphr_Plugin::instance()->run();
}

add_action('plugins_loaded', 'wphr_bootstrap');

// Aktivierungs-/Deaktivierungs-Hooks (Default-Optionen + Cleanup).
register_activation_hook(__FILE__, ['Wphr_Plugin', 'activate']);
register_deactivation_hook(__FILE__, ['Wphr_Plugin', 'deactivate']);
