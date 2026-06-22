#!/usr/bin/python
"""
Ansible Module for creating Content Lifecycle Project versions

2026 Christian Stankowic

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: clp_version
short_description: Create CLP version
description:
  - Creating Content Lifecycle Project version
author:
  - "Christian Stankowic (@stdevel)"
extends_documentation_fragment:
  - uyuni_project.uyuni.uyuni_auth
options:
  project_label:
    description: Name of the Content Lifecycle Project
    required: True
    type: str
  version_message:
    description: Version history message
    type: str
'''

EXAMPLES = '''
- name: Create new CLP version
  uyuni_project.uyuni.clp_version:
    uyuni_host: 192.168.1.1
    uyuni_user: admin
    uyuni_password: admin
    project_label: leap-servers
    version_message: Weekly updates
'''

RETURN = '''
entity:
  description: State whether project was built successfully
  returned: success
  type: bool
'''

from ansible.module_utils.basic import AnsibleModule
from ..module_utils.exceptions import EmptySetException, SSLCertVerificationError
from ..module_utils.helper_functions import _configure_connection


def _build_clp_version(module, api_instance):
    """
    Builds a Content Lifecycle Project
    """
    try:
        api_instance.build_clp_version(
            module.params.get('project_label'),
            module.params.get('version_message')
        )
        module.exit_json(changed=True)
    except SSLCertVerificationError:
        module.fail_json(msg="Failed to verify SSL certificate")
    except EmptySetException as err:
        module.fail_json(msg=f"Exception when calling UyuniAPI->build_clp_version: {err}")


def main():
    """
    Main function
    """
    argument_spec = dict(
        uyuni_host=dict(required=True),
        uyuni_user=dict(required=True),
        uyuni_password=dict(required=True, no_log=True),
        uyuni_port=dict(default=443, type='int'),
        uyuni_verify_ssl=dict(default=True, type='bool'),
        project_label=dict(type='str', required=True),
        version_message=dict(type='str')
    )

    module = AnsibleModule(argument_spec=argument_spec)

    connection_params = dict(
        host=module.params.get('uyuni_host'),
        username=module.params.get('uyuni_user'),
        password=module.params.get('uyuni_password'),
        port=module.params.get('uyuni_port'),
        verify_ssl=module.params.get('uyuni_verify_ssl')
    )

    api_instance = _configure_connection(connection_params)
    _build_clp_version(module, api_instance)


if __name__ == '__main__':
    main()
