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
        self.send_result(self.result)

    def addSuccess(self, test):
        self.result['status'] = 'pass'

    def addFailure(self, test, err):
        self.result['status'] = 'fail'
        self.result['trace'] = self.formatErr(err)
        try:
            browser = test.test.browser
            self.result['screenshot'] = 'data:image/png;base64,{0}'\
                .format(browser.get_screenshot_as_base64())
        except AttributeError:
            pass

    def addError(self, test, err):
        try:
            self.result['status'] = 'fail'
            self.result['trace'] = self.formatErr(err)
            browser = test.test.browser
            self.result['screenshot'] = 'data:image/png;base64,{0}'\
                .format(browser.get_screenshot_as_base64())
        except Exception:
            pass

    def send_result(self, result):
        headers = {'content-type': 'Content-Type:text/json'}
        host = os.environ.get('RESULTOR_HOST')
        if host:
            uri = 'http://{0}/api/result'.format(host)
            requests.put(uri, data=json.dumps([result]), headers=headers)

    def formatErr(self, err):
        """format error"""
        exctype, value, tb = err
        tr = traceback.format_exception(exctype, value, tb)
        return "".join(tr)
