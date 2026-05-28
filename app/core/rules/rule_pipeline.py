class RulePipeline:

    def __init__(self, rules):

        self.rules = rules

    def process(self, text):

        result = text

        for rule in self.rules:

            result = rule.apply(result)

        return result