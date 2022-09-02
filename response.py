#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
import slackweb

now = datetime.now().strftime('%H:%M:%S - %Y.%m.%d')
print now
slack = slackweb.Slack(url='https://hooks.slack.com/services/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')
slack.notify(text='slackへ通知 %s' % now)
