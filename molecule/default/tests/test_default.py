# coding: utf-8
from __future__ import unicode_literals

from ansible.parsing.dataloader import DataLoader
from ansible.template import Templar

import pytest
import os

import testinfra.utils.ansible_runner

import pprint
pp = pprint.PrettyPrinter()

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def base_directory():
    """ ... """
    cwd = os.getcwd()

    if('group_vars' in os.listdir(cwd)):
        directory = "../.."
        molecule_directory = "."
    else:
        directory = "."
        molecule_directory = "molecule/{}".format(os.environ.get('MOLECULE_SCENARIO_NAME'))

    return directory, molecule_directory


@pytest.fixture()
def get_vars(host):
    """
        parse ansible variables
        - defaults/main.yml
        - vars/main.yml
        - molecule/${MOLECULE_SCENARIO_NAME}/group_vars/all/vars.yml
    """
    base_dir, molecule_dir = base_directory()

    file_defaults = "file={}/defaults/main.yml name=role_defaults".format(base_dir)
    file_vars = "file={}/vars/main.yml name=role_vars".format(base_dir)
    file_molecule = "file={}/group_vars/all/vars.yml name=test_vars".format(molecule_dir)

    defaults_vars = host.ansible("include_vars", file_defaults).get("ansible_facts").get("role_defaults")
    vars_vars = host.ansible("include_vars", file_vars).get("ansible_facts").get("role_vars")
    molecule_vars = host.ansible("include_vars", file_molecule).get("ansible_facts").get("test_vars")

    ansible_vars = defaults_vars
    ansible_vars.update(vars_vars)
    ansible_vars.update(molecule_vars)

    templar = Templar(loader=DataLoader(), variables=ansible_vars)
    result = templar.template(ansible_vars, fail_on_undefined=False)

    return result


def config_file(host, get_vars):
    """
    """
    conf_directory = get_vars.get("_chrony_config_file")
    distribution = host.system_info.distribution

    if(distribution in ['redhat', 'centos', 'ol']):
        distribution = "redhat"
    elif(distribution in ['debian', 'ubuntu']):
        distribution = "debian"
    elif(distribution == 'arch'):
        distribution = "archlinux"
    else:
        distribution = "default"

    cfg = conf_directory.get(distribution)
    if(not cfg):
        cfg = conf_directory.get("default")

    return cfg


def test_hosts_file(host):
    f = host.file("/etc/hosts")

    assert f.exists
    assert f.user == "root"
    assert f.group == "root"


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


def test_config_file(host, get_vars):
    """
    """
    f = host.file(config_file(host, get_vars))

    assert f.exists
    assert f.user == "root"
    assert f.group == "root"
