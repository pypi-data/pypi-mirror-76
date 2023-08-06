"""LICENSE
Copyright 2020 Hermann Krumrey <hermann@krumreyh.com>

This file is part of fat-ffipd.

fat-ffipd is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

fat-ffipd is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with fat-ffipd.  If not, see <http://www.gnu.org/licenses/>.
LICENSE"""

# noinspection PyProtectedMember
from puffotter.flask.test.TestFramework import _TestFramework \
    as __TestFrameWork
from fat_ffipd import root_path
from fat_ffipd.Config import Config
from fat_ffipd.routes import blueprint_generators
from fat_ffipd.db import models


class _TestFramework(__TestFrameWork):
    """
    Class that models a testing framework for the flask application
    """
    module_name = "fat_ffipd"
    root_path = root_path
    config = Config
    models = models
    blueprint_generators = blueprint_generators
