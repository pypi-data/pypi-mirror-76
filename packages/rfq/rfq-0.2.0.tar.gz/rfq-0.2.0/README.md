<h1 align='center'>rfq</h1>

<p align=center>
  Simple language-agnostic message queues: tools, conventions, examples
  <img src="assets/rfq.png" />
</p>

## Table of Contents

1. [Overview](#overview)
2. [Usage](#usage)
    - [list-topics](#list-topics)
    - [list-queue](#list-queue)
    - [purge-queue](#purge-queue)
    - [publish](#publish)
    - [consume](#consume)
    - [harvest](#harvest)
3. [Development](#development)
4. [License](#license)


## Overview

Implementing a reliable message queue with redis is possible but has to follow certain [best practices](https://redis.io/commands/rpoplpush#pattern-reliable-queue).
The goal of this project is to provide a simple reliable message queue on top of redis while following best practices and capturing conventions as code.
See [rfq.js](https://github.com/robofarmio/rfq.js) for a simple Javascript/Typescript integration.

The following describes how to use rfq as a library or as a set of command line tools while [design.md](./design.md) describes the low level design.


## Usage

The following shows library functionality in terms of their command line wrappers.

The command line tool and library can be configured by setting the environment variables

    export RFQ_REDIS_HOST=localhost
    export RFQ_REDIS_PORT=6397

for the default redis host and port when not providing a custom redis instance.


### list-topics

List all active topics

    rfq list-topics
    ndvi


### list-queue

List messages in the backlog (work not yet started)

    rfq list-queue --topic 'ndvi'
    eeba0c1642ab11eaa480a4c3f0958f5d
    ede1296442ab11eabdb9a4c3f0958f5d

List messages in the nextlog (work started but not yet committed)

    rfq list-queue--topic 'ndvi' --queue nextlog
    eeba0c1642ab11eaa480a4c3f0958f5d


### purge-queue

Deletes messages in a queue

    rfq purge-queue --topic 'ndvi'
    eeba0c1642ab11eaa480a4c3f0958f5d
    ede1296442ab11eabdb9a4c3f0958f5d


### publish

Publish messages to a topic

    rfq publish --topic 'ndvi' --message '{ "tile": "T32UNE" }'
    eeba0c1642ab11eaa480a4c3f0958f5d
    rfq publish --topic 'ndvi' --message '{ "tile": "T33UVU" }'
    ede1296442ab11eabdb9a4c3f0958f5d

Note: messages and are a flat map of key-value pairs, see [issue/1](https://github.com/robofarmio/rfq/issues/1)


### consume

Consume a message, working on it (dummy sleep), then commit the message when done

    rfq consume --topic 'ndvi'
    { "tile": "T32UNE" }


### harvest

Harvest messages from the nextlog back into the backlog

    rfq harvest --topic 'ndvi'
    eeba0c1642ab11eaa480a4c3f0958f5d

Note: messages end up in the nextlog when workers start processing but haven't committed them yet.


## Development

For development

    make

    make run
    $ rfq --help

    $ exit
    make down

Or run the commands directly from the docker container with

    docker run -e RFQ_REDIS_HOST=MyRedisHost robofarm/rfq --help


## License

Copyright © 2020 robofarm

Distributed under the MIT License (MIT).
