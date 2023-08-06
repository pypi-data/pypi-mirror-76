from .dialogue_manager import DialogueManager
from .task_engine import TaskEngine
from .knowledge_graph import KnowledgeGraph
from .question_answering import QuestionAnswering
from .intent_answering import IntentAnswering
from .ner_parser import NERParser
from .set import Set


class Bot:
    """
    机器人
    """
    def __init__(self, app_id):
        self.app_id = app_id
        self.set = Set()
        self.intent = IntentAnswering(app_id,self.set)
        self.qa = QuestionAnswering(app_id,self.set)
        self.kg = KnowledgeGraph(app_id,self.set)
        self.te = TaskEngine(app_id,self.set)
        self.dm = DialogueManager(app_id,self.set)
        self.ner = NERParser(app_id,self.set)
