# CCEI Tild integration for Home Assistant

The repository provide a Home Assistant integration for CCEI Tild pool box. It's allow to retrieve
the current state of the Tild box (water temperature, light, filtration, ...), act on it (turn on/off
the filtration/auxiliary/light, change it color/intensity, ...) and edit it configuration
(light/filtration/auxiliary programming).

It's initialy based on [Ricky_D](https://forum.hacf.fr/u/Ricky_D) works to reverse the protocol used
between the [smartphone app](https://play.google.com/store/apps/details?id=com.ccei.tild) and the
device before I taked care about this project to make it a real and complete Home-Assistant
integration. Thank's to him !

**Note:** This integration is borned on [the HACF forum](https://forum.hacf.fr/t/tild-piscine/22627).

## Installation

### Using HACS

Add CCEI Tild integration via HACS:

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=brenard&repository=ccei-tild-custom-component&category=integration)

Add your CCEI Tild pool box via the Integration menu:

[![Open your Home Assistant instance and start setting up a new integration.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=ccei_tild)

_Note:_ A [request](https://github.com/hacs/default/pull/2160) for integration as default repository
in HACS is currently pending.

### Manually

Put the `custom_components/ccei_tild` directory in your Home Assistant `custom_components` directory
and restart Home Assistant. You can now add this integration (look for _"CCEI Tild"_) and provide the
IP address (or hostname) of your Tild box.

__Note:__ The `custom_components` directory is located in the same directory of the
`configuration.yaml`. If it doesn't exists, create it.

## Run development environment

A development environment is provided with this integration if you want to contribute. The `manage`
script at the root of the repository permit to create and start a Home Assistant docker container
with a pre-installation of this integration (linked to sources).

To create and start the container, just run the command `./manage start`. The container logs will
be show on console and you can access to Home Assistant web interface on
[http://localhost:8123](http://localhost:8123). On first start, you need to follow the
initialization process of the Home Assistant instance as on a regular installation.

A fake Tild server is also provide to emulate a Tild box. This fake server is running and listening
inside the Home-Assistant container (`0.0.0.0:30302`). As a regular Tild box, it's could be
automatically discovered when you add the integration, or you could enter the `127.0.0.1` IP address
(or `localhost`) in the configuration dialog.

__Note:__ you could disable it by setting the `USE_FAKE_TILD` variable to zero inside the `manage` script.

Futhermore, the `manage analyse-tild-state-data` command is provided to help to analyse raw status
data retrieved from Tild box:

```
usage: analyse-tild-state-data [-h] [-M] [-F] data [data ...]

positional arguments:
  data

options:
  -h, --help      show this help message and exit
  -M, --markdown  Format output in Markdown
  -F, --forum     Format output for the forum
```

## Debugging

To enable debug log, edit the `configuration.yaml` file and locate the `logger` block. If it does not
exists, add it with the following content :

```yaml
logger:
  default: warn
  logs:
    custom_components.ccei_tild: debug
```

Don't forget to restart Home Assistant after.
