import socket
import threading
import queue
import unreal

class UnrealSocketServer:
    """
    Threaded socket server for Unreal Engine Editor.
    Receives Python commands via socket and executes them safely
    on the Game Thread using EditorTicker.
    """

    BUFFER_SIZE = 8192
    TICK_INTERVAL = 0.1  # Not used directly; EditorTicker ticks every frame

    def __init__(self, host="localhost", port=9999):
        """
        Initialize the server and the command queue.
        """
        self.host = host
        self.port = port
        self._running = False
        self._thread = None
        self._command_queue = queue.Queue()
        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_socket.bind((self.host, self.port))
        self._server_socket.listen(1)

        # Handle to remove the ticker later
        self._ticker_handle = None

    def start(self):
        """
        Start the socket server and register the Unreal Editor ticker.
        """
        if not self._running:
            self._running = True

            # Start background socket thread
            self._thread = threading.Thread(target=self._run_server, name="UnrealSocketServerThread")
            self._thread.daemon = True
            self._thread.start()
            unreal.log(f"[UnrealSocketServer] Listening on {self.host}:{self.port}")

            # Register with EditorTicker (runs every frame)
            self._ticker_handle = unreal.register_slate_post_tick_callback(self._tick)

    def stop(self):
        """
        Stop the socket server and unregister the Unreal ticker.
        """
        self._running = False
        try:
            self._server_socket.close()
        except Exception as e:
            unreal.log_error(f"[UnrealSocketServer] Error closing socket: {e}")
        unreal.log("[UnrealSocketServer] Server stopped.")

        if self._ticker_handle:
            unreal.unregister_slate_post_tick_callback(self._ticker_handle)
            self._ticker_handle = None

    def _run_server(self):
        """
        Threaded socket server: receives code and queues it for execution.
        """
        while self._running:
            try:
                conn, addr = self._server_socket.accept()
                unreal.log(f"[UnrealSocketServer] Connection from {addr}")
                chunks = []
                while True:
                    data = conn.recv(self.BUFFER_SIZE)
                    if not data:
                        break
                    chunks.append(data)
                command = b''.join(chunks).decode("utf-8")
                self._command_queue.put(command)
                conn.close()
            except OSError:
                break  # Socket closed
            except Exception as e:
                unreal.log_error(f"[UnrealSocketServer] Socket error: {e}")

    def _tick(self, delta_seconds: float) -> bool:
        """
        Called every frame by the editor. Executes pending commands safely.
        """
        while not self._command_queue.empty():
            command = self._command_queue.get()
            try:
                exec(command)
                unreal.log("[UnrealSocketServer] Executed command.")
            except Exception as e:
                unreal.log_error(f"[UnrealSocketServer] Execution error: {e}")
        return True  # Keep the ticker active
