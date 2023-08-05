# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from knack.util import CLIError


def validate_local_context(cmd, namespace):  # pylint: disable=unused-argument
    if not cmd.cli_ctx.local_context.username:
        raise CLIError('Can\'t get system user account. Local Context is ignored.')
    if not cmd.cli_ctx.local_context.current_dir:
        raise CLIError('The working directory has been deleted or recreated. You can change to another working '
                       'directory or reenter current one if it is recreated.')


def validate_local_context_for_delete(cmd, namespace):
    if (namespace.all and namespace.name) or (not namespace.all and not namespace.name):
        raise CLIError('Please specify either --name or --all.')

    validate_local_context(cmd, namespace)
