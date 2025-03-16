#!/bin/bash

# Set error handling
set -e

echo "Testing Tau Chat TypeScript Client"
echo "=================================="

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js to run this test."
    exit 1
else
    echo "✅ Node.js is installed"
fi

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "❌ npm is not installed. Please install npm to run this test."
    exit 1
else
    echo "✅ npm is installed"
fi

# Check if Python is installed
if ! command -v python &> /dev/null; then
    echo "❌ Python is not installed. Please install Python to run this test."
    exit 1
else
    echo "✅ Python is installed"
fi

# Check if config.json exists in the parent directory
if [ ! -f "../config.json" ]; then
    echo "❌ config.json not found in the parent directory."
    echo "   Please create a config.json file based on config.example.json."
    exit 1
else
    echo "✅ config.json exists"
fi

# Install dependencies
echo "Installing dependencies..."
npm install
echo "✅ Dependencies installed"

# Build the TypeScript code
echo "Building TypeScript code..."
npm run build
echo "✅ TypeScript code built successfully"

# Check if the build directory exists
if [ ! -d "dist" ]; then
    echo "❌ Build failed: dist directory not found."
    exit 1
else
    echo "✅ dist directory exists"
fi

# Check if the compiled JavaScript file exists
if [ ! -f "dist/chat.js" ]; then
    echo "❌ Build failed: dist/chat.js not found."
    exit 1
else
    echo "✅ dist/chat.js exists"
fi

echo ""
echo "All tests passed! The TypeScript client is ready to use."
echo "Run './run-chat.sh' to start the chat client."
