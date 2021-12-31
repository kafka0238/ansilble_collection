#!/usr/bin/python

# Copyright: (c) 2018, Terry Jones <terry.jones@example.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: my_own_module

short_description: Create text file

# If this is part of a collection, you need to use semantic versioning,
# i.e. the version is of the form "2.5.0" and not "2.4".
version_added: "1.0.0"

description: This module create text file with path from param path and write into it text from param content.

options:
    path:
        description: This is the path where should be created file.
        required: true
        type: str
    content:
        description: This is the text which should be wrote in file.
        required: true
        type: str
# Specify this value according to your collection
# in format of namespace.collection.doc_fragment_name
extends_documentation_fragment:
    - my_namespace.my_collection.my_doc_fragment_name

author:
    - kafka
'''

EXAMPLES = r'''
# Pass in a message
- name: Test with a message
  my_own_namespace.yandex_cloud_elk.my_own_module:
    path: /tmp/file.txt
    content: the module test was successful
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
original_message:
    description: The original name param that was passed in.
    type: str
    returned: always
    sample: 'hello world'
message:
    description: The output message that the test module generates.
    type: str
    returned: always
    sample: 'goodbye'
'''

import os

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_bytes


def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        path=dict(type='str', required=True),
        content=dict(type='str', required=True)
    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # changed is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        module.exit_json(**result)

    # manipulate or modify the state as needed (this is going to be the
    # part where your module will do what it needs to do)
    path = module.params['path']
    content = module.params['content']

    b_path = to_bytes(path, errors='surrogate_or_strict')
    changed = False
    result = {'dest': path}

    if not module.check_mode:
        if not os.path.lexists(b_path):
            try:
                open(b_path, 'wb').close()
                changed = True
            except (OSError, IOError) as e:
                raise AnsibleModuleError(results={'msg': 'Error, could not touch target: %s'
                                                         % to_native(e, nonstring='simplerepr'),
                                                  'path': path})

        with open(b_path, 'r') as fp:
            old_content = fp.read()

        if old_content != content:
            changed = True
            with open(b_path, 'w') as fp:
                fp.write(content)

    result['changed'] = changed

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
