#!/usr/bin/python3

import io
import json
import pika
import sys
import uuid

import avro.schema
import avro.io

from avro.datafile import DataFileReader, DataFileWriter
from avro.io import DatumReader, DatumWriter

from urllib import request as urlreq

requestSchema  = avro.schema.Parse(open('basicRequest.avsc').read())
responseSchema = avro.schema.Parse(open('basicResponse.avsc').read())
D2ServerURL    = "http://172.27.25.236:4567/prashtis"

class PrashtiClient(object):
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
                host=getIPAddrFromD2()))

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(self.on_response, no_ack=True,
                                   queue=self.callback_queue)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, request):
        self.response = None
        self.corr_id  = str(uuid.uuid4())
        writer        = avro.io.DatumWriter(requestSchema)
        bytesWriter   = io.BytesIO()
        encoder       = avro.io.BinaryEncoder(bytesWriter)
        writer.write(request, encoder)
        self.channel.basic_publish(exchange='',
                                   routing_key='rpc_queue_prashti',
                                   properties=pika.BasicProperties(
                                         reply_to = self.callback_queue,
                                         correlation_id = self.corr_id,
                                         ),
                                   body=bytesWriter.getvalue())
        while self.response is None:
            self.connection.process_data_events()
        rawBytes    = self.response
        bytesReader = io.BytesIO(rawBytes)
        decoder     = avro.io.BinaryDecoder(bytesReader)
        reader      = avro.io.DatumReader(responseSchema)
        response    = reader.read(decoder)
        return response

def randomReqId():
    return str(uuid.uuid4().hex)

def getIPAddrFromD2():
    req = urlreq.urlopen(D2ServerURL)
    encoding = req.headers.get_content_charset()
    obj = json.loads(req.read().decode(encoding))
    return obj[0]['ipAddr']

