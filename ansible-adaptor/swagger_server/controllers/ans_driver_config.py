"""
reads config file for the ansible resource manager driver

IBM Corporation, 2017, jochen kappel
"""
import os
import yaml
from flask import current_app as app

class ConfigReader:
    """
    singleton to read and cache configuration
    """
    class __ConfigReader:
        """
        inner singleton class
        """
        def __init__(self):
            try:
                with open("./config.yml", 'r') as ymlfile:
                    cfg = yaml.load(ymlfile)
            except FileNotFoundError:
                app.logger.critical('configuration file config.yml not found')
                raise FileNotFoundError

            app.logger.info('loading configuration')
            self.driver_name = cfg['driver']['name']
            self.driver_version = cfg['driver']['version']
            self.requests_ttl = cfg['cassandra']['ttl']

            self.resource_dir = cfg['ansible']['resource_dir']
            app.logger.debug('check for resource folder: ' + self.resource_dir)
            # check if configured directory exists:
            if not os.path.isdir(self.resource_dir):
                app.logger.warning('resource folder ' + self.resource_dir + ' does not exist')
                app.logger.info('creating resource folder ' + self.resource_dir)
                os.mkdir(self.resource_dir)

            self.keys_dir = cfg['ansible']['keys_dir']
            app.logger.debug('check for keys folder: ' + self.keys_dir)
            # check if configured directory exists:
            if not os.path.isdir(self.keys_dir):
                app.logger.warning('keys folder ' + self.keys_dir + ' does not exist')
                app.logger.info('creating keys folder ' + self.keys_dir)
                os.mkdir(self.keys_dir)


            self.supported_features = cfg['driver']['supportedFeatures']
            self.supported_api_version = cfg['driver']['supportedApiVersions']
            self.supported_properties = cfg['driver']['properties']

        def getDriverNameVersion(self):
            """ get driver name and version """
            return self.driver_name, self.driver_version

        def getDriverName(self):
            """ get driver name """
            return self.driver_name

        def getDriverVersion(self):
            """ get driver version """
            return  self.driver_version

        def getResourceDir(self):
            """ get resource directory """
            return self.resource_dir

        def getKeysDir(self):
            """ get keypair directory """
            return self.keys_dir

        def getDriverProperties(self):
            """ get driver properties """
            return self.supported_properties

        def getSupportedFeatures(self):
            """ get supported features """
            return self.supported_features

        def getSupportedApiVersions(self):
            """ get supported ALM API version """
            return self.supported_api_version

        def getTTL(self):
            """ get time to live for request records """
            return self.requests_ttl

    instance = None

    def __init__(self):
        if not ConfigReader.instance:
            ConfigReader.instance = ConfigReader.__ConfigReader()

    def __getattr__(self, name):
        return getattr(self.instance, name)