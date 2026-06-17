# 📊 Metabase MCP Server

## 📚 Table of Contents

1. [What is this tool about?](#-what-is-this-tool-about)
2. [Architecture Diagram](#-architecture-diagram)
3. [Getting Started](#-getting-started)
   - [Set Up Metabase](#1-set-up-metabase-if-you-havent-already)
   - [Install uv Package Manager](#2-install-uv-package-manager)
   - [Clone or Download the Repository](#3-clone-or-download-the-repository)
   - [Install dependencies](#4-install-dependencies)
   - [Configure Your Credentials](#5-configure-your-credentials)
   - [Connect to Your MCP client](#6-connect-to-your-mcp-client)
4. [Configuration Options](#-configuration-options)
5. [Getting Your Metabase API Key](#-getting-your-metabase-api-key)
6. [DXT File Support](#-dxt-file-support)
7. [How to Create Your Own DXT File](#how-to-create-your-own-dxt-file)
8. [Remote Deployment](#-remote-deployment)
9. [Debugging with MCP Inspector](#-debugging-with-mcp-inspector)
10. [Available Tools](#-available-tools)
11. [Skills](#-skills)
12. [Example Prompts to Try](#-example-prompts-to-try)
13. [Community & Support](#-community--support)
14. [Credits](#-credits)
15. [License](#-license)

---

## 😊 What is this tool about?

**Metabase MCP Server** is a backend integration layer that connects your **Metabase** instance with **AI assistants** using the **Model Context Protocol (MCP)**. This allows business leaders, product managers and analysts to interact with business intelligence assets like dashboards and charts using **natural language**—through any MCP client (e.g., Claude Desktop).

Instead of navigating through menus or constructing SQL queries manually, you can:

- You can ask a question and get an instant insight.
- Generate dashboards and charts by describing what you want.
- Manage user access and database connections through simple instructions.

This project makes Metabase not just a dashboarding tool—but a conversational, intelligent business assistant.

---

## 📐 Architecture Diagram

![Architecture Diagram](./assets/architecture_diagram.png)

---

## 🚀 Getting Started

### 1. Set Up Metabase (If you haven't already)

Follow the official Metabase installation guide: [Metabase Docs](https://www.metabase.com/docs/latest/installation-and-operation/installing-metabase)

### 2. Install uv Package Manager

Install `uv` which includes Python and package management:

**Windows:**

```bash
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**macOS/Linux:**

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Or install via package managers:

```bash
# macOS
brew install uv

# Windows (via Scoop)
scoop install uv

# Windows (via Chocolatey)
choco install uv
```

For more information about uv installation and usage, please visit the official documentation: [https://docs.astral.sh/uv/getting-started/installation/](https://docs.astral.sh/uv/getting-started/installation/)

### 3. Clone or Download the Repository

You need to get this tool onto your computer. You can either download it manually or use Git.
Open your computer's Terminal (Mac) or Command Prompt (Windows).
Navigate to the folder where you unzipped the files or want to clone the project:

```bash
# Example (replace with your actual path):
cd ~/Downloads/metabase-mcp-server-dev
```

**Option 1: Download ZIP**

1.  Go to the [GitHub repository](https://github.com/urbs-data/metabase-mcp-server)
2.  Click the green **"Code"** button
3.  Select **"Download ZIP"**
4.  Unzip the downloaded file to a location like your **Documents** folder

**Option 2: Use Git** If you're familiar with Git, run this in your terminal:

```bash
git clone https://github.com/urbs-data/metabase-mcp-server.git
cd metabase-mcp-server

```

### 4. Install dependencies

This command will automatically:

- Install the required Python version (if not already available)
- Create a virtual environment for the project
- Install all necessary packages and dependencies

```bash
uv sync
```

### 5. Configure Your Credentials

You have three options to configure your Metabase credentials for the MCP Server:

**Option 1: Using a `.env` file (Recommended)**
The repository ships a `.env.example` you can copy as a starting point, then fill in your real values:

```bash
cp .env.example .env
```

```env
METABASE_URL=http://localhost:3000
METABASE_API_KEY=mb_xxx_your_key
PORT=3200
HOST=localhost
TRANSPORT=streamable-http
LOG_LEVEL=INFO
```

> **Note:** `TRANSPORT` defaults to `stdio`. Set `TRANSPORT=streamable-http` (as above) when you want the server to listen on a port for remote/HTTP clients.

**Option 2: Using command-line arguments**
Pass configuration directly via command line:

```bash
 uv run src/metabase_mcp_server.py --metabase-url http://localhost:3000 --metabase-api-key "YOUR_API_KEY" --port 3200 --host localhost --transport streamable-http --log-level DEBUG
```

**Option 3: Using environment variables in MCP client config**
Configure directly in your MCP client without a `.env` file (see examples below).

```json
{
  "mcpServers": {
    "metabase": {
      "type": "stdio",
      "command": "C:\\Users\\YourName\\Projects\\metabase-mcp-server\\.venv\\Scripts\\python.exe",
      "args": [
        "C:\\Users\\YourName\\Projects\\metabase-mcp-server\\src\\metabase_mcp_server.py"
      ],
      "env": {
        "METABASE_URL": "http://localhost:3000",
        "METABASE_API_KEY": "mb_xxx_your_key",
        "PORT": 3200,
        "HOST": "localhost",
        "TRANSPORT": "streamable-http",
        "LOG_LEVEL": "DEBUG"
      }
    }
  }
}
```

### 6. Connect to Your MCP client

Choose your preferred MCP clients like Claude Desktop app, Claude Code, Cursor, Windsurf etc., and add the Metabase MCP server in their respective configuration files. All MCP clients follow a similar configuration pattern.

#### Configuration Examples

**For stdio transport (recommended for local MCP server):**

**Option A: Using `uv run` (recommended — no need to manage the virtualenv path)**

Windows:

```json
{
  "mcpServers": {
    "metabase": {
      "type": "stdio",
      "command": "uv",
      "args": [
        "--directory",
        "C:\\Users\\YourName\\Projects\\metabase-mcp-server",
        "run",
        "python",
        "src\\metabase_mcp_server.py"
      ],
      "env": {
        "METABASE_URL": "http://localhost:3000",
        "METABASE_API_KEY": "mb_xxx_your_key"
      }
    }
  }
}
```

Mac/Linux:

```json
{
  "mcpServers": {
    "metabase": {
      "type": "stdio",
      "command": "uv",
      "args": [
        "--directory",
        "/Users/YourName/Projects/metabase-mcp-server",
        "run",
        "python",
        "src/metabase_mcp_server.py"
      ],
      "env": {
        "METABASE_URL": "http://localhost:3000",
        "METABASE_API_KEY": "mb_xxx_your_key"
      }
    }
  }
}
```

> **Tip:** Setting `METABASE_URL` and `METABASE_API_KEY` in the MCP client config (as shown above) takes priority over the `.env` file, so you don't need to edit `.env` after cloning.

**Option B: Using the virtualenv Python path directly**

Windows:

```json
{
  "mcpServers": {
    "metabase": {
      "type": "stdio",
      "command": "C:\\Users\\YourName\\Projects\\metabase-mcp-server\\.venv\\Scripts\\python.exe",
      "args": [
        "C:\\Users\\YourName\\Projects\\metabase-mcp-server\\src\\metabase_mcp_server.py"
      ]
    }
  }
}
```

Mac:

```json
{
  "mcpServers": {
    "metabase": {
      "type": "stdio",
      "command": "/Users/YourName/Projects/metabase-mcp-server/.venv/bin/python",
      "args": [
        "/Users/YourName/Projects/metabase-mcp-server/src/metabase_mcp_server.py"
      ]
    }
  }
}
```

##### Key Differences:

- Windows uses **backslashes** `\\` in paths
- macOS/Linux uses **forward slashes** `/` in paths
- Make sure to match the correct format based on your OS to avoid errors

##### Important Notes:

- Replace `FULL_PATH` with the actual absolute path to your project directory
- After saving configuration changes, **restart your MCP client** to apply the new settings
- For project-specific tools in Cursor, create a `.cursor/mcp.json` file in your project directory
- For global tools in Cursor, create a `~/.cursor/mcp.json` file in your home directory

**For streamable-http transport (recommended for remote MCP server):**

```json
{
  "mcpServers": {
    "metabase": {
      "type": "streamable-http",
      "url": "http://localhost:3200/mcp/"
    }
  }
}
```

#### Compatible MCP clients

Click on any client to visit their official MCP setup documentation:

| Client                                                                                                                                                                                                                               | Official MCP Documentation                        |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------- |
| [![Claude Desktop](https://img.shields.io/badge/Claude-Desktop-orange?style=for-the-badge&logo=anthropic)](https://support.anthropic.com/en/articles/10949351-getting-started-with-model-context-protocol-mcp-on-claude-for-desktop) | Anthropic's official MCP guide for Claude Desktop |
| [![Claude Code](https://img.shields.io/badge/Claude-Code-orange?style=for-the-badge&logo=anthropic)](https://docs.anthropic.com/en/docs/claude-code/mcp)                                                                             | Official Claude Code MCP setup documentation      |
| [![Cursor](https://img.shields.io/badge/Cursor-AI_Code_Editor-blue?style=for-the-badge&logo=cursor)](https://docs.cursor.com/context/model-context-protocol#configuring-mcp-servers)                                                 | Cursor's official MCP configuration guide         |
| [![Windsurf](https://img.shields.io/badge/Windsurf-Codeium-green?style=for-the-badge&logo=codeium)](https://docs.windsurf.com/windsurf/mcp)                                                                                          | Windsurf official MCP setup documentation         |
| [![Cline](https://img.shields.io/badge/Cline-VS_Code_Extension-purple?style=for-the-badge&logo=visualstudiocode)](https://docs.cline.bot/mcp-servers/mcp-quickstart)                                                                 | Cline's official MCP quickstart guide             |
| [![VS Code](https://img.shields.io/badge/VS_Code-Copilot-blue?style=for-the-badge&logo=visualstudiocode)](https://code.visualstudio.com/docs/copilot/chat/mcp-servers#_add-an-mcp-server-to-your-workspace)                          | VS Code Copilot MCP server configuration          |

Once you have added the configuration, the MCP server should be visible in your MCP client.

---

## 🔧 Configuration Options

The Metabase MCP Server supports flexible configuration through environment variables, command-line arguments, or a combination of both.

### Environment Variables

| Variable           | Description                | Default Value     | Example                     |
| ------------------ | -------------------------- | ----------------- | --------------------------- |
| `METABASE_URL`     | Your Metabase instance URL | Required          | `http://127.0.0.1:3000`     |
| `METABASE_API_KEY` | Your Metabase API key      | Required          | `mb_xxx_your_api_key`       |
| `TRANSPORT`        | Transport protocol         | `stdio`           | `stdio`, `streamable-http`  |
| `HOST`             | Host for HTTP transports   | `localhost`       | `0.0.0.0`, `127.0.0.1`      |
| `PORT`             | Port for HTTP transports   | `3200`            | `8080`, `9000`              |
| `LOG_LEVEL`        | Logging level              | `INFO`            | `DEBUG`, `WARNING`, `ERROR` |

### Command-line Arguments

| Argument             | Description              | Default Value     |
| -------------------- | ------------------------ | ----------------- |
| `--metabase-url`     | Metabase instance URL    | Required          |
| `--metabase-api-key` | Metabase API key         | Required          |
| `--transport`        | Transport protocol       | `stdio`           |
| `--host`             | Host for HTTP transports | `localhost`       |
| `--port`             | Port for HTTP transports | `3200`            |
| `--log-level`        | Logging verbosity level  | `INFO`            |

### Transport Protocols

| Protocol            | Description                         | Use Case                                                   |
| ------------------- | ----------------------------------- | ---------------------------------------------------------- |
| **stdio**           | Standard input/output communication | Best for local integrations (Claude Desktop, Cursor, etc.) |
| **streamable-http** | HTTP-based streaming protocol       | Ideal for remote deployments and web-based integrations    |
| **sse**             | Server-Sent Events over HTTP        | ⚠️ **Deprecated - Not recommended for new setups**         |

### Configuration Priority

Configuration values are applied in the following priority order (highest to lowest):

1. **Command-line arguments** (overrides everything)
2. **Environment variables** (overrides defaults)
3. **Default values**

### Complete Command Examples

```bash
uv run src/metabase_mcp_server.py --transport streamable-http --host localhost --port 3200 --metabase-url http://127.0.0.1:3000 --metabase-api-key mb_xxx_your_key

```

**Note:** You don't need to pass every parameter when running the server. However, you must provide the Metabase URL and API key. Any parameters not specified will use their default values as shown above.

---

## 🔑 Getting Your Metabase API Key

To get your Metabase API key:

1. **Log into your Metabase instance**
2. **Click on your profile picture** (top-right corner)
3. **Select "Account settings"**
4. **Navigate to the "API Keys" tab**
5. **Click "Create API Key"**
6. **Give your key a descriptive name** (e.g., "MCP Server Key")
7. **Copy the generated key** (starts with `mb_`)

⚠️ **Important:** Store your API key securely and never commit it to version control. The key provides full access to your Metabase instance.

---

## 📂 DXT File Support

You no longer need to go through the steps of cloning the repository and setting up the environment. Simply follow the steps below to install the **Metabase MCP Server** in your **Cloude Desktop App**:

1. **Download the DXT File**  
   Check the link below to download the latest **DXT file** directly:  
   [Download DXT File](./metabase-mcp-server.dxt)

2. **Open the Claude Desktop App**  
   Once you have the file, open the **Claude Desktop App** on your system.

3. **Navigate to Extensions Settings**  
   In the **Claude Desktop App**:

   - Go to **Files** → **Settings** → **Extensions**
   - Then click on **Advanced Settings**.

4. **Select the DXT File**  
   In the **Advanced Settings** section, click on **Choose File**, select the downloaded **DXT file**.

5. **Enter the Required Details**  
   After slecting the **DXT file**, a prompt will appear asking you to fill in the required details:

   - **Metabase URL**: Enter your Metabase server URL.
   - **API Key**: Add the relevant API key for authentication.

6. **Complete the Setup**  
   After entering the necessary details, click **Save** to apply the configuration.

That's it! The **Metabase MCP Server** is now installed and ready to use in your **Claude Desktop App**.

## How to Create Your Own DXT File

If you want to create your own **DXT file**, please visit the Official Guide:  
[Creating Your Own DXT File](https://www.anthropic.com/engineering/desktop-extensions)

## 🚀 Remote Deployment

For production use or team collaboration, you can deploy the Metabase MCP Server remotely as an HTTP service (`TRANSPORT=streamable-http`).

### Docker Deployment

The repository includes a `Dockerfile` and a `docker-compose.yml` to make remote deployment straightforward.

#### Docker Compose (Recommended)

The bundled `docker-compose.yml` reads all configuration from a `.env` file and joins an **existing Docker network shared with your Metabase instance**, so the MCP can reach Metabase by its service name:

```yaml
services:
  metabase-mcp:
    build: .
    container_name: metabase-mcp
    env_file: .env
    ports:
      - "3200:3200" # optional if the client reaches it over the Docker network / a tunnel
    networks:
      - metabase-net
    restart: unless-stopped

networks:
  metabase-net:
    external: true
    name: metabase_metanet1 # the network your Metabase containers already use
```

Steps:

```bash
# 1. Create your env file from the template and fill in real values
cp .env.example .env

# 2. Start the service (builds the image on first run)
docker compose up -d --build
```

> **Network note:** `metabase_metanet1` must be the Docker network your Metabase stack already runs on, so set `METABASE_URL` to the Metabase **service name** (e.g. `http://metabase:3000`), not `localhost`. If your network has a different name, edit the `name:` field in `docker-compose.yml`. To inspect available networks run `docker network ls`. If you are running Metabase elsewhere (not in Docker), remove the `networks:` block and point `METABASE_URL` at its reachable URL instead.

#### Quick Start without Compose

If you prefer a one-off container, pass the configuration as environment variables:

```bash
# Build the Docker image
docker build -t metabase-mcp-server .

# Run it
docker run -d \
  -p 3200:3200 \
  -e METABASE_URL="http://your-metabase-instance.com" \
  -e METABASE_API_KEY="mb_xxx_your_api_key" \
  -e TRANSPORT="streamable-http" \
  -e HOST="0.0.0.0" \
  metabase-mcp-server
```

#### Connecting to Remote MCP Server

Once deployed, configure your MCP clients to connect to the remote server:

```json
{
  "mcpServers": {
    "metabase": {
      "type": "streamable-http",
      "url": "http://server-ip:3200/mcp/"
    }
  }
}
```

### Deployment Options

- **Cloud Providers:** AWS ECS, Google Cloud Run, Azure Container Instances
- **VPS/Dedicated Servers:** DigitalOcean, Linode, Vultr
- **Container Platforms:** Kubernetes, Docker Swarm
- **Platform-as-a-Service:** Railway, Render, Fly.io

### Security Considerations

- Use HTTPS in production environments
- Implement proper firewall rules
- Consider VPN access for sensitive business data
- Regularly rotate API keys
- Monitor access logs

---

## 🔍 Debugging with MCP Inspector

To debug and test your Metabase MCP Server setup, you can use the official MCP Inspector tool.

### Prerequisites

First, install Node.js if you haven't already:

- **Download from:** [nodejs.org](https://nodejs.org/en/download)
- **Or install via package manager:**

  ```bash
  # macOS
  brew install node

  # Windows (via Chocolatey)
  choco install nodejs

  # Windows (via Scoop)
  scoop install nodejs
  ```

### Install and Run MCP Inspector

```bash
# Install MCP Inspector globally
npm install -g @modelcontextprotocol/inspector

# Run the inspector with your Metabase MCP Server
npx @modelcontextprotocol/inspector uv run FULL_PATH/metabase-mcp-server/src/metabase_mcp_server.py
```

### Using MCP Inspector

The MCP Inspector provides:

- **Real-time tool testing** - Execute MCP tools directly from the web interface
- **Request/Response monitoring** - See exactly what data is being sent and received
- **Error debugging** - Identify configuration or API issues quickly
- **Schema validation** - Verify that your tools are properly defined

Once running, open your browser to `http://localhost:5173` to access the inspector interface.

### Common Debugging Scenarios

- **Connection issues** - Verify your Metabase URL and API key
- **Permission errors** - Check if your API key has the required permissions

---

## 🔧 Available Tools

The server exposes **36 tools** covering collections, charts, dashboards, databases, table/database metadata, users, groups, and raw SQL.

| Function                     | Description                            |
| ---------------------------- | -------------------------------------- |
| **Collection Operations**    |                                        |
| `get_metabase_collections`   | List all collections                   |
| `get_collection_items`       | Get items inside a collection          |
| `get_metabase_collection`    | Get a collection by ID                 |
| `create_metabase_collection` | Create a new collection                |
| `update_metabase_collection` | Update collection metadata             |
| `delete_metabase_collection` | Delete a collection                    |
| **Chart (Card) Operations**  |                                        |
| `get_metabase_cards`         | List all charts                        |
| `get_card_query_results`     | Get results from a chart query         |
| `create_metabase_card`       | Create a new chart                     |
| `update_metabase_card`       | Update an existing chart               |
| `delete_metabase_card`       | Delete a chart                         |
| **Dashboard Operations**     |                                        |
| `get_metabase_dashboards`    | List all dashboards                    |
| `get_dashboard_by_id`        | Get a dashboard by ID                  |
| `get_dashboard_cards`        | Get cards in a dashboard               |
| `create_metabase_dashboard`  | Create a dashboard                     |
| `update_metabase_dashboard`  | Update a dashboard                     |
| `delete_metabase_dashboard`  | Delete a dashboard                     |
| `copy_metabase_dashboard`    | Create a copy of an existing dashboard |
| `add_card_to_dashboard`      | Add a saved question to a dashboard    |
| `remove_card_from_dashboard` | Remove a card from a dashboard         |
| `move_resize_dashboard_card` | Move or resize a card on a dashboard   |
| **Database Operations**           |                                        |
| `get_metabase_databases`          | List databases                         |
| `get_metabase_database_metadata`  | Get tables and fields for a database   |
| `get_metabase_table_metadata`     | Get field details for a table          |
| `create_metabase_database`        | Create a new database connection       |
| `update_metabase_database`        | Update a database connection           |
| `delete_metabase_database`        | Delete a database connection           |
| **User Operations**          |                                        |
| `get_metabase_users`         | List all users                         |
| `get_metabase_current_user`  | Get current user details               |
| `create_metabase_user`       | Create a new user                      |
| `update_metabase_user`       | Update user info                       |
| `delete_metabase_user`       | Delete a user                          |
| **Group Operations**         |                                        |
| `get_metabase_groups`        | List user groups                       |
| `create_metabase_group`      | Create a user group                    |
| `delete_metabase_group`      | Delete a user group                    |
| **SQL Operations**           |                                        |
| `execute_sql_query`          | Execute a native SQL query             |

---

## 🎯 Skills

Skills are workflow instructions for Claude that unlock guided, multi-step experiences on top of the MCP tools — without requiring technical knowledge from the user.

### `metabase-chart` — Business chart assistant (Spanish)

A guided workflow for non-technical users to create charts and dashboards through natural language. Claude handles all technical details (field IDs, MBQL format, grid positioning) invisibly.

**Install:**

```bash
# Windows
copy skills\metabase-chart\SKILL.md "%APPDATA%\Claude\skills\metabase-chart\SKILL.md"

# macOS/Linux
mkdir -p ~/.claude/skills/metabase-chart
cp skills/metabase-chart/SKILL.md ~/.claude/skills/metabase-chart/SKILL.md
```

**Usage:** Type `/metabase-chart` in Claude Desktop and describe what you want to see.

**What it does:**
- Asks business-friendly questions in plain language (no IDs, no SQL visible to the user)
- Shows a live data preview before creating anything
- Requires explicit confirmation before creating or adding to a dashboard
- Creates charts in native Metabase MBQL format (editable and filterable in the UI)
- Automatically places charts in available space on the target dashboard

---

## 🧪 Example Prompts to Try

- Create a dashboard called 'Flight Overview' with a bar chart showing flights by destination city.
- Run SQL: `SELECT origin, destination, COUNT(*) FROM flights GROUP BY origin, destination LIMIT 10`.
- Create a card displaying total bookings last month grouped by region.
- Add the 'Monthly Revenue' chart to the 'Finance' dashboard below the existing cards.
- Move the KPI card to row 0, column 0 on the Sales dashboard and resize it to 6×3.
- Show me all charts in the Marketing collection.
- Delete the chart named 'Abandoned Queries'.
- Update the dashboard 'Sales KPIs' to include a new revenue card.
- Show all users in the 'Admin' group.
- Create a new group called 'Finance Analysts'.
- Connect to a Supabase database and list all tables.

---

## 💬 Community & Support

This is a community-maintained project — contributions, bug reports, and ideas are welcome!

- **🐙 Repository:** [urbs-data/metabase-mcp-server](https://github.com/urbs-data/metabase-mcp-server)
- **🐞 Issues:** [Report a bug or request a feature](https://github.com/urbs-data/metabase-mcp-server/issues)
- **🤝 Contributing:** Open a pull request — improvements to tools, docs, and the `metabase-chart` skill are especially appreciated.

---

## 🙏 Credits

This project started as a fork of [**CW-Codewalnut/metabase-mcp-server**](https://github.com/CW-Codewalnut/metabase-mcp-server) and is maintained as a community collaboration on top of their original work. Many thanks to the CodeWalnut team for building the foundation this project is based on.

---

## 📜 License

This project is licensed under the [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0).

You can find the full license text in the [`LICENSE`](./LICENSE) file.

---
