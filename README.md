# CCEI Tild integration for Home Assistant

The repository provide a Home Assistant integration for CCEI Tild pool box. It's based on
[Ricky_D](https://forum.hacf.fr/u/Ricky_D) [works](https://forum.hacf.fr/t/tild-piscine/22627).

## Installation

Put the `custom_components/ccei_tild` directory in your Home Assistant `custom_components` directory
and restart Home Assistant. You can now add this integration (look for _"CCEI Tild"_) and provide the
IP address (or hostname) of your Tild box.

__Note:__ The `custom_components` directory is located in the same directory of the
`configuration.yaml`. If it doesn't exists, create it.

## Run development environment

A development environment is provided with this integration if you want to contribute. The `manage`
script at the root of the repository permit to create and start a Home Assistant docker container
with a pre-installation of this integration (linked to sources).

Start by create the container by running the command `./manage create` and start it by running
`./manage start` command. You can now access to Home Assistant web interface on
[http://localhost:8123](http://localhost:8123) and follow the initialization process of the Home
Assistant instance.

A fake Tild server is also provide to emulate a Tild box. You can start it by running the command
`./manage fake-tild`. This fake server is listening on your computer IP address (`0.0.0.0:30302`)
and you can add the integration by providing the IP address to Home Assistant configuration dialog.

Futhermore, the `manage analyse-tild-state-data` command is provided to help to analyse raw status
data retrieved from Tild box:

```
usage: manage analyse-tild-state-data [-h] [-M] [-F] data [data ...]

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

Don't forget to restart Home Assistant after and you will be able to follow docker container logs by
running `./manage logs` command.
