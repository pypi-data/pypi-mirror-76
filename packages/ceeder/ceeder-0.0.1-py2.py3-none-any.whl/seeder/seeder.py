#!/usr/bin/env python3

import sys
import os
import logging
import json

import falcon

from abc import ABC, abstractmethod


class Annotator(ABC):
    '''Annotator is a falcon-based "analytic".

    Implementations must implement one methods:

    on_post(request, response)

    Implementations can also override on_get(req, resp)
    in order to implement custom health check behavior.
    '''

    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200  # This is the default status
        resp.media = {'status': 'ok'}


    @abstractmethod
    def on_post(self, req, resp):
        pass


    def create(self,
               health_endpoint='/api/v1/health',
               post_endpoint='/api/v1/annotate/cdr',
    ):
        app = falcon.API()
        app.add_route(health_endpoint, self)
        app.add_route(post_endpoint, self)
        return app


class TagAnnotator(Annotator):
    '''TagAnnotator takes in a function that produces CDR annotation tags.

    It uses this function in the on_post method in order to more easily
    create a tag analytic by handling the web/framework parts. As a result,
    in order to implement a new tag analytic, one just needs to pass in
    an annotate_function that produces the right CDR tag output.
    '''
    def __init__(self,
                 annotate_function,
                 label,
                 annotator_type='tags',
                 version='0.0.1',
    ):
        self.annotate_function = annotate_function
        self.label = label
        self.annotator_type = annotator_type
        self.version = version


    def on_post(self, req, resp):
        request_json = req.media
        txt = request_json['extracted_text']
        logging.debug('incoming text: {}'.format(txt))
        output = {}
        output['content'] = self.annotate_function(txt)
        output['type'] = "tags"
        output['label'] = self.label
        output['version'] = self.version
        resp.media = output
