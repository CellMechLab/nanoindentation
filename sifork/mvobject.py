import configparser as ConfigParser
import logging
INIFILE = 'defaults.ini'
class mvobject(object):
    """
    abstract class to be extended. Provides file-based configuration utility
    """
    def parseConfig(self,defaults,section):
        """
        at startup, configure the object with defaults or file-read values
        NB: only values in the default dictionary are parsed
        """
        c = ConfigParser.SafeConfigParser()
        try:
            c.readfp(open(INIFILE))
        except:
            pass
        for k,v in defaults.items():
            if c.has_option(section,k):
                if type(v)==bool:
                    v = c.getboolean(section,k)
                elif type(v)==int:
                    v = c.getint(section,k)
                elif type(v)==float:
                    v = c.getfloat(section,k)
                else:
                    v = c.get(section,k)
            setattr(self,k,v)
