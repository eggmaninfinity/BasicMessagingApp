# Multi-User Containerized Chat System

A concurrent messaging application built with **Python** and **Docker**. This project explores TCP socket programming, multi-threading, and CLI UX design within a containerized Linux-bridge network.

## Key Features

* **Full-Duplex CLI UI:** Leveraging `prompt-toolkit` and `patch_stdout` to provide a persistent input buffer. This allows users to type messages without being interrupted by incoming network traffic.
* **Command History:** Integrated `InMemoryHistory` allowing users to cycle through previous messages using the Up-Arrow key.
* **Service Discovery:** Clients use Docker's internal DNS to locate the `messenger-server` dynamically.
* **Layer-Optimized Dockerfiles:** Uses tiered `COPY` commands and `--no-cache-dir` to ensure fast build times and slim image sizes.

## Tech Stack

* **Language:** Python 3.11
* **Libraries:** `prompt-toolkit` (for the "advanced" UI ;-P), `socket` (Networking), `threading` (Concurrency)
* **Infrastructure:** Docker, Docker Compose, Linux Bridge Networking

## Getting Started

### Prerequisites

* [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed.

### Installation & Run

1. **Clone the repository:**
```bash
git clone https://github.com/eggmaninfinity/BasicMessagingApp

```

2. **Start the Server:**
```bash
docker-compose up -d messenger-server

```

3. **Launch Interactive Clients** (Open new terminal tabs):
* **Alice:** `docker-compose run --rm alice`
* **Bob:** `docker-compose run --rm bob`
* **Mimi:** `docker-compose run --rm mimi`

*(Using `run` ensures you catch the interactive name prompt immediately.)*

4. **Shutdown:**
* `docker-compose down`

## Technical Deep-Dive

### The Persistent Input Buffer

To solve the common "text collision" problem in terminal-based chats, I implemented `patch_stdout`. This ensures that when the background listener thread receives a message, it clears the current line, prints the new message, and re-renders the user's current unsubmitted text seamlessly.

### Docker Orchestration

The environment is managed via `docker-compose.yml`. Each client is isolated in its own container with `tty: true` and `stdin_open: true` enabled to support the interactive CLI session.
