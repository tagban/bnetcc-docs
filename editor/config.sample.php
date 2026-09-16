<?php
/*
 * Copy this file OUTSIDE the website folder, to:
 *   ~/editor-config/edit.bnet.cc.php
 * and fill in the values. It holds secrets, so it must never be inside edit.bnet.cc/.
 */
return [
    'site_name' => 'BNET.cc Docs',
    'site_url' => 'https://docs.bnet.cc',
    // Where the editor itself is reached. Defaults to site_url + '/editor'. Set it when the
    // editor has its own domain, such as 'https://edit.bnet.cc'.
    'editor_url' => 'https://edit.bnet.cc',
    // The site's stylesheets, loaded from site_url. Defaults to /css/wiki.css and /css/site.css.
    // 'stylesheets' => ['/css/wiki.css', '/css/site.css'],

    'discord' => [
        // Discord Developer Portal > your application > OAuth2
        'client_id' => '',
        'client_secret' => '',
        // Right-click the server icon > Copy Server ID (needs Developer Mode in Discord settings)
        'guild_id' => '',
        // Server Settings > Roles > right-click the role > Copy Role ID
        'role_ids' => [''],
        'role_name' => '',
        'invite' => 'https://discord.gg/dR4djHweh3',
    ],

    'github' => [
        // Fine-grained token limited to this one repository, with
        // "Contents: Read and write" and "Pull requests: Read and write".
        'token' => '',
        'repo' => 'tagban/bnetcc-docs',
        'branch' => 'main',
    ],

    // Local testing only (php -S): skip Discord login and record GitHub writes instead of sending them.
    // 'dev_user' => ['id' => '1', 'username' => 'test', 'name' => 'Test', 'avatar' => null, 'token' => '', 'token_expires' => PHP_INT_MAX],
    // 'dry_run' => true,

    'limits' => [
        'edits_per_hour' => 10,
        'image_max_bytes' => 5000000,
        'image_max_width' => 1600,
    ],
];
