

from typing import Text, List, Any, Optional, Union, Callable, Dict
import datetime
import os

from scribesclasses import load_json

JsonVal=[Text, List['JsonVal'], Dict[Text, 'JsonVal']]
ConvertFun=Callable[JsonVal, Any]

def toBool(s):
    if s=='True':
        return True
    elif s=='False':
        return False
    else:
        raise ValueError('"True" or "False" expected. "%s" found' % s)

def toText(s):
    return s

def toInt(s):
    try:
        return int(s)
    except:
        raise ValueError('Integer expected. "%s" found' % s)

def toDateTime(s):
    try:
        return datetime.datetime.strptime(s, "%d/%m/%Y")
    except:
        raise ValueError('Date expected. "%s" found.' % s )


class Configuration(object):

    def __init__(self, configurationFile):
        self.filename = configurationFile
        self._info = load_json(self.filename)

    @property
    def basename(self):
        return os.path.basename(self.filename)

    def param(self, pathOrName, default=None, err=None, f=toText):
        #type: (Union[List[Text], Text], Any, Optional[Any], ConvertFun) -> Any
        def _item(tree, path):
            if path==[]:
                return tree
            if path[0] not in tree:
                if err is not None:
                    raise ValueError(
                        '%s must define %s' % (
                            self.filename,
                            '.'.join(pathOrName)))
                else:
                    return default
            else:
                text_val=_item(tree[path[0]], path[1:])
                try:
                    val=f(text_val)
                    return val
                except ValueError as e:
                    if err is not None:
                        # improvz
                        raise ValueError(  #TODO: add the path to message
                            'Error in %s: %s' % (
                                self.basename,
                                str(e)))
                    else:
                        return default


        initpath=(
            [pathOrName] if isinstance(pathOrName, basestring)
            else pathOrName)
        return _item(
            self._info,
            initpath
        )

    def choice(self, value, pathOrName, default=None, err=None, f=toText):
        #type: (Any, Union[List[Text], Text], Any, Optional[Any]) -> Any
        return (
            value if value is not None
            else self.param(pathOrName, default=default, err=err, f=f)
        )
