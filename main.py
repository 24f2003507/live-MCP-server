'''import hashlib

from mcp.server.fastmcp import FastMCP, Context
from mcp.types import CallToolResult, TextContent

EMAIL = "24f2003507@ds.study.iitm.ac.in"

mcp = FastMCP(
    "Exam MCP Server",
    stateless_http=True,
    json_response=True,
)


@mcp.tool(
    name="solve_challenge",
    description="Solve the exam challenge."
)
def solve_challenge(ctx: Context) -> CallToolResult:
    headers = ctx.headers or {}

    challenge = (
        headers.get("x-exam-challenge")
        or headers.get("X-Exam-Challenge")
    )

    if not challenge:
        return CallToolResult(
            content=[
                TextContent(
                    type="text",
                    text=""
                )
            ]
        )

    answer = hashlib.sha256(
        f"{challenge}:{EMAIL}".encode("utf-8")
    ).hexdigest()[:16]

    return CallToolResult(
        content=[
            TextContent(
                type="text",
                text=answer,
            )
        ]
    )


# Expose the MCP ASGI application directly.
# This serves the MCP endpoint at "/".
app = mcp.streamable_http_app()
'''

import hashlib

from mcp.server.fastmcp import FastMCP, Context
from mcp.types import CallToolResult, TextContent

EMAIL = "24f2003507@ds.study.iitm.ac.in"

mcp = FastMCP(
    "Exam MCP Server",
    stateless_http=True,
    json_response=True,
)

@mcp.tool(name="solve_challenge")
def solve_challenge(ctx: Context) -> CallToolResult:
    headers = ctx.headers or {}

    challenge = headers.get("x-exam-challenge") or headers.get("X-Exam-Challenge")

    answer = ""
    if challenge:
        answer = hashlib.sha256(
            f"{challenge}:{EMAIL}".encode()
        ).hexdigest()[:16]

    return CallToolResult(
        content=[
            TextContent(
                type="text",
                text=answer
            )
        ]
    )

app = mcp.streamable_http_app()

print("\n===== ROUTES =====")
for r in app.routes:
    print(r)
print("==================\n")