from .module import Module
from ..caller.parser_caller import NERParserCaller

class PredictAnswer:
    def __init__(self, slot_content, slot_name, slot_desc):
        self.slot_content = slot_content
        self.slot_name = slot_name
        self.slot_desc = slot_desc

class NERParser(Module):

    def __init__(self, app_id,set):
        super().__init__(app_id, 'ner',set)
        self.app_id = app_id
        self.caller = NERParserCaller(app_id)
        self.caller.register_tde_user(app_id)

    def predict(self, sentence, parser: str):
        results = self.caller.predict(sentence, parser)
        answers = []
        if results:
            for result in results:
                answers.append(PredictAnswer(result['slotContent'], result['slotName'], result['slotDesc']))
        return answers

    def predicts(self, sentence, parsers: list):
        answers = []
        for parser in parsers:
            results = self.predict(sentence, parser)
            if results is not None:
                answers.extend(results)

        return answers
