"""
    Sitecheck Module 

    This module represents the automated controller for Daily Sitechecks.
    
    Projects are read from 'project.ini', and feed into the Scanner module to 
    gather sensor data on when sensors were last updated.
    Once the data is gathered, It is Fed into the adaptivecards module and 
    queued to post to teams.
"""
# __name__ = 'sitecheck'
# __author__ = 'Dan Edens'

import os
import sys

os.environ['ROOT_DIR'] = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.environ['ROOT_DIR'])
