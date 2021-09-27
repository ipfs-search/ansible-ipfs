#!/usr/bin/python

# Copyright: (c) 2021, Mathijs de Bruin <mathijs@mathijsfietst.nl>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: my_test

short_description: This is my test module

# If this is part of a collection, you need to use semantic versioning,
# i.e. the version is of the form "2.5.0" and not "2.4".
version_added: "1.0.0"

description: This is my longer description explaining my test module.

options:
    name:
        description: This is the message to send to the test module.
        required: true
        type: str
    new:
        description:
            - Control to demo if the result of this module is changed or not.
            - Parameter description can be a list as well.
        required: false
        type: bool
# Specify this value according to your collection
# in format of namespace.collection.doc_fragment_name
extends_documentation_fragment:
    - my_namespace.my_collection.my_doc_fragment_name

author:
    - Your Name (@yourGitHubHandle)
'''

EXAMPLES = r'''
# Pass in a message
- name: Test with a message
  my_namespace.my_collection.my_test:
    name: hello world

# pass in a message and have changed true
- name: Test with a message and changed output
  my_namespace.my_collection.my_test:
    name: hello world
    new: true

# fail the module
- name: Test failure of the module
  my_namespace.my_collection.my_test:
    name: fail me
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

import json
from ansible.module_utils.basic import AnsibleModule, heuristic_log_sanitize


class IPFSConfig(AnsibleModule):
    def __init__(self):
        """ Initialization of AnsibleModule and module specifics. """
        super().__init__(
            argument_spec=dict(
                list_all=dict(required=False, type='bool', default=False),
                name=dict(type='str'),
                ipfs_path=dict(type='path', required=False),
                value=dict(type='dict', required=False)
            ),
            mutually_exclusive=[['list_all', 'name'], ['list_all', 'value']],
            required_one_of=[['list_all', 'name']],
            supports_check_mode=True,
        )

        # Perform local initialization
        self._init()

    def _init(self):
        """ Module-specific initialization. """
        ipfs_binary = self.get_bin_path('ipfs', True)
        self._base_args = [ipfs_binary, "config", "--json"]
        self._results = dict(
            changed=False,
        )
        self._command_debug = {}

    def _run_command(self, args):
        (rc, stdout, stderr) = self.run_command(args)

        self._command_debug = dict(
            cmd=self._clean_args(args),
            rc=rc,
            stdout=stdout,
            stderr=stderr
        )

        if rc != 0:
            if 'key has no attributes' in stderr:
                # Key not found returns None
                return None

            msg = heuristic_log_sanitize(stderr.rstrip(), self.no_log_values)
            self.fail_json(cmd=self._clean_args(args), rc=rc, stdout=stdout, stderr=stderr, msg=msg)

        if stdout:
            try:
                return json.loads(stdout)
            except Exception as e:
                self._results.update(self._command_debug)
                self.fail_json('{}: {}'.format(type(e).__name__, e), **self._results)

    def _list_all(self):
        """ Wraps `ipfs config --json show`. """
        args = self._base_args + ['show']

        return self._run_command(args)

    def _get_value(self, name):
        """ Wraps `ipfs config --json -- <name>`. """
        args = self._base_args + ['--', name]

        return self._run_command(args)

    def _set_value(self, name, value):
        """ Wraps `ipfs config --json -- <name> <value>`. """
        json_value = json.dumps(value)
        args = self._base_args + ['--', name, json_value]
        self._run_command(args)

    def run(self):
        """ Perform module action. """
        if self.params['ipfs_path']:
            self.run_command_environ_update['IPFS_PATH'] = self.params['ipfs_path']

        name = self.params['name']
        new_value = self.params['value']
        list_all = self.params['list_all']

        if list_all:
            # Return all values
            self._results.update(dict(value=self._list_all()))

        else:
            # Get specific value
            orig_value = self._get_value(name)

            if new_value:
                # Conditionally update value
                if orig_value != new_value:
                    if not self.check_mode:
                        self._set_value(name, new_value)

                    self._results.update(dict(
                        msg='setting changed',
                        changed=True,
                        # Original and final value, as dict
                        orig_value=orig_value,
                        value=new_value
                    ))

                    if self._diff:
                        # Add string diff
                        self._results['diff'] =dict(
                            before_header=name + ' (before)',
                            before=self.jsonify(orig_value),
                            after_header=name + ' (after)',
                            after=self.jsonify(new_value)
                        )
            else:
                self._results['value'] = orig_value

        if self._debug:
            self._results.update(self._command_debug)

        self.exit_json(**self._results)

if __name__ == '__main__':
    IPFSConfig().run()
