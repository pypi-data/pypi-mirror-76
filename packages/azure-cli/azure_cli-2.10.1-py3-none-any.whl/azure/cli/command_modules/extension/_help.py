# coding=utf-8
# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from knack.help_files import helps  # pylint: disable=unused-import
# pylint: disable=line-too-long, too-many-lines

helps['extension'] = """
type: group
short-summary: Manage and update CLI extensions.
"""

helps['extension add'] = """
type: command
short-summary: Add an extension.
parameters:
  - name: --system
    type: string
    short-summary: Use a system directory for the extension.
    long-summary: Default path is azure-cli-extensions folder under the CLI running python environment lib path, configurable by environment variable AZURE_EXTENSION_SYS_DIR. On Windows, you may need to open your shell as Administrator to run with the right permission.
examples:
  - name: Add extension by name
    text: az extension add --name anextension
  - name: Add extension from URL
    text: az extension add --source https://contoso.com/anextension-0.0.1-py2.py3-none-any.whl
  - name: Add extension from local disk
    text: az extension add --source ~/anextension-0.0.1-py2.py3-none-any.whl
  - name: Add extension from local disk and use pip proxy for dependencies
    text: az extension add --source ~/anextension-0.0.1-py2.py3-none-any.whl --pip-proxy https://user:pass@proxy.server:8080
  - name: Add extension to system directory
    text: az extension add --name anextension --system
"""

helps['extension list'] = """
type: command
short-summary: List the installed extensions.
"""

helps['extension list-available'] = """
type: command
short-summary: List publicly available extensions.
examples:
  - name: List all publicly available extensions
    text: az extension list-available
  - name: List details on a particular extension
    text: az extension list-available --show-details --query anextension
"""

helps['extension remove'] = """
type: command
short-summary: Remove an extension.
examples:
  - name: Remove an extension. (autogenerated)
    text: az extension remove --name MyExtension
    crafted: true
"""

helps['extension show'] = """
type: command
short-summary: Show an extension.
examples:
  - name: Show an extension. (autogenerated)
    text: az extension show --name MyExtension
    crafted: true
"""

helps['extension update'] = """
type: command
short-summary: Update an extension.
examples:
  - name: Update an extension by name
    text: az extension update --name anextension
  - name: Update an extension by name and use pip proxy for dependencies
    text: az extension update --name anextension --pip-proxy https://user:pass@proxy.server:8080
"""
