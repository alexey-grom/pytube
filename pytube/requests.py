# -*- coding: utf-8 -*-


def get_content_factory(client, successful_statuses=(200, )):
    async def get_content(**kwargs):
        async with client.request(**kwargs) as response:
            status = response.status
            content = None
            if status in successful_statuses:
                content = await response.text()
            return status, content
    return get_content
