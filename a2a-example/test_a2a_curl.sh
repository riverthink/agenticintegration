#!/bin/bash

echo "=== A2A Agent Testing with curl ==="
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}1. Get Agent A's card${NC}"
curl -s http://localhost:9999/.well-known/agent.json | jq .
echo ""

echo -e "${BLUE}2. Get Agent B's card${NC}"
curl -s http://localhost:9998/.well-known/agent.json | jq .
echo ""

echo -e "${GREEN}3. Send non-streaming message to Agent A${NC}"
curl -X POST http://localhost:9999/ \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": "test-123",
    "method": "message/send",
    "params": {
      "message": {
        "role": "user",
        "parts": [
          {
            "kind": "text",
            "text": "Hello from curl!"
          }
        ],
        "messageId": "msg-456"
      }
    }
  }' | jq .
echo ""

echo -e "${GREEN}4. Send streaming message to Agent A${NC}"
echo "Note: Streaming responses will show multiple JSON objects"
curl -X POST http://localhost:9999/ \
  -H "Content-Type: application/json" \
  -H "Accept: text/event-stream" \
  -d '{
    "jsonrpc": "2.0",
    "id": "test-789",
    "method": "message/stream",
    "params": {
      "message": {
        "role": "user",
        "parts": [
          {
            "kind": "text",
            "text": "Hello again from curl"
          }
        ],
        "messageId": "msg-789"
      }
    }
  }'
echo ""
