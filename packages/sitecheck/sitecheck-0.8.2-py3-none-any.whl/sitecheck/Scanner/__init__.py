"""
    Geo-Instruments
    Sitecheck Scanner

    CLI entry point and function pool
"""
# __name__ = 'Scanner'
# __author__ = "Dan Edens"
# __url__= "https://geodev.geo-instruments.com/DanEdens/Sitecheck_Scanner"


import os
import sys

from sitecheck.Scanner.scanner import config
from sitecheck.Scanner.scanner import options
from sitecheck.Scanner.scanner import utlis

logger = utlis.make_logger('root')
ROOT_DIR = os.environ['ROOT_DIR']
projects = config.read_config_file()


async def Scan():
    """
    Invoke to Scan all projects marked with "skip = false" in projects.ini
    """
    from sitecheck.Scanner.scanner import projecthandler

    print(f"{sys.argv}")
    logger.debug(f'\n{utlis.projects_table(config.read_config_file())}')
    [await (projecthandler.run_controller(project)) for project in
     projects.sections()]
    logger.info('\nScan completed.')


def edit():
    """
    Edits project config file
    """
    if options.Edit:
        config.edit_project()


def enable_all_projects():
    """
    Quick reset of all projects to skip = false
    """
    if options.EnableAll:
        for each in projects.sections():
            config.edit_config_option(each, 'skip', 'false')
