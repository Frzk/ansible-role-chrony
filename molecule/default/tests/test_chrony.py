#!/usr/bin/env python
# coding: utf8

import os
from testinfra.utils.ansible_runner import AnsibleRunner


testinfra_hosts = AnsibleRunner(os.environ["MOLECULE_INVENTORY_FILE"])\
                  .get_hosts("all")


def test_chrony_is_installed(host):
    """
    """
    package_name = "chrony"

    chrony = host.package(package_name)
    assert chrony.is_installed


def test_chrony_running_and_enabled(host):
    """
    """
    os = host.system_info.distribution
    service_name = "chronyd"

    if os in ("debian", "ubuntu"):
        service_name = "chrony"

    chrony = host.service(service_name)
    assert chrony.is_running
    assert chrony.is_enabled
