from unreal_mcp_server import mcp

if __name__ == "__main__":
    # This will spin up a single‐endpoint HTTP server (Streamable HTTP transport)
    # listening on 127.0.0.1:8000 by default.
    mcp.run(transport="streamable-http")