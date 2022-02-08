class LoadError(Exception):
    pass

class mySQLError(Exception):
    pass

class httpError(Exception):
    pass

class APRSPackageError(Exception):
    pass

class PlaneLibArgumentError(Exception):
    pass

def version():
    return "errorhandlers.py: 1.0"
