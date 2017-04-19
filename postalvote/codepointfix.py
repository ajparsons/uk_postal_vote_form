'''
py2/py3 codepoint fixes
'''

from oscodepoint import CodePointZip, Metadata
import io, os
import six 

class FixedMeta(Metadata):

    def __init__(self, f):
        self['area_counts'] = {}
        for line, mode in self.line_modes(f):
            if mode == 'header':
                match = self.header_re.search(line)
                self[match.group(1)] = match.group(2)
            
            if mode == 'area_count':
                match = self.area_count_re.search(line)
                self['area_counts'][match.group(1)] = int(match.group(2))
        
        self['total_count'] = sum(six.itervalues(self['area_counts']))

class lazyproperty(object):
    def __init__(self, fget):
        self.fget = fget
    
    def __get__(self, obj, type=None):
        value = self.fget(obj)
        if six.PY2:
            setattr(obj, self.fget.func_name, value)
        else:
            setattr(obj, self.fget.__name__, value)
        return value

class CodePointZipFix(CodePointZip):
    
    def _open(self, name):
        zp = self.zip_file.open(name)    
        return io.TextIOWrapper(zp)

    def _get_metadata(self):
        return FixedMeta(self._open(self.metadata_name))
    
    @lazyproperty
    def metadata(self):
        return self._get_metadata()
    