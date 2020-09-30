from .utility import getCurrentTime, jsonDump

class CustomLogger():
    logs = []
    errors = 0
    warnings = 0
    infos = 0
    startTime = getCurrentTime()
    stopTime =  getCurrentTime()
    def addLogs(self, label, text):
        time = getCurrentTime()
        self.logs.append({
            'time': time,
            'label': label,
            'text': text
        })
        self.stopTime = time

    def error(self, text):
        self.errors += 1
        self.addLogs('ERROR', text)

    def warning(self, text):
        self.warnings += 1
        self.addLogs('WARNING', text)

    def info(self, text):
        self.infos += 1
        self.addLogs('INFO', text)

    def printLog(self, spider):
        text = 'JOB DONE\n\n\n'
        text += 'Started at: ' + self.startTime + '\n'
        text += 'Finished at: ' + self.stopTime + '\n'
        text += 'Errors found: ' + str(self.errors) + '\n'
        text += 'Warnings at: ' + str(self.warnings) + '\n\n\n\n'
        for log in self.logs:
            text += log['time'] + '  (' + log['label'] + '):  ' + log['text'] + '\n\n\n'
        text += 'Summary stats: \n\n' + jsonDump(spider.crawler.stats.get_stats()) + '\n'
        text += '\n\nThanks'
        return text


customLogger = CustomLogger()
