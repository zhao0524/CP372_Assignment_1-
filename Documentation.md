# TCP File Transfer & Messaging System

## Overview

This project is a simple TCP-based client-server application written in Python.
It supports:

* User login authentication
* Sending text messages
* Uploading files
* Graceful client disconnects

The system consists of:

* `server.py` — handles incoming client connections and processes commands
* `client.py` — command-line client used to communicate with the server

---

# Project Structure

```text
.
├── client.py
├── server.py
├── users.txt
└── received_files/
```

* `users.txt` stores valid usernames
* `received_files/` stores uploaded files received by the server

---

# Requirements

* Python 3.x
* Standard Python libraries only:

  * `socket`
  * `os`
  * `sys`

No external packages are required.

---

# Running the Server

```bash
python server.py
```

The server:

* Loads valid usernames from `users.txt`
* Starts listening on port `9372`
* Accepts one client connection at a time

Default configuration:

```python
HOST = "0.0.0.0"
PORT = 9372
```

---

# Running the Client

```bash
python client.py
```

Optional custom host and port:

```bash
python client.py <host> <port>
```

Example:

```bash
python client.py 127.0.0.1 9372
```

---

# Supported Commands

## LOGIN

Authenticate with a valid username.

### Syntax

```text
LOGIN <username>
```

### Example

```text
LOGIN alice
```

### Server Responses

```text
200 OK Welcome, alice
401 UNAUTHORIZED Invalid username
400 ERROR Missing username
```

---

## MSG

Send a text message to the server.

### Syntax

```text
MSG <message>
```

### Example

```text
MSG Hello server
```

### Requirements

* User must be logged in first

### Server Responses

```text
200 OK Message received: Hello server
403 FORBIDDEN Please login first
400 ERROR Empty message
```

---

## FILE

Upload a file to the server.

### Syntax

```text
FILE <filepath>
```

### Example

```text
FILE notes.txt
```

### Process

The client sends:

1. `FILE <filename>`
2. File size
3. Raw file bytes

The server:

* Validates the file size
* Saves the file into `received_files/`
* Prevents directory traversal using `os.path.basename()`

### Limits

* Maximum file size: **100 MB**

### Server Responses

```text
200 OK File 'notes.txt' received (1024 bytes)
400 ERROR Missing filename
400 ERROR Invalid file size
403 FORBIDDEN Please login first
```

---

## QUIT

Disconnect gracefully from the server.

### Syntax

```text
QUIT
```

### Response

```text
200 OK Goodbye
```

---

# Authentication

Valid usernames are stored in `users.txt`.

Example:

```text
alice
bob
charlie
```

Only usernames listed in this file are allowed to log in.

---

# Communication Protocol

The application uses a simple line-based protocol over TCP.

## Text Commands

Commands are newline (`\n`) terminated.

Example:

```text
LOGIN alice\n
```

## File Transfer Format

```text
FILE example.txt\n
1024\n
<raw file bytes>
```

---

# Error Handling

The system handles several error cases:

* Empty commands
* Invalid usernames
* Unauthorized actions
* Missing files
* Invalid file sizes
* Unexpected client disconnects

The client also handles:

* Connection failures
* Keyboard interrupts (`Ctrl+C`)
* Server disconnects

---

# Security Notes

Implemented protections include:

* Filename sanitization using `os.path.basename()`
* File size limit (100 MB)
* Authentication before messaging or file upload

Limitations:

* No password authentication
* No encryption (plain TCP)
* Single-threaded server (one client at a time)

---

# Example Session

## Client

```text
> LOGIN alice
[Server] 200 OK Welcome, alice

> MSG Hello
[Server] 200 OK Message received: Hello

> FILE test.txt
[Server] 200 OK File 'test.txt' received (45 bytes)

> QUIT
[Server] 200 OK Goodbye
```

## Server

```text
[AUTH] User logged in: alice
[MSG] alice: Hello
[FILE] Received 'test.txt' (45 bytes) from alice
```

---

# Future Improvements

Possible enhancements:

* Multi-client support using threads
* Password-based authentication
* Encrypted communication (TLS)
* File download support
* Message broadcasting/chat rooms
* Better logging system