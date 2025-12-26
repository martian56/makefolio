"""Development server with hot reload."""

import http.server
import socketserver
import socket
import threading
import signal
import sys
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from makefolio.builder import Builder


class RebuildHandler(FileSystemEventHandler):
    """Handle file system events and trigger rebuilds."""

    def __init__(self, builder: Builder):
        self.builder = builder
        self.last_build = 0

    def on_modified(self, event):
        if event.is_directory:
            return

        # Debounce rapid changes
        import time

        now = time.time()
        if now - self.last_build < 0.5:
            return
        self.last_build = now

        # Rebuild on content changes
        src_path = str(event.src_path)
        if any(src_path.endswith(ext) for ext in (".md", ".yaml", ".html", ".css", ".js")):
            print(f"\n[Rebuild] {Path(src_path).name}")
            try:
                self.builder.build()
                print("✓ Rebuild complete")
            except Exception as e:
                print(f"✗ Rebuild failed: {e}")


class DevServer:
    """Development server with file watching."""

    def __init__(
        self, source_path: Path, output_path: Path, host: str = "127.0.0.1", port: int = 8000
    ):
        self.source_path = source_path
        self.output_path = output_path
        self.host = host
        self.port = port
        self.builder = Builder(source_path, output_path)

        # Initial build
        self.builder.build()

    def serve(self):
        """Start the development server with file watching."""
        # Ensure build directory exists
        self.output_path.mkdir(parents=True, exist_ok=True)

        # Setup file watcher
        event_handler = RebuildHandler(self.builder)
        observer = Observer()
        observer.schedule(event_handler, str(self.source_path), recursive=True)
        observer.start()

        # Create custom handler that serves from build directory
        output_dir = str(self.output_path)
        shutdown_event = threading.Event()

        class BuildDirectoryHandler(http.server.SimpleHTTPRequestHandler):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, directory=output_dir, **kwargs)

            def do_GET(self):
                # Check for shutdown before handling request
                if shutdown_event.is_set():
                    return
                # Handle extensionless URLs (e.g., /about -> /about.html)
                import os

                original_path = self.path

                # Skip rewriting for files with extensions, directories, or static assets
                if (
                    original_path
                    and not original_path.endswith(
                        (
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
                    )
                    and not original_path.endswith("/")
                ):
                    # Check if .html version exists
                    html_path = (
                        original_path + ".html"
                        if not original_path.endswith("/")
                        else original_path + "index.html"
                    )
                    file_path = os.path.join(output_dir, html_path.lstrip("/"))
                    if os.path.exists(file_path) and os.path.isfile(file_path):
                        self.path = html_path

                super().do_GET()

            def log_message(self, format, *args):
                # Log requests to console
                print(f"{self.address_string()} - {format % args}")

        class ThreadedHTTPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
            daemon_threads = True
            allow_reuse_address = True
            timeout = 1

            def server_bind(self):
                self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                super().server_bind()

        httpd = ThreadedHTTPServer((self.host, self.port), BuildDirectoryHandler)

        # Flag to track if we're shutting down
        is_shutting_down = threading.Event()

        def shutdown_server():
            if is_shutting_down.is_set():
                return
            is_shutting_down.set()

            print("\nShutting down server...")
            shutdown_event.set()

            # Close socket immediately to break serve_forever() loop
            try:
                httpd.socket.close()
            except Exception:
                pass

            # Stop file watcher
            try:
                observer.stop()
                observer.join(timeout=0.5)
            except Exception:
                pass

            # Shutdown server
            try:
                httpd.shutdown()
            except Exception:
                pass

            # Close server socket
            try:
                httpd.server_close()
            except Exception:
                pass

            print("✓ Server stopped")

        def signal_handler(sig, frame):
            # Close socket directly to force serve_forever() to exit
            try:
                httpd.socket.close()
            except Exception:
                pass
            # Then do full shutdown in thread
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
