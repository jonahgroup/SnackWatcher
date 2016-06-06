---
layout: post
title: 'Talking To Robots'
date: 2016-06-05 12:00:00.000000000 -05:00
permalink: 'talking-to-robots'
author: RJ Salvador
tags:
  - SnackWatcher
  - Slack
  - Marvin
  - Hubot
  - Bot
  - RESTful API
category: post
comments: true
cover: images/talking-to-robots/cover.jpg
---
<!--excerpt.start-->
Jonah Group’s implementation of SnackWatcher uses a Slack bot named Marvin. Marvin is a [Hubot](https://hubot.github.com/), and he offers a fun way for users to interact with the SW system.<!--excerpt.end--> Currently, Marvin offers two modes of operation:


__ACTIVE MODE__: Marvin allows users to ask for snack updates. Once a users asks Marvin about current snack levels, he asks SnackWatcher for a snapshot and sends the snack report to the chat dialog.

__PASSIVE MODE__: Every few minutes, Marvin will retrieve updates from SnackWatcher and send snack reports to users. The time interval can be adjusted by admins.

Would you like to know more about Marvin and his origins? Great!

## Hubot + Slack Integration
In order to start talking with robots, we had to integrate a Hubot with Slack. Thankfully, adding new integrations/configurations is super easy on Slack!

To set up a new Hubot integration, just hop in to your team's "Apps" menu and add a new Custom Integration:
![Hubot-Slack Integration Step 1]({{ site.baseurl }}/images/talking-to-robots/slack-integration-01-sm.jpg)

During setup, you'll see an API token like this:
![Hubot-Slack Integration Step 1]({{ site.baseurl }}/images/talking-to-robots/slack-integration-03-sm.jpg)

That API token is critical for letting your Hubot instance pester the right Slack team! For example, a script like this is used for starting up a Hubot:

```bash
HUBOT_SLACK_TOKEN=xoxb-3246845465-exampleApiToken5324 ./bin/hubot --adapter slack
```


## Hubot + SnackWatcher
Hubots can make HTTP requests, and this is how Marvin interacts with the SnackWatcher REST API.
This can be accomplished through code like so:

```coffeescript
    snackUpdate = ->
        robot.http('example.snackwatcher.net/api/snacks/snap')
            .header('User-Agent', 'Hubot Snack Watcher')
            .get() (err, res, body) ->
                returnObj = JSON.parse(body)
                robot.messageRoom 'snack_channel', 'Snack status:\n' + returnObj.img_url
```


## Active Mode
So how does Marvin understand when users want a snack update? He does it with the power of Regular expressions! For example, Marvin's ACTIVE MODE response to his hungry colleauges looks kinda like this:

```coffeescript
    robot.respond /(snack|snake)(\s+table)?/i, (msg) ->
        robot.messageRoom 'snack_channel', 'Please wait while I take a pic...'
        snackUpdate()
```

When Marvin hears something like "Snack table" or "SNACK TABLE NOW!!", he would immediately:

- reply to the snack watching channel
- request a status update from the SnackWatcher system
- send this update to the eagerly awaiting snack watcher


## Passive Mode

Marvin's PASSIVE MODE operation essentially does the same thing as his ACTIVE MODE, but has a time-based trigger. For that, we used a [hubot-cronjob](https://github.com/PavelVanecek/hubot-cronjob) package from NPM. That package is used like so:

```coffeescript
    HubotCron = require 'hubot-cronjob'
    CRON_PATTERN = '0 */15 9-17 * * 1-5'
    CRON_TIMEZONE = 'America/Toronto'

    # Initializing hubot's cron functions.
    new HubotCron CRON_PATTERN, CRON_TIMEZONE, snackUpdate()
```

The cron pattern roughly means:

> Every 15 minutes, from 9:00AM to 5:59PM during Mondays to Fridays

Yes, we love snacks. But not enough to watch themduring evenings and weekends...
