import uuid
from pygear3 import global_v
import json
class AbstractItemBase():
    def __init__(self):
        pass
    def to_dict(self):
        dict = {}
        dict.update(self.__dict__)
        return dict
    def to_string(self):
        dict = {}
        dict.update(self.__dict__)
        return json.dumps(dict,ensure_ascii=False)
class RequestItem(AbstractItemBase):
    def __init__(self,Type,Content):
        super(RequestItem).__init__()
        self.ID = str(uuid.uuid4())
        self.Type = Type
        self.Channel = global_v.global_channel
        self.Token = global_v.global_token
        self.Content = Content


class LoginItem(AbstractItemBase):
    def __init__(self):
        super(LoginItem).__init__()
        self.GearID = ''
        self.GearUserName = ''
        self.GearPassword = ''
        self.GearNickName = ''
        self.GearPhone = ''
        self.GearType = ''
        self.GearCreateTime = ''
        self.GearOnline = ''
        self.GearLastOnline = ''
        self.GearDesc = ''
        self.GearProfile = ''
        self.GearGroupID = ''

class ActionItem(AbstractItemBase):
    def __init__(self):
        super(ActionItem).__init__()
        self.ActionName = ''
        self.limit = 0
        self.timeout = 0


class ReportDataItem(AbstractItemBase):
    def __init__(self,data_type,task_uid):
        super(ReportDataItem).__init__()
        self.TaskUID = task_uid
        self.Type = data_type
        self.ExpandTask = list()
        self.ContentData = list()
class GraphData(AbstractItemBase):
    def __init__(self,start_node,relation,end_node):
        super(GraphData).__init__()
        self.StartNode = start_node
        self.RelationShip = relation
        self.EndNode = end_node
class Node(AbstractItemBase):
    def __init__(self,label_name):
        super(Node).__init__()
        self.ExternInfo =dict()
        self.PrimaryKey = dict()
        self.LName = label_name
class Relationship(AbstractItemBase):
    def __init__(self,label_name):
        super(Relationship).__init__()
        self.ExternInfo = dict()
        self.PrimaryKey = dict()
        self.LName = label_name

class ExpandTask(AbstractItemBase):
    def __init__(self,type,value):
        super(GraphData).__init__()
        self.Type = start_node
        self.Value = value
