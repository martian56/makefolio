"""Development server with hot reload."""

import http.server
import os
import signal
import socket
import socketserver
import threading
import time
from pathlib import Path

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from makefolio.builder import Builder

REBUILD_EXTENSIONS = (".md", ".yaml", ".html", ".css", ".js")
STATIC_EXTENSIONS = (
    ".html",
    ".css",
    ".js",
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".svg",
    ".ico",
    ".json",
    ".xml",
)


class RebuildHandler(FileSystemEventHandler):
    """Trigger site rebuilds on file changes with debouncing."""

    def __init__(self, builder: Builder):
        self.builder = builder
        self.last_build = 0.0

    def on_modified(self, event):
        if event.is_directory:
            return

        now = time.time()
        if now - self.last_build < 0.5:
            return
        self.last_build = now

        if any(event.src_path.endswith(ext) for ext in REBUILD_EXTENSIONS):
            name = Path(event.src_path).name
            print(f"\n[Rebuild] {name}")
            try:
                self.builder.build()
                print("Rebuild complete")
            except Exception as e:
                print(f"Rebuild failed: {e}")


class DevServer:
    """Development server with file watching for live reload."""

    def __init__(
        self, source_path: Path, output_path: Path, host: str = "127.0.0.1", port: int = 8000
    ):
        self.source_path = source_path
        self.output_path = output_path
        self.host = host
        self.port = port
        self.builder = Builder(source_path, output_path)
        self.builder.build()

    def serve(self):
        self.output_path.mkdir(parents=True, exist_ok=True)

        event_handler = RebuildHandler(self.builder)
        observer = Observer()
        observer.schedule(event_handler, str(self.source_path), recursive=True)
        observer.start()

        output_dir = str(self.output_path)
        shutdown_event = threading.Event()

        class BuildDirectoryHandler(http.server.SimpleHTTPRequestHandler):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, directory=output_dir, **kwargs)

            def do_GET(self):
                if shutdown_event.is_set():
                    return

                original_path = self.path
                if (
                    original_path
                    and not original_path.endswith(STATIC_EXTENSIONS)
                    and not original_path.endswith("/")
                ):
                    html_path = original_path + ".html"
                    file_path = os.path.join(output_dir, html_path.lstrip("/"))
                    if os.path.exists(file_path) and os.path.isfile(file_path):
                        self.path = html_path

                super().do_GET()

            def log_message(self, format, *args):
                print(f"{self.address_string()} - {format % args}")

        class ThreadedHTTPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
            daemon_threads = True
            allow_reuse_address = True
            timeout = 1

            def server_bind(self):
                self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                super().server_bind()

        httpd = ThreadedHTTPServer((self.host, self.port), BuildDirectoryHandler)
        is_shutting_down = threading.Event()

        def shutdown_server():
            if is_shutting_down.is_set():
                return
            is_shutting_down.set()

            print("\nShutting down server...")
            shutdown_event.set()

            try:
                httpd.socket.close()
            except Exception:
                pass

            try:
                observer.stop()
                observer.join(timeout=0.5)
            except Exception:
                pass

            try:
                httpd.shutdown()
            except Exception:
                pass

            try:
                httpd.server_close()
            except Exception:
                pass

            print("Server stopped")

        def signal_handler(sig, frame):
            try:
                httpd.socket.close()
            except Exception:
                pass
            threading.Thread(target=shutdown_server, daemon=True).start()

        signal.signal(signal.SIGINT, signal_handler)
        if hasattr(signal, "SIGTERM"):
            signal.signal(signal.SIGTERM, signal_handler)

        try:
            print(f"Server running at http://{self.host}:{self.port}/")
            print("Press Ctrl+C to stop")
            httpd.serve_forever(poll_interval=0.5)
        except KeyboardInterrupt:
            shutdown_server()
        finally:
            if not is_shutting_down.is_set():
                shutdown_server()
