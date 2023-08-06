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

from typing import Type
from puffotter.flask.Config import Config as BaseConfig


class Config(BaseConfig):
    """
    Configuration for the flask application
    """

    @classmethod
    def _load_extras(cls, parent: Type[BaseConfig]):
        """
        Loads non-standard configuration variables
        :param parent: The base configuration
        :return: None
        """
        parent.API_VERSION = "0"
        parent.STRINGS.update({
            "password_changed": "PaSsWoRd ChAnGeD SuCeSsFuLlY"
        })
