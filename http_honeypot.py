import argparse
import base64
import os
import shutil
import urllib.parse
from mimetypes import guess_type
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
from twisted.internet import reactor
from twisted.python import log
from twisted.web import resource, server

script_dir = os.path.dirname(os.path.abspath(__file__))
index_file_path = os.path.join(script_dir, 'index.html')

class SimpleHTTPResource(resource.Resource):
    isLeaf = True

    def __init__(self, server):
        self.server = server
        self.current_url = server.url

    def render_GET(self, request):
        request.setHeader(b"Server", self.server.server_banner.encode())
        return self.serve_page(request)

    def render_POST(self, request):
        request.setHeader(b"Server", self.server.server_banner.encode())
        post_content = self.extract_post_content(request)
        self.log_request(request, post_content)
        return self.serve_page(request)

    def serve_page(self, request):
        requested_path = request.path.decode()
        requested_url = self.current_url if requested_path == '/' else urllib.parse.urljoin(self.current_url, requested_path)

        try:
            self.server.download_and_modify_html(requested_url)
            self.current_url = requested_url
            with open(index_file_path, 'rb') as file:
                return file.read()
        except Exception as e:
            log.msg(f"Error processing requested URL {requested_url}: {e}")
            with open(index_file_path, 'rb') as file:
                return file.read()

    def extract_post_content(self, request):
        request.content.seek(0)
        content = request.content.read()
        try:
            content_str = content.decode()
            return urllib.parse.parse_qs(content_str)
        except Exception as e:
            log.msg(f"Error parsing POST content: {e}")
            return {}
            
    def log_request(self, request, post_data=None):
        src_ip = request.getClientIP()
        src_port = request.client.port
        user_agent = request.getHeader('user-agent') or 'Unknown'
        language = request.getHeader('accept-language') or 'Unknown'
        referer = request.getHeader('referer') or 'Unknown'
        protocol_version = request.transport.negotiatedProtocol.decode('utf-8') if hasattr(request.transport, 'negotiatedProtocol') and request.transport.negotiatedProtocol is not None else 'Unknown'
        request_path = request.uri.decode()

        log_message = (
            f"src_ip={src_ip}, "
            f"src_port={src_port}, "
            f"user_agent='{user_agent}', "
            f"language='{language}', "
            f"referer='{referer}', "
            f"protocol_version='{protocol_version}', "
            f"path='{request_path}'"
        )

        if post_data:
            log_message += f", post_data={post_data}"

        log.msg(log_message)

class RootResource(resource.Resource):
    isLeaf = False

    def __init__(self, server):
        resource.Resource.__init__(self)
        self.server = server

    def getChild(self, path, request):
        if path == b'':
            return self
        else:
            return SimpleHTTPResource(self.server)

    def render_GET(self, request):
        if request.path == b'/':
            return SimpleHTTPResource(self.server).render_GET(request)
        else:
            return SimpleHTTPResource(self.server).render_GET(request)

class SimpleHTTPServer:
    def __init__(self, host, port, url):
        self.host = host
        self.port = port
        self.url = url

    def start(self):
        self.setup_logging()
        url_parsed = urlparse(self.url)
        url_path = url_parsed.path
        redirect_url = f'http://{self.host}:{self.port}{url_path}'

        print(f"Please wait, downloading resources from {self.url} ...")
        all_resources_downloaded = self.download_and_modify_html(self.url)

        if all_resources_downloaded:
            root = RootResource(self)
            site = server.Site(root)
            reactor.listenTCP(self.port, site, interface=self.host)
            print(f"HTTP Server running on {self.host}:{self.port}")
            reactor.run()
        else:
            print("Failed to download all resources. Server not started.")

    def setup_logging(self):
        log_file_path = os.path.join(script_dir, "http_honeypot.log")
        print(f"All HTTP requests will be logged in: {log_file_path}")

        log_observer = log.FileLogObserver(open(log_file_path, 'a'))
        log.startLoggingWithObserver(log_observer.emit, setStdout=False)

    def download_and_modify_html(self, url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        try:
            response = requests.get(url)
            self.server_banner = response.headers.get('Server', 'Apache/2.2.49')
            soup = BeautifulSoup(response.content, 'html.parser')

            for css in soup.find_all("link", rel="stylesheet"):
                if 'href' in css.attrs:
                    css_url = urllib.parse.urljoin(url, css['href'])
                    try:
                        css_response = requests.get(css_url, headers=headers)
                        css_content = css_response.text
                        new_style_tag = soup.new_tag("style")
                        new_style_tag.string = css_content
                        css.replace_with(new_style_tag)
                    except Exception as e:
                        log.msg(f"Error inlining CSS from {css_url}: {e}")

            for js in soup.find_all("script", src=True):
                js_url = urllib.parse.urljoin(url, js['src'])
                try:
                    js_response = requests.get(js_url, headers=headers)
                    js_content = js_response.text
                    new_script_tag = soup.new_tag("script")
                    new_script_tag.string = js_content
                    js.replace_with(new_script_tag)
                except Exception as e:
                    log.msg(f"Error inlining JavaScript from {js_url}: {e}")

            for img in soup.find_all("img", src=True):
                img_url = urllib.parse.urljoin(url, img['src'])
                try:
                    img_response = requests.get(img_url, headers=headers)
                    img_content = img_response.content
                    mime_type, _ = guess_type(img_url)
                    if not mime_type:
                        mime_type = "image/jpeg"  # Default MIME type
                    data_url = f"data:{mime_type};base64," + base64.b64encode(img_content).decode()
                    img['src'] = data_url
                except Exception as e:
                    log.msg(f"Error inlining image from {img_url}: {e}")

            with open(index_file_path, 'w', encoding='utf-8') as file:
                file.write(str(soup))
            
            return True
        except Exception as e:
            log.msg(f"Error processing HTML from {url}: {e}")
            return False

def main():
    parser = argparse.ArgumentParser(description='Run a simple HTTP server.')
    parser.add_argument('--host', type=str, default='0.0.0.0', help='Host to bind the HTTP server to.')
    parser.add_argument('-p', '--port', type=int, default=80, help='Port to bind the HTTP server to.')
    parser.add_argument('--url', type=str, required=True, help='URL to download and serve HTML from.')
    args = parser.parse_args()

    http_server = SimpleHTTPServer(args.host, args.port, args.url)
    http_server.start()

if __name__ == "__main__":
    main()