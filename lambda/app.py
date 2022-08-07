import os
from dataclasses import dataclass
from enum import Enum
from typing import Any, Optional

from aws_lambda_powertools.logging import Logger
from nacl.signing import VerifyKey

logger = Logger(service="dicebot-engine")


MAX_JSON_DEPTH = 3
MAX_LOGGING_MESSAGE_LENGTH = 1000


@dataclass
class Response:
    status_code: int
    body: Any = None

    def to_json(self) -> dict[str, Any]:
        if self.body is None:
            return {"statusCode": self.status_code}
        return {"statusCode": self.status_code, "body": str(self.body)}


class DiscordMessageType(Enum):
    Ping = 1
    AnswerWithInvocation = 4


@dataclass
class DiscordResponse:
    type: DiscordMessageType
    body: Optional[str] = None
    content: Optional[str] = None

    def to_json(self) -> dict[str, Any]:
        if self.type is DiscordMessageType.Ping:
            return Response(200, str({"type": DiscordMessageType.Ping})).to_json()
        if self.type is DiscordMessageType.AnswerWithInvocation:
            return {
                "type": self.type,
                "data": {
                    "content": self.content,
                },
            }
        raise ValueError(self)


def sanitize_json(json_like: Any, depth: int = 0) -> Any:
    ty = type(json_like)
    if ty is dict:
        if depth <= MAX_JSON_DEPTH:
            return {k: sanitize_json(v, depth=depth + 1) for k, v in json_like.items()}
        else:
            return f"<dict of depth > {MAX_JSON_DEPTH}>"
    elif ty is list:
        return f"<list of length {len(json_like)}>"
    elif ty in (None, int, float, str):
        return json_like
    else:
        raise ValueError(json_like)


@logger.inject_lambda_context
def handler(event: dict, context) -> dict[str, Any]:  # NOQA
    event = sanitize_json(event)
    logger.info(str(event)[:MAX_LOGGING_MESSAGE_LENGTH])

    public_key: str = os.environ["PUBLIC_KEY"]
    signature: str = event["headers"]["x-signature-ed25519"]
    timestamp: str = event["headers"]["x-signature-timestamp"]
    body: str = event["body"]

    verify_key = VerifyKey(
        key=public_key.encode("hex"),
    )

    is_verified = verify_key.verify(
        smessage=(timestamp + body).encode("hex"),
        signature=signature.encode("hex"),
    )
    if not is_verified:
        return Response(401, "invalid request signature").to_json()

    if data := event.get("data"):
        if command_name := data.get("name"):  # handle /foo command etc.
            logger.info(f"command_name: {command_name}")
            try:
                return DiscordResponse(
                    type=DiscordMessageType.AnswerWithInvocation,
                    content="<result>",  # FIXME
                ).to_json()
            except:
                return Response(
                    status_code=401,
                    body=f"command {command_name} does not accept <dice-format>.",  # FIXME  # NOQA
                ).to_json()

    return Response(status_code=401, body="invalid command").to_json()
