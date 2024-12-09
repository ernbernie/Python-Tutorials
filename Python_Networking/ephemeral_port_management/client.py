import asyncio

async def start_client():
    try:
        reader, writer = await asyncio.open_connection('127.0.0.1', 12345)
        print("Connected to server at 127.0.0.1:12345")

        while True:
            message = input("Enter a message to send (type 'exit' to quit): ").strip()
            if message.lower() == "exit":
                print("Disconnecting from server...")
                writer.write("shutdown".encode())
                await writer.drain()
                break

            writer.write(message.encode())
            await writer.drain()

            response = await reader.read(100)
            print(f"Message from server: {response.decode()}")

        writer.close()
        await writer.wait_closed()

    except ConnectionRefusedError:
        print("No server found at 127.0.0.1:12345. Please make sure the server is running.")
    except asyncio.IncompleteReadError:
        print("Server has closed the connection.")
    finally:
        print("Client exiting...")


def display_client_menu():
    print("=== Client Menu ===")
    print("1. Start Client")
    print("2. Help")
    print("3. Exit")

    while True:
        choice = input("> ").strip().lower()
        if choice == "1" or choice == "start client":
            asyncio.run(start_client())
            break
        elif choice == "2" or choice == "help":
            print("Help: This is a simple client program.")
            print("Start Client: Connects to the server and sends messages.")
            print("Exit: Closes the client.")
        elif choice == "3" or choice == "exit":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    display_client_menu()
