import httpx
from fastapi.requests import Request
from fastapi.responses import StreamingResponse
from starlette.background import BackgroundTask

client = httpx.AsyncClient()


async def reverse_proxy(url: str, request: Request) -> StreamingResponse:
    url = httpx.URL(url=url)  # type: ignore

    rp_request = client.build_request(method=request.method, url=url)

    # Response
    rp_response = await client.send(rp_request, stream=True)
    return StreamingResponse(
        rp_response.aiter_raw(),
        status_code=rp_response.status_code,
        headers=rp_response.headers,
        background=BackgroundTask(rp_response.aclose),
    )
