import sys
from pathlib2 import Path

# Append parent directory of `tree_util_lite` and `binary_vcs_lite` package
sys.path.append(str(Path(__file__).resolve().parent.parent))
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
sys.path.append(str(Path(__file__).resolve().parent.parent.parent.joinpath(
    'tree-util-lite'
)))

from binary_vcs_lite.common.util import *
from binary_vcs_lite.vcs_interface import LocalVersioning, RemoteVersioning

_TEST_ROOT = Path(r'D:\temp\binary-vcs-lite-test-data')

ASSET_FILE_PATTERN = {
    'INCLUDE': ['**/*'],
    'EXCLUDE': [
        '.vcs_lite',
        '.piece_common',
        '.mov$',
        '.tx$',
        '.turntable.',
        '.db$'
    ]
}


def init():
    # We have 2 workspaces with 2 corresponding local repos
    #   These local repos store "wip" session data
    # And one central repo which is connected to by 2 workspaces
    #   This repo stores "review" and "publish" session data
    # All these repos are independent of each other
    #
    workspace_1_dir = _TEST_ROOT.joinpath('workspace_1')
    workspace_2_dir = _TEST_ROOT.joinpath('workspace_2')
    central_repo_dir = _TEST_ROOT.joinpath('central_repo')

    # Local versioning with workspace 1
    ws_1_local = LocalVersioning(workspace_1_dir, 'wip')

    # Local versioning with workspace 2
    ws_2_local = LocalVersioning(workspace_2_dir, 'wip')

    # Remote versioning with workspace 1
    ws_1_remote = RemoteVersioning(workspace_1_dir, central_repo_dir, 'review')

    # Remote versioning with workspace 2
    ws_2_remote = RemoteVersioning(workspace_2_dir, central_repo_dir, 'review')

    return ws_1_local, ws_2_local, ws_1_remote, ws_2_remote


def standard_commit():
    ws_1_local, ws_2_local, ws_1_remote, ws_2_remote = init()

    # Commit to local repo
    ws_1_local.set_file_pattern(ASSET_FILE_PATTERN)
    ws_1_local.commit(
        ['wip'],
        data={'message': 'workspace 1, local commit 1'},
        add_only=0,
        fast_forward=0
    )

    # Commit to remote repo
    ws_1_remote.set_file_pattern(ASSET_FILE_PATTERN)
    ws_1_remote.commit(
        ['review'],
        data={'message': 'workspace 1, remote commit 1'},
        add_only=0,
        fast_forward=0
    )


def ls_changes():
    ws_1_local, ws_2_local, ws_1_remote, ws_2_remote = init()

    ws_1_local.set_file_pattern(ASSET_FILE_PATTERN)
    log_info('Listing changes')
    log_info(ws_1_local.ls_changes())


def add_only_commit():
    ws_1_local, ws_2_local, ws_1_remote, ws_2_remote = init()

    # Commit to local repo
    ws_1_local.set_file_pattern(ASSET_FILE_PATTERN)
    ws_1_local.commit(
        ['wip'],
        data={'message': 'workspace 1, local commit 2, add only'},
        add_only=1,
        fast_forward=0
    )

    # Commit to remote repo
    ws_1_remote.set_file_pattern(ASSET_FILE_PATTERN)
    ws_1_remote.commit(
        ['review'],
        data={'message': 'workspace 1, remote commit 2, add only'},
        add_only=0,
        fast_forward=0
    )


def checkout():
    ws_1_local, ws_2_local, ws_1_remote, ws_2_remote = init()

    ws_1_local.checkout('wip', ws_1_local.latest_revision('wip'))


def checkout_overwrite():
    ws_1_local, ws_2_local, ws_1_remote, ws_2_remote = init()

    ws_1_local.checkout('wip', ws_1_local.latest_revision('wip'), overwrite=1)


def checkout_custom_dir():
    ws_1_local, ws_2_local, ws_1_remote, ws_2_remote = init()

    ws_1_local.checkout(
        'wip',
        ws_1_local.latest_revision('wip'),
        checkout_dir=Path(_TEST_ROOT, 'checkout')
    )


def fast_forward_commit():
    ws_1_local, ws_2_local, ws_1_remote, ws_2_remote = init()

    # Commit to remote repo
    ws_2_remote.set_file_pattern(ASSET_FILE_PATTERN)
    ws_2_remote.commit(
        ['review'],
        data={'message': 'workspace 2, remote commit 1'},
        add_only=0,
        fast_forward=1
    )


if __name__ == '__main__':
    # init()
    # standard_commit()
    # ls_changes()
    # add_only_commit()
    # checkout()
    # checkout_overwrite()
    # checkout_custom_dir()
    # fast_forward_commit()
    pass
