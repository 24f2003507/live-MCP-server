import contextlib
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


@contextlib.asynccontextmanager
async def lifespan(app: Starlette):
    async with mcp.session_manager.run():
        yield


app = Starlette(
    routes=[
        Mount("/mcp", app=mcp.streamable_http_app())
    ],
    lifespan=lifespan,
)