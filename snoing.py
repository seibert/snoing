#!/usr/bin/env python
# Author P G Jones - 12/05/2012 <p.g.jones@qmul.ac.uk> : First revision
# SNO+ package manager
import PackageManager
import os
import inspect
import PackageUtil
import Rat
import Log
import Util

class snoing( PackageManager.PackageManager ):
    """ The package manager for sno+."""
    def __init__( self, options ):
        """ Initialise the snoing package manager."""
        import sys
        super( snoing, self ).__init__()
        Util.CheckSystem()
        PackageUtil.kCachePath = Util.BuildDirectory( options.cachePath )
        PackageUtil.kInstallPath = Util.BuildDirectory( options.installPath )
        Log.kInfoFile = Log.LogFile( os.path.join( PackageUtil.kInstallPath, "README.md" ), True )
        Log.kInfoFile.Write( "## SNOING\nThis is a snoing install directory. Please alter only with snoing at %s" % __file__ )
        # Set the local details file
        Log.kDetailsFile = Log.LogFile( os.path.join( os.path.dirname( __file__ ), "snoing.log" ) )
        # Now check the graphical option is compatible with install directory
        snoingSettingsPath = os.path.join( PackageUtil.kInstallPath, "snoing.pkl" )
        graphical = Util.DeSerialise( snoingSettingsPath )
        if graphical is not None and graphical != options.graphical:
            raise Exception( "Install path chosen is marked as graphical = %s" % (not options.graphical ) )
        PackageUtil.kGraphical = options.graphical
        Util.Serialise( snoingSettingsPath, options.graphical )
        # First import all register all packages in the versions folder
        self.RegisterPackagesInDirectory( os.path.join( os.path.dirname( __file__ ), "versions" ) )
        # Now set the username password for the rat packages
        for package in self._Packages:
            if isinstance( self._Packages[package], Rat.RatRelease ):
                self._Packages[package].SetUsernamePassword( options.username, options.password )
        

if __name__ == "__main__":
    import optparse
    # Load defaults from file
    defaultFilePath = os.path.join( os.path.dirname( __file__ ), "settings.pkl" )
    defaults = Util.DeSerialise( defaultFilePath )
    if defaults is None: # No defaults
        defaults = { "cache" : "cache", "install" : "install" }
    parser = optparse.OptionParser( usage = "usage: %prog [options] [package]", version="%prog 1.0" )
    parser.add_option( "-c", type="string", dest="cachePath", help="Cache path.", default=defaults["cache"] )
    parser.add_option( "-i", type="string", dest="installPath", help="Install path.", default=defaults["install"] )
    parser.add_option( "-g", action="store_true", dest="graphical", help="Graphical install?" )
    parser.add_option( "-q", action="store_true", dest="query", help="Query Package Status?" )
    parser.add_option( "-d", action="store_true", dest="dependency", help="Dependencies only?" )
    parser.add_option( "-v", action="store_true", dest="verbose", help="Verbose Install?", default=False )
    parser.add_option( "-u", type="string", dest="username", help="Github username (for rat releases)" )
    parser.add_option( "-p", type="string", dest="password", help="Github password (for rat releases)" )
    (options, args) = parser.parse_args()
    # Save the defaults to file
    defaults["cache"] = options.cachePath
    defaults["install"] = options.installPath
    Util.Serialise( defaultFilePath, defaults )
    # Construct snoing installer
    Log.Header( "Registering Packages" )
    PackageUtil.kVerbose = options.verbose
    installer = snoing( options )
    if len(args) == 0:
        #Do something to all packages
        if options.query == True:
            Log.Header( "Checking all packages" )
            for packageName in installer.PackageNameGenerator():
                installer.CheckPackage( packageName )
        else:
            Log.Header( "Installing all packages" )
            for packageName in installer.PackageNameGenerator():
                installer.InstallPackage( packageName )
    else:
        if options.query == True:
            Log.Header( "Checking %s package" % args[0] )
            installer.CheckPackage( args[0] )
        elif options.dependency == True:
            Log.Header( "Installing %s package dependencies" % args[0] )
            installer.InstallPackageDependencies( args[0] )
        else: 
            Log.Header( "Installing %s package" % args[0] )
            installer.InstallPackage( args[0] )
