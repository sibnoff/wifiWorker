CREATE TABLE IF NOT EXISTS `logins` (
    `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT,
    `service` varchar(255) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
    `login` varchar(255) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
    `pass` varchar(255) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
    `timestamp` int(11) UNSIGNED NOT NULL DEFAULT 0,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
