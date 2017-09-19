from typing import List, Tuple
import github.Label
from datetime import datetime
from scribesclasses.models.configurations import (
    toDateTime
)


from typing import Optional, Text
import github.Milestone

Date=Text
JsonMilestonList=List[Tuple[Text, Text, Text]]

class Milestone(object):
    def __init__(self, repo, title, description, dueOn, atGH=None):
        self.repository=repo  #type: 'Repository'
        self.repository.milestoneEntitled[title]=self # backward reference
        self.title=title
        self.description=description #type: Text
        self.dueOn=dueOn #type: datetime
        self.atGH=atGH #type: Optional[github.Milestone.Milestone]
        # set later when ensure milestone


class MilestoneConfig(object):
    def __init__(self, title, description, dueOn):
        #type: (Text, Text, datetime) -> None
        self.title=title
        self.description=description
        self.dueOn=dueOn

def toMilestoneConfigList(milestoneList):
    #type: (JsonMilestonList) -> List[MilestoneConfig]
    # Takes something like this as parameeter
    #   [
    #       ["M1","End of first phase", "21/12/2015"],
    #       ["M2","Early delivery","31/03/2019"]
    #   ]
    try:
        return [
            MilestoneConfig(
                title,
                desc,
                toDateTime(due_on))
                for (title, desc, due_on) in milestoneList]
    except Exception as e:
        raise ValueError('invalid milestone list: %s (%s)' % (
                            str(milestoneList),
                            str(e)))