# ansible-collection-uyuni

Ansible Collection for managing Uyuni / SUSE Multi-Linux Manager installations and ressources.

## Roles

- [`server`](roles/server) - Prepares, installs and configures Uyuni or SUSE Multi-Linux Manager server
- [`client`](roles/client) - Bootstraps Uyuni or SUSE Multi-Linux Manager clients
- [`proxy`](roles/proxy) - Prepares, installs and configures Uyuni or SUSE Multi-Linux Manager Proxy server

## Plugins

- [`apply_highstate`](plugins/modules/apply_highstate.py) - Apply a host's highstate
- [`apply_states`](plugins/modules/apply_states.py) - Apply states for a host
- [`install_patches`](plugins/modules/install_patches.py) - Installs patches on managed hosts
- [`install_upgrades`](plugins/modules/install_upgrades.py) - Installs package upgrades on managed hosts
- [`inventory`](plugins/inventory/inventory.py) - Dynamic inventory
- [`openscap_run`](plugins/modules/openscap_run.py) - Schedules OpenSCAP runson managed hosts
- [`reboot_host`](plugins/modules/reboot_host.py) - Reboots a managed hosts
- [`clp_version`](plugins/modules/clp_version.py) - Create CLP version
- [`clp_promote`](plugins/modules/clp_promote.py) - Promote CLP version

### Event-driven Ansible

- [`requires_reboot`](extensions/eda/plugins/event_source/requires_reboot.py) - Checks whether a particular system requires a reboot

Check-out [issues](https://codeberg.org/stdevel/ansible-collection-uyuni/issues) for known issues, missing and upcoming functionality.

## Notes

When using SLES or SL(E) Micro for using this collection you will most likely have to install an additional Python interpreter - the system-wide installation (3.6) is way too old.

## Demonstration

See [the following Git repository](https://codeberg.org/stdevel/susecon-suma-aap-demo) for a demonstration of using this collection with AWX.
