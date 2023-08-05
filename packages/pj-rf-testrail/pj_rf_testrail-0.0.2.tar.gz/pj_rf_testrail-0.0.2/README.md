RobotTestRailUpdate
===============

Update Test Rail execution status using Robot Framework.

Installation
------------

The recommended installation method is pip:

    pip install robotframework-notifications

Running this command installs also the latest version of Requests

Import Library
-----

To use RobotSlackNotifications in Robot Framework, the library needs to be imported using the ``Library`` setting as any other library. The library needs the webhook url from Slack or Mattermost as an argument.

You can retrieve this webhook url in Slack or Mattermost.

Slack

> https://slack.com/intl/en-lv/help/articles/115005265063-incoming-webhooks-for-slack

Mattermost

>  https://docs.mattermost.com/developer/webhooks-incoming.html#simple-incoming-webhook 

Usage
-----

Import library then add it on the listener during Robot Framework test run.