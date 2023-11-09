[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]][license]

[![hacs][hacsbadge]][hacs]
[![Project Maintenance][maintenance-shield]][user_profile]

[![Community Forum][forum-shield]][forum]

The component provide a Home Assistant integration for CCEI Tild pool box. It's allow to retrieve
the current state of the Tild box (water temperature, light, filtration, ...), act on it (turn on/off
the filtration/auxiliary/light, change it color/intensity, ...) and edit it configuration
(light/filtration/auxiliary programming).

{{ "{% if not installed %}" }}

## Installation

1. Click install.
1. In the HA UI go to "Configuration" -> "Integrations" click "+" and search for "CCEI Tild".

{{ "{% endif %}" }}

## Configuration is done in the UI

When adding the integration, the integration will try to detect your Tild box by using the same
method as the smartphone application. If detected, you will just have to confirm detected
information and you'r done. Otherwise, you will have to provide :

* The name of your Tild box. It will be used only to name the device in Home-Assistant
* The IP address (or the hostname) of the Tild box
* The refresh rate of the information of the Tild box (default: 5 minutes)

**Note:** The provided IP address (or hostname) will be used to connect on your Tild box. Please
configure a static IP address (or reserved it on your DHCP configuration) to be sure it will not
changed. Otherwise, you will have to reconfigure the integration in Home-Assistant on each change.

## Credits

This project is initialy based on [Ricky_D](https://forum.hacf.fr/u/Ricky_D) works to reverse the
protocol used between the [smartphone app](https://play.google.com/store/apps/details?id=com.ccei.tild)
and the device before I taked care about this project to make it a real and complete Home-Assistant
integration. Thank's to him !


---

[commits-shield]: https://img.shields.io/github/commit-activity/y/brenard/ccei-tild-custom-component.svg?style=for-the-badge
[commits]: https://github.com/brenard/ccei-tild-custom-component/commits/main
[hacs]: https://hacs.xyz
[hacsbadge]: https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge
[license]: https://github.com/brenard/ccei-tild-custom-component/blob/main/LICENSE
[license-shield]: https://img.shields.io/github/license/brenard/ccei-tild-custom-component.svg?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-%40brenard-blue.svg?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/brenard/ccei-tild-custom-component.svg?style=for-the-badge
[releases]: https://github.com/brenard/ccei-tild-custom-component/releases
[user_profile]: https://github.com/brenard
