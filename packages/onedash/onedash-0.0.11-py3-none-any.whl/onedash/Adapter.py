import asyncio
from dataclasses import dataclass

import aiohttp

from .Fields.Record import Record
from .config import insert_record_url


async def send(headers, payload):
    async with aiohttp.ClientSession() as session:
        async with session.post(insert_record_url, headers=headers, json=payload) as response:
            # await session.close()
            return await response.text()


@dataclass
class Adapter:
    token: str

    # TODO insert full ref (change insert method or add new request)

    def save(self, record: Record):
        payload = {'user_id': record.user.user_id,
                   'user_message': record.user_message.text if record.user_message is not None else '',
                   'bot_message': record.bot_answer.text if record.bot_answer is not None else '',
                   'intent_name': record.intent.name if record.intent is not None else '',
                   'payload': record.payload if record.payload is not None else '',
                   'ref': record.reference.ref if record.reference is not None else '',
                   'timestamp': str(record.timestamp),
                   'slug': record.slug.name if record.slug is not None else '',
                   'message_tag': []}

        if record.intent is not None:
            if record.intent.is_misunderstanding_intent:
                payload['message_tag'].append('misunderstanding')
            if record.intent.is_unsubscribed_intent:
                payload['message_tag'].append('unsubscribed')
            if record.intent.is_nps_intent:
                payload['message_tag'].append('nps')

        headers = {'Authorization': self.token}

        loop = asyncio.get_event_loop()
        response = loop.run_until_complete(send(headers=headers, payload=payload))
        loop.close()
        return response
