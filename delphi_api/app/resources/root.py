import app.util.json as json


class RootResources(object):
    """
    Root endpoint that handles a GET request to the root: /

    Returns:
        "Hello, World!"
    """
    def on_get(self, req, resp):
        resp.body = json.dumps({
            "message": "Hello, World!",
        })


class RootNameResources(object):
    """
    Root endpoint that handles a POST message to the root: /

    Parameters:
        name
    """
    def on_post(self, req, resp, name):
        resp.body = json.dumps({
            "message": "Hello, {}!".format(name.capitalize())
        })
