# Tau Chat Client

A TypeScript client that launches the tau Python module and performs a chat.

## Prerequisites

- Node.js (v14 or later)
- npm or yarn
- Python with the tau module installed

## Setup

1. Install dependencies:

```bash
npm install
```

2. Make sure you have a valid `config.json` file in the root directory of the project.

## Usage

You can start the chat client in two ways:

### Option 1: Using the shell script

```bash
./run-chat.sh
```

This script will:
1. Check for required dependencies
2. Verify that config.json exists
3. Install npm dependencies if needed
4. Start the chat client

### Option 2: Manual start

```bash
npm run start
```

This will:
1. Launch the Python tau module
2. Start a chat interface in the terminal
3. Allow you to send messages and receive responses

To exit the chat, type `\q` and press Enter.

## Building

To compile the TypeScript code to JavaScript:

```bash
npm run build
```

The compiled JavaScript will be in the `dist` directory.

## Testing

To verify that the TypeScript client is set up correctly:

```bash
./test.sh
```

This script will:
1. Check for required dependencies
2. Verify that config.json exists
3. Install npm dependencies
4. Build the TypeScript code
5. Verify that the build was successful
