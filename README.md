# Ansible Role: `chrony`

[![GitHub Super-Linter](https://github.com/Frzk/ansible-role-chrony/actions/workflows/linter.yml/badge.svg?branch=main)](https://github.com/marketplace/actions/super-linter)
[![Molecule](https://github.com/Frzk/ansible-role-chrony/actions/workflows/molecule.yml/badge.svg?branch=main)](https://github.com/Frzk/ansible-role-chrony/actions/workflows/molecule.yml)
[![Ansible Role](https://img.shields.io/ansible/role/d/55387?color=2997FF&label=Ansible%20Galaxy%20downloads&logo=ansible)](https://galaxy.ansible.com/Frzk/chrony)

This Ansible role allows you to install `chrony` and manage its configuration.

An hardened systemd unit file is setup when deploying under Debian >= 11 and Arch Linux.

For more information about `chrony`, please check [the official project page](https://chrony.tuxfamily.org/).

## Requirements

None

## Dependencies

None

## Role variables

| Variable name               | Description                                                                    | Default value                          |
| --------------------------- | ------------------------------------------------------------------------------ | -------------------------------------- |
| `chrony_service_name`       | Service name.                                                                  | `chronyd`                              |
| `chrony_ntp_pools`          | A list of NTP pools to use, with their options.                                | `[ 'pool.ntp.org iburst maxpoll 10' ]` |
| `chrony_ntp_servers`        | A list of NTP servers to use, with their options.                              | `[]`                                   |
| `chrony_ntp_peers`          | A list of NTP peers to use, with their options.                                | `[]`                                   |
| `chrony_config_file`        | Path to chrony configuration file.                                             | `/etc/chrony.conf`                     |
| `chrony_config_logdir`      | Path to chrony logs directory.                                                 | `/var/log/chrony`                      |
| `chrony_config_driftfile`   | Path to chrony drift file.                                                     | `/var/lib/chrony/drift`                |
| `chrony_makestep_threshold` | Limit (in sec) above which chrony will step the clock instead of slewing it.   | `1`                                    |
| `chrony_makestep_limit`     | Limit (in nb) above which chrony won't step the clock anymore, even if needed. | `10`                                   |
| `chrony_allow`              | List of subnets allowed to access this computer as an NTP server.              | `[]`                                   |
| `chrony_deny`               | List of subnets NOT allowed to access this computer as an NTP server.          | `[]`                                   |

:green_book: Documentation:

- [Chrony configuration documentation](https://chrony.tuxfamily.org/doc/4.2/chrony.conf.html)

## Example

Here is a small **example** playbook.

**IMPORTANT**: DO NOT use this example as it is.

```yaml
---
- hosts: all
  become: true
  roles:
    - role: frzk.chrony
      chrony_service_name: chronyd
      chrony_ntp_pools: []
      chrony_ntp_servers:
        - 0.rhel.pool.ntp.org iburst maxpoll 10
        - 1.rhel.pool.ntp.org iburst maxpoll 10
        - 2.rhel.pool.ntp.org iburst maxpoll 10
        - 3.rhel.pool.ntp.org iburst maxpoll 10
      chrony_ntp_peers:
        - ntp00.example.com maxpoll 10
        - ntp01.example.com maxpoll 10
        - ntp02.example.com maxpoll 10
      chrony_config_file: /etc/chrony.conf
      chrony_config_driftfile: /var/lib/chrony/drift
      chrony_makestep_threshold: 5
      chrony_makestep_limit: 3
      chrony_allow:
        - 192.0.2.0/24
        - 192.0.2.200
      chrony_deny:
        - 192.0.2.0/25
...
```
## Testing

Testing is done by leveraging Molecule and Ansible (see [verify.yml](molecule/default/verify.yml)), through GitHub Actions and Docker containers.

Tests successfully pass under the following distributions:

- Arch Linux
- Debian 11
- Debian 10
- Debian 9
- Ubuntu 20.04
- Ubuntu 18.04

## Contributing

Code reviews, patches, comments, bug reports and feature requests are welcome. Please read the [Contributing Guide](CONTRIBUTING.md) for further details.
