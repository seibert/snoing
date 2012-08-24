#!/usr/bin/env python
# Author P G Jones - 24/08/2012 <p.g.jones@qmul.ac.uk> : First revision
# Text logger class, print logging information to the screen
import Logger

HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
END = '\033[0m'

class TextLogger(Logger.Logger):
    """ Update with pacakages state change information, and convey information to the
    screen in different colours :).
    """

    def __init__(self, local, install):
        """ Call the base class init."""
        super(TextLogger, self).__init__(local, install)

    def package_registered(self, package_name):
        """ Notify that a package has been registered."""
        print HEADER + ("Package %s registered." % package_name) + END
        super(TextLogger, self).package_registered(package_name)

    def package_downloaded(self, package_name):
        """ Notify that a package has been downloaded."""
        print OKBLUE + ("Package %s downloaded." % package_name) + END
        super(TextLogger, self).package_downloaded(package_name)

    def package_installed(self, package_name):
        """ Notify that a package has been installed."""
        print OKGREEN + ("Package %s installed." % package_name) + END
        super(TextLogger, self).package_installed(package_name)

    def package_removed(self, package_name):
        """ Notify that a package has been removed."""
        print WARNING + ("Package %s removed." % package_name) + END
        super(TextLogger, self).package_removed(package_name)

    def package_updated(self, package_name):
        """ Notify that a package has been updated."""
        print OKGREEN + ("Package %s updated." % package_name) + END
        super(TextLogger, self).package_updated(package_name)

    def info(self, info_message):
        """ Output some information."""
        print info_message
        super(TextLogger, self).info(info_message)

    def error(self, error_message):
        """ Notify that an error has occurred."""
        print FAIL + error_message + END
        super(TextLogger, self).error(error_message)
