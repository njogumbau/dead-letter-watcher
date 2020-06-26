
class TriggeredAlert:
    def __init__(self, alert):
        self.alert = alert

    def get_deadletter_metric_value(self):
        condition = self.alert['data']['alertContext']['condition']
        for x in condition['allOf']:
            return x['metricValue']
            

    def get_service_bus_queue(self):
        condition = self.alert['data']['alertContext']['condition']
        for x in condition['allOf']: 
            if x['metricName'] == "DeadletteredMessages":
                for dimension in x['dimensions']:
                    if dimension['name'] == 'EntityName':
                        return dimension['value']
    
    def get_service_bus_name(self):
        return self.alert['data']['essentials']['alertTargetIDs'][0]

    def get_fired_datetime(self):
        return self.alert['data']['essentials']['firedDateTime']


