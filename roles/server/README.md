# server

This role prepares, installs and configures [Uyuni](https://uyuni-project.org) and [SUSE Multi-Linux Manager](https://www.suse.com/products/multi-linux-manager/).

## Requirements

Make sure to install the `jmespath` and `xml` Python modules.

The system needs access to the internet. Also, you will need one of the following distributions:

| Product | Distributions |
| ------- | ------------- |
| Uyuni | openSUSE Tumbleweed, Leap 16.x, Leap Micro 6.x |
| SUSE Multi-Linux Manager 5.2 | SL Micro 6.2, SLES 15 SP7 |
| SUSE Multi-Linux Manager 5.1 | SL Micro 6.1, SLES 15 SP7 |

When setting the variable `server_allow_unsupported_distributions` to `true`, the following additional Linux distributions can be used for Uyuni:

- Debian 13
- RHEL 9 and compatible downstreams (AlmaLinux, Rocky Linux, Oracle Linux)
- Ubuntu 24.04

**NOTE**: The Uyuni project won't test against these distributions, the functionalty is provided as-is without any guarantee.

## Role Variables

| Variable | Default | Description |
| -------- | ------- | ----------- |
| `server_allow_unsupported_distributions` | `false` | Allow unsupported distributions (see above) |
| `server_check_requirements` | `true` | Check for hardware requirements |
| `server_suma_release` | `5.2` | SUSE Multi-Linux Manager release to install |
| `server_disk_volumes` | - | Dedicated disk for container volumes |
| `server_disk_database` | - | Dedicated disk for database container volume |
| `server_suma_airgapped` | `false` | Whether to get container image from RPM instead of online registry |
| `server_release` | *empty* | Uyuni release to install (*e.g. `2024.12`*) |
| `server_scc_url` | `https://scc.suse.com` | [SUSE Customer Center](https://scc.suse.com) URL to use (*may be different for some hyperscalers*) |
| `server_scc_reg_code_os` | - | [SUSE Customer Center](https://scc.suse.com) registration code for the OS (optional) |
| `server_scc_reg_code_mlm` | - | [SUSE Customer Center](https://scc.suse.com) registration code (*received after trial registration or purchase*) |
| `server_scc_mail` | - | SUSE Customer Center mail address |
| `server_scc_check_registration` | `true` | Register system if unregistered |
| `server_scc_check_modules` | `true` | Activate required modules if not already enabled |
| `server_slm_modules` | (*Modules required for SUSE Multi-Linux Manager 5.x*) | Modules to enable before installation |
| `server_mail` | `root@localhost` | Web server administrator mail |
| `server_cert_city` | `Darmstadt` | Certificate city |
| `server_cert_country` | `DE` | Certificate country |
| `server_cert_mail` | `root@localhost` | Certificate mail |
| `server_cert_o` | `Darmstadt` | Certificate organization |
| `server_cert_ou` | `Darmstadt` | Certificate organization unit |
| `server_cert_state` | `Hessen` | Certificate state |
| `server_cert_pass` | `uyuni` | Certificate password |
| `server_org_name` | `Demo` | Organization name |
| `server_org_login` | `admin` | Organization administrator username |
| `server_org_password` | `admin` | Organization administrator password |
| `server_org_mail` | `root@localhost` | Organization administrator mail |
| `server_org_first_name` | `Anton` | Organization administrator first name |
| `server_org_last_name` | `Administrator` | Organization administrator last name |
| `server_channels` | *empty* | Common channels to synchronize (*e.g. `almalinux9` and `epel9`*) |
| `server_enable_monitoring` | `false` | Flag whether integrated monitoring stack should be enabled |
| `server_fqdn` | - | Set custom FQDN if `ansible_facts['fqdn']` doesn't work for you |

When supplying channels to create in `channels`, ensure passing a list with dicts like this:

```yaml
- name: almalinux9
  arch: x86_64
- name: almalinux9-appstream
  arch: x86_64
- name: almalinux9-uyuni-client
  arch: x86_64
```

For available channels and architectures, see the `spacewalk-common-channels.ini` installed by the `spacewalk-utils` package. There is also [an online version](https://github.com/uyuni-project/uyuni/blob/master/utils/spacewalk-common-channels.ini) on GitHub.

## Dependencies

No dependencies.

## Example Playbook

Refer to the following example:

```yaml
- hosts: servers
  roles:
    - uyuni_project.uyuni.server
```

Set variables if required, e.g.:

```yaml
---
- hosts: uyuni.giertz.loc
  remote_user: root
  roles:
    - role: uyuni_project.uyuni.server
      server_channels:
        - name: almalinux9
          arch: x86_64
        - name: almalinux9-appstream
          arch: x86_64
        - name: almalinux9-uyuni-client
          arch: x86_64
```

Don't forget setting SUSE-related variables when deploying SUSE Multi-Linux Manager:

```yaml
- hosts: servers
  roles:
    - role: uyuni_project.uyuni.server
      server_scc_reg_code_mlm:
        - DERP1337LULZ
      server_scc_mail: bla@foo.bar
```

Installing Multi-Linux Manager on SLES requires an additional registration code as the MLM subscription only includes SL Micro:

```yaml
- hosts: servers
  roles:
    - role: uyuni_project.uyuni.server
      server_scc_reg_code_os: DERP1337LULZ
      server_scc_reg_code_mlm: RFL0815CPTR
      server_scc_mail: meh@foo.baz
```

If you plan to bootstrap older Uyuni versions, set the Uyuni release:

```yaml
---
- hosts: retro.giertz.loc
  remote_user: root
  roles:
    - role: uyuni_project.uyuni.server
      server_release: '2026.01'
```

## Development

You'll need an customized openSUSE Tumbleweed Podman container (with systemd and other utilities) for testing Uyuni:

```command
$ podman build -t opensuse-tumbleweed-uyuni -f Containerfile.tumbleweed
```

Use `molecule` for running the code:

```command
$ molecule create [--scenario-name mlm]
$ molecule converge [--scenario-name mlm]
$ molecule verify [--scenario-name mlm]
```

SUSE Multi-Linux Manager requires a dedicated container image:

```command
$ podman build -t sles-157-mlm -f Containerfile.sles
```

For testing unsupported Linux distributions (see above), dedicated Containerfiles and scenarios have been prepared:

| Containerfile | Image name | Scenario | Description |
| ------------- | ---------- | -------- | ----------- |
| [`Containerfile.almalinux`](Containerfile.almalinux) | `almalinux9-uyuni` | `almalinux` | AlmaLinux 9 |
| [`Containerfile.debian`](Containerfile.debian) | `debian13-uyuni` | `debian` | Debian 13 (Trixie) |
| [`Containerfile.ubuntu`](Containerfile.ubuntu) | `ubuntu2404-uyuni` | `ubuntu` | Ubuntu LTS 24.04 (Noble Numbat) |

```command
$ podman build -t almalinux9-uyuni -f Containerfile.almalinux
$ molecule create --scenario-name almalinux
$ molecule converge --scenario-name almalinux
$ molecule verify --scenario-name almalinux
```

## License

GPL 3.0

## Author information

Christian Stankowic
