from binary_vcs_lite.common.util import *


class Blob(object):
    """Manage data blob.

    Blob does not care about anything except following info::

        blob_dir (str or Path):
        workspace_hash (common.hashing.WorkspaceHash):

    These data are processed and given to Blob by Workspace and Repo

    Attributes:
        _blob_dir (Path):

    Properties:
        blob_dir (Path):

    """

    def __init__(self, blob_dir):
        """
        Args:
            blob_dir (str or Path): A folder store blob data

        """

        super(Blob, self).__init__()
        self._blob_dir = Path(blob_dir)

    @property
    def blob_dir(self):
        """Path: """
        return self._blob_dir

    def _parse_hash(self, hash_value):
        """Parse blob sub folder and blob file name from hash.

        Args:
            hash_value (str): 40-char string digest

        Returns:
            2-tuple: (sub_folder_name, blob_file_name)

        """

        return (hash_value[:2], hash_value[2:])

    def store_blob(self, workspace_hash, verbose=0):
        """Put files in working dir to blob.

        Args:
            workspace_hash (common.hashing.WorkspaceHash):

        """

        log_info('Preparing to store blob...')

        path_pair = []
        for v in workspace_hash.values():
            sub_folder, blob_name = self._parse_hash(v['hash'])
            blob_file = self._blob_dir.joinpath(sub_folder, blob_name)
            workspace_file = Path(v['absolute_path'])
            if workspace_file.exists():
                path_pair.append((workspace_file, blob_file))
                if verbose:
                    log_info('Stored blob: {}/{}'.format(
                        sub_folder,
                        blob_name
                    ))
                    log_info('----{}'.format(str(workspace_file)))

        copied = batch_copy(path_pair, verbose=verbose)
        log_info('Stored all blobs')
        return copied

    def extract_blob(self, workspace_hash, verbose=0):
        """Extract files from blob to working dir.

        Args:
            workspace_hash (common.hashing.WorkspaceHash):

        """

        log_info('Preparing to extract blob...')

        path_pair = []
        for v in workspace_hash.values():
            sub_folder, blob_name = self._parse_hash(v['hash'])
            blob_file = self._blob_dir.joinpath(sub_folder, blob_name)
            workspace_file = Path(v['absolute_path'])
            if blob_file.exists():
                path_pair.append((blob_file, workspace_file))
                if verbose:
                    log_info('Extracted blob: {}/{}'.format(
                        sub_folder,
                        blob_name
                    ))
                    log_info('----{}'.format(str(workspace_file)))

        copied = batch_copy(path_pair, overwrite=1, verbose=verbose)
        log_info('Extracted all blobs')
        return copied
