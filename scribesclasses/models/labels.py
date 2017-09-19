
from typing import Text, Optional, Dict, List
import github.Label

Color=Text
Name=Text
JsonLabelMap=Dict[Name, Color]

class Label(object):
    def __init__(self, repo, name, color, atGH=None):
        self.repository=repo  #type: 'Repository'
        self.repository.labelNamed[name]=self # backward reference
        self.name=name  #type: Name
        self.color=color #type: Color
        self.atGh=atGH #type: Optional[github.Label.Label]
        # set later when ensure label

class LabelConfig(object):
    def __init__(self, name, color):
        #type: (Name, Color)->None
        self.name=name
        self.color=color

def toLabelConfigList(jsonLabelMap):
    #type: (JsonLabelMap) -> List[LabelConfig]
    # Takes something like this as parameter
    #  {
    #       "Announcement": "eb6420",
    #       "Answered": "c03070",
    #       "Bug": "fc2929",
    #   },
    try:
        return [LabelConfig(name, color)
                for (name, color) in jsonLabelMap.items()]
    except Exception as e:
        raise ValueError('invalid label map: %s (%s)' % (
                            str(jsonLabelMap),
                            str(e)))



