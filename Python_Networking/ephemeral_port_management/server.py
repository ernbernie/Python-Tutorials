import asyncio

async def handle_client(reader, writer):
    """Handle an individual client connection."""
    addr = writer.get_extra_info('peername')
    print(f"New connection from {addr}")

    try:
        while True:
            data = await reader.read(100)  # Read data from the client
            if not data:
                break  # Break if no data (client disconnected)
            message = data.decode()
            print(f"Message from {addr}: {message}")

            # Echo the message back to the client
            writer.write(f"Server received: {message}".encode())
            await writer.drain()

            # Handle a client-initiated shutdown
            if message.lower() == "shutdown":
                print(f"Closing connection with {addr}")
                writer.write("Server is shutting down. Goodbye!".encode())
                await writer.drain()
                writer.close()
                await writer.wait_closed()
                return

    except ConnectionResetError:
        print(f"Connection with {addr} lost.")
    finally:
        print(f"Closing connection with {addr}")
        writer.close()
        await writer.wait_closed()


async def start_server():
    """Start the server and manage connections."""
    server = await asyncio.start_server(handle_client, '127.0.0.1', 12345)
    print("Server started on ('127.0.0.1', 12345)")
    print("Type 'exit' to shut down the server.")

    try:
        async with server:
            # Run the server and the command listener concurrently
            await asyncio.gather(
                server.serve_forever(),
                listen_for_exit(server)
            )
    except asyncio.CancelledError:
        print("Server shutting down gracefully.")
    finally:
        print("Server has stopped.")


async def listen_for_exit(server):
    """Listen for server shutdown commands."""
    while True:
        command = input("> ").strip().lower()
        if command == "exit":
            print("Shutting down the server...")
            server.close()
            await server.wait_closed()
            break
        else:
            print("Invalid command. Type 'exit' to stop the server.")


def display_server_menu():
    """Display the server menu and handle user input."""
    while True:
        print("=== Server Menu ===")
        print("1. Start Server")
        print("2. Help")
        print("3. Exit")
        
        choice = input("> ").strip().lower()

        if choice == "1" or choice == "start server":
            asyncio.run(start_server())
            break  # Exit the menu once the server stops
        elif choice == "2" or choice == "help":
            print("\n=== Help Menu ===")
            print("Help: This is a simple server program.")
            print("Start Server: Starts the server and listens for clients.")
            print("Exit: Closes the server.\n")
        elif choice == "3" or choice == "exit":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    display_server_menu()
