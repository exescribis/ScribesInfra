from typing import Text, Optional
import github.NamedUser

class Member(object):

    def __init__(self,
                 team,
                 login,
                 email,
                 atGH,
                 firstName=None,
                 lastName=None,
                 trigram=None):
        #type: ('Team', Text, Text, github.NamedUser.NamedUser, Optional[Text], Optional[Text], Optional[Text]) -> None
        self.team=team
        self.team.memberByLogin[login]=self # backward
        self.firstName=firstName
        self.lastName=lastName
        self.trigram=trigram
        self.login=login
        self.email=email
        self.atGH=atGH