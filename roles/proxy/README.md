# proxy

This role prepares, installs and configures [Uyuni](https://uyuni-project.org) and [SUSE Multi-Linux Manager](https://www.suse.com/products/multi-linux-manager/) proxy servers.

## Requirements

Make sure to install the `jmespath` and `xml` Python modules.

The system needs access to the internet. Also, you will need one of the following distributions:

| Product | Distributions |
| ------- | ------------- |
| Uyuni | openSUSE Tumbleweed, Leap 16.x, Leap Micro 6.x |
| Multi-Linux Manager 5.1 | SL Micro 6.1, SLES 15 SP7 |

When setting the variable `server_allow_unsupported_distributions` to `true`, the following additional Linux distributions can be used for Uyuni:

- Debian 13
- RHEL 9 and compatible downstreams (AlmaLinux, Rocky Linux, Oracle Linux)
- Ubuntu 24.04

**NOTE**: The Uyuni project won't test against these distributions, the functionalty is provided as-is without any guarantee.

## Role Variables

| Variable | Default | Description |
| -------- | ------- | ----------- |
| `proxy_allow_unsupported_distributions` | `false` | Allow unsupported distributions (see above) |
| `proxy_disk` | - | Dedicated disk for volume |
| `proxy_config_file` | - | Proxy configuration tarball (**required**) |
| `proxy_uyuni_release`, `proxy_suma_release` | - | Specific release |
| `proxy_scc_url` | `https://scc.suse.com` | [SUSE Customer Center](https://scc.suse.com) URL to use (*may be different for some hyperscalers*) |
| `proxy_scc_reg_code_os` | - | [SUSE Customer Center](https://scc.suse.com) registration code for the OS (optional) |
| `proxy_scc_reg_code_mlm` | - | [SUSE Customer Center](https://scc.suse.com) registration code (*received after trial registration or purchase*) |
| `proxy_scc_mail` | - | SUSE Customer Center mail address |
| `proxy_scc_check_registration` | `true` | Register system if unregistered |
| `proxy_scc_check_modules` | `true` | Activate required modules if not already enabled |

## Dependencies

No dependencies.

## Example Playbook

Refer to the following example:

```yaml
---
- hosts: prawwxy.giertz.loc
  roles:
    - role: uyuni_project.uyuni.proxy
      proxy_config_file: myproxy.tar.gz
```

Use a dedicated disk for the proxy cache:

```yaml
---
- hosts: darmstadt.hessen.loc
  roles:
    - role: uyuni_project.uyuni.proxy
      proxy_config_file: eigude.tar.gz
      proxy_disk: /dev/sdb
      proxy_uyuni_release: '2024.12'
```

Set SCC-related variables when installing a MLM proxy:

```yaml
- hosts: enterprise.lega.cy
  roles:
    - role: uyuni_project.uyuni.proxy
      proxy_config_file: lvdg.mybiz.loc
      proxy_scc_reg_code_os: DERP1337LULZ
      proxy_scc_reg_code_mlm: RFL0815CPTR
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

Christian Stankowic (info@cstan.io)
