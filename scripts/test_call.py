#!/usr/bin/env python3
import asyncio
import httpx


async def test_outbound_call():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/api/calls/outbound",
            json={
                "to_number": "+1234567890",
                "initial_message": "Test call"
            }
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")


if __name__ == "__main__":
    asyncio.run(test_outbound_call())
