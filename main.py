import hashlib

from mcp.server.fastmcp import FastMCP, Context
from mcp.types import CallToolResult, TextContent

EMAIL = "24f2003507@ds.study.iitm.ac.in"

mcp = FastMCP(
    "Exam MCP Server",
    stateless_http=True,
    json_response=True,
)


@mcp.tool
def solve_challenge(ctx: Context) -> CallToolResult:
    challenge = (ctx.headers or {}).get("x-exam-challenge")

    if challenge is None:
        challenge = ""

    answer = hashlib.sha256(
        f"{challenge}:{EMAIL}".encode()
    ).hexdigest()[:16]

    return CallToolResult(
        content=[
            TextContent(
                type="text",
                text=answer,
            )
        ]
    )


app = mcp.streamable_http_app()