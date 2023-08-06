__version__ = '0.3.1'

from .management import (archive, zip_contents)
from .prj import (Project, setup, qs, get_prj, set_delete_sys_path_index)

from .deprecated import (find_paths)

__all__ = ['archive', 'zip_contents', 'Project', 'setup', 'qs', 'get_prj', 'set_delete_sys_path_index']
