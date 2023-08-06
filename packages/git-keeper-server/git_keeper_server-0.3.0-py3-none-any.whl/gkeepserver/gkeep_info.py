# Copyright 2016 Nathan Sommer and Ben Coleman
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
import json
from getpass import getuser

from gkeepcore.faculty_class_info import FacultyClassInfo
from gkeepcore.gkeep_exception import GkeepException
from gkeepcore.path_utils import user_gitkeeper_path, faculty_info_path
from gkeepcore.shell_command import run_command


class GkeepInfoException(GkeepException):
    pass


def main():
    username = getuser()
    gitkeeper_path = user_gitkeeper_path(username)
    info_path = faculty_info_path(gitkeeper_path)

    cmd = 'echo | cat {0}/`ls {0} | tail -1`'.format(info_path)

    try:
        info_json = run_command(cmd)
        info = json.loads(info_json)
    except Exception as e:
        raise GkeepInfoException('Error loading info from JSON: {}'
                                 .format(e))

    print(info)

    info = FacultyClassInfo(info)

