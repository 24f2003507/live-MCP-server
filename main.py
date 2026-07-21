import hashlib

from mcp.server.fastmcp import FastMCP, Context
from mcp.types import CallToolResult, TextContent
from starlette.applications import Starlette
from starlette.routing import Mount

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


mcp_app = mcp.streamable_http_app()

app = Starlette(
    routes=[
        Mount("/", app=mcp_app),
    ],
    lifespan=mcp_app.lifespan,
)