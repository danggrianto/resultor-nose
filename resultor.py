"""Plugin to send result to the resultor"""
from nose.plugins import Plugin
import json
import os
import requests
import time
import traceback


class Resultor(Plugin):
    name = 'resultor'

    def options(self, parser, env=os.environ):
        super(Resultor, self).options(parser, env=env)

    def configure(self, options, conf):
        super(Resultor, self).configure(options, conf)
        if not self.enabled:
            return

    def begin(self):
        self.results = []
        self.current_time = time.time()

    def startTest(self, test):
        self.result = {
            'name': test.id(),
            'module': test.context.__module__,
            'time': time.strftime('%d/%m/%Y %H:%M:%S')
        }

    def stopTest(self, test):
        self.results.append(self.result)
        current_time = time.time()
        self.result['duration'] = round(current_time - self.current_time, 2)
        self.current_time = current_time

    def addSuccess(self, test):
        self.result['status'] = 'pass'

    def addFailure(self, test, err):
        self.result['status'] = 'fail'
        self.result['trace'] = self.formatErr(err)

    def addError(self, test, err):
        self.result['status'] = 'fail'
        self.result['trace'] = self.formatErr(err)

    def finalize(self, result):
        headers = {'content-type': 'Content-Type:text/json'}
        uri = 'http://127.0.0.1:5000/api/result'
        requests.put(uri, data=json.dumps(self.results), headers=headers)

    def formatErr(self, err):
        """format error"""
        exctype, value, tb = err
        tr = traceback.format_exception(exctype, value, tb)
        return "".join(tr)
