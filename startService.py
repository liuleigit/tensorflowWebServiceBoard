# coding=utf-8

import tornado.ioloop
import tornado.web
import tornado.httpserver
import tornado.httpclient
import tornado.netutil
from tornado.options import define, options
import sys
import operator

class TfTest(tornado.web.RequestHandler):
    def get(self):
        #self.write('tensor flow test.')
        print("board get")
        http_client = tornado.httpclient.HTTPClient()
        try:
            response = http_client.fetch("http://10.172.64.2:9999/tf/test")
            #response = http_client.fetch("http://baidu.com")
            self.write("response :" + response.body)
            print ("body = "+response.body)
        except tornado.httpclient.HTTPError as e:
            print("Error: " + str(e))
        except Exception as e:
            print("error: "+ str(e))
        http_client.close()

class WordEmbeding(tornado.web.RequestHandler):
    def get(self):
        print("board word embeding.")
        w1 = self.get_argument("word1", None)
        w2 = self.get_argument("word2", None)
        w3 = self.get_argument("word3", None)
        http_client = tornado.httpclient.HTTPClient()
        try:
            req = "http://10.172.64.2:9999/tf/w2v?word1=%s&word2=%s&word3=%s" % (w1, w2, w3)
            print("req = " + req)
            response = http_client.fetch(req)
            self.write("board :" + response.body)
            print ("body = "+response.body)
        except tornado.httpclient.HTTPError as e:
            print("Error: " + str(e))
        except Exception as e:
            print("error: "+ str(e))
        http_client.close()
        
class FetchContent(tornado.web.RequestHandler):
    def get(self):
        type = self.get_argument('type', None)
        txt = self.get_argument('txt', None)
        http_client = tornado.httpclient.HTTPClient()
        try:
            req = "http://10.172.64.2:9999/ml/fetchContent?type=%s&txt=%s" % (type, txt)
            response = http_client.fetch(req)
            self.write(response)
        except tornado.httpclient.HTTPError as e:
            print("Error: " + str(e))
        except Exception as e:
            print("error: "+ str(e))
        http_client.close()

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/tf/test", TfTest),
            (r"/tf/w2v", WordEmbeding),
            (r"/ml/fetchContent", FetchContent)
        ]
        settings = {

        }
        tornado.web.Application.__init__(self, handlers, **settings)

if __name__ == "__main__":
    port = sys.argv[1]
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(port)
    tornado.ioloop.IOLoop.instance().start()
