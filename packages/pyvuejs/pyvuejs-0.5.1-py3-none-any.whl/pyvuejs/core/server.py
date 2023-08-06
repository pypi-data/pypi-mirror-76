# -*- coding: utf-8 -*-
import os, signal
from threading import Thread
from bottle import route, get, post, run, response, request, json_dumps, redirect
from bottle_websocket import GeventWebSocketServer

from ._loaders import load_project
from ..static import static_dir
from ..webview import WebViewUtils, start as webview_start

class Server():
    def __init__(self, project_dir:str):
        self.__project_dir = project_dir
        apps, components, self.__options = load_project(project_dir)

        @get("/server/state")
        def send_server_state():
            return json_dumps({ "state": True })

        @route("/static/<static_file>")
        def get_static_file(static_file:str):
            file_ext = os.path.splitext(static_file)[1][1:]
            static_file = os.path.join(static_dir, static_file)

            if os.path.exists(static_file):
                if file_ext == "ico":
                    response.set_header("Content-type", "image/x-icon")
                    return open(static_file, "rb").read()
                elif file_ext == "js":
                    response.set_header("Content-type", "text/javascript")
                else:
                    response.set_header("Content-type", "text/{}".format(file_ext))

                return open(static_file, "r", encoding = "utf-8").read()
            else:
                return "static files: " + ", ".join(os.listdir(static_dir))

        @get("/public/<public_file>")
        def get_project_public_file(public_file:str):
            file_ext = os.path.splitext(public_file)[1][1:]
            public_file = os.path.join(project_dir, "public", public_file)

            if os.path.exists(public_file):
                if file_ext == "ico":
                    response.set_header("Content-type", "image/x-icon")
                    return open(public_file, "rb").read()
                elif file_ext == "js":
                    response.set_header("Content-type", "text/javascript")
                else:
                    response.set_header("Content-type", "text/{}".format(file_ext))

                return open(public_file, "r", encoding = "utf-8").read()
            else:
                return "public files: " + ", ".join(os.listdir(os.path.join(project_dir, "public")))

        @get("/apps/default_webview")
        def fn_redirect_from_webview():
            redirect(f"/apps/{list(apps.keys())[0]}")

        @get("/apps/<app_url>")
        def fn_get_vue_render(app_url:str):
            response.set_header("content-type", "text/html")
            return apps[app_url].render()

        @get("/apps/<app_url>/init")
        def fn_init_vue_app(app_url:str):
            return json_dumps({
                "data": apps[app_url]._data,
                "methods": apps[app_url]._methods,
                "components": {
                    component.name: {
                        "props": component.props,
                        "template": component.template,
                        "style": component.style
                    }
                    for component in components
                }
            })

        @get("/apps/<app_url>/data/get")
        def fn_send_data_to_vue(app_url:str):
            return json_dumps({ "data": apps[app_url]._data })

        @post("/apps/<app_url>/data/set")
        def fn_get_data_from_vue(app_url:str):
            req = request.json

            for name, value in req["data"].items():
                apps[app_url].set_data(name, value)

        @post("/apps/<app_url>/method")
        def fn_call_vue_method(app_url:str):
            req = request.json

            apps[app_url].call_method(req["method"])
            return json_dumps({ "state": "success" })

    def __start(self, host:str, port:int):
        run(
            host = host, port = port,
            quiet = True,
            server = GeventWebSocketServer
        )

    # pyvuejs -> pvuejs -> 047372 -> 47372
    def start(self, host:str = None, port = None, wait_server:bool = True):
        if host == None:
            host = self.__options["host"]

        if port == None:
            port = self.__options["port"]

        Thread(target = self.__start, args = (host, port), daemon = True).start()

        if wait_server:
            try:
                while True:
                    pass
            except KeyboardInterrupt:
                self.__class__.stop()

        return host, port

    def start_standalone(self, default_app:str = None, host:str = None, port = None, width:int = 950, height:int = 650):
        if default_app == None:
            default_app = "default_webview"

        host, port = self.start(host, port, False)

        WebViewUtils.create_window(
            os.path.basename(self.__project_dir), f"http://127.0.0.1:{port}/apps/{default_app}",
            width = width, height = height
        )

        webview_icon = os.path.join(self.__project_dir, "public", "favicon.png")
        if not os.path.exists(webview_icon):
            webview_icon = os.path.join(static_dir, "favicon.png")

        webview_start(webview_icon)
        self.__class__.stop()

    @staticmethod
    @route("/stop")
    def stop():
        os.kill(os.getpid(), signal.SIGTERM)
