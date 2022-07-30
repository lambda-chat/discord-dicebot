import os
from typing import Any, cast

from aws_lambda_powertools.logging import Logger

from dicebot.multidice import roll_by_expr

logger = Logger(service="dicebot-engine")


@logger.inject_lambda_context
def handler(event, context) -> dict[str, Any]:  # NOQA
    if event.get("api_key", "") != os.environ["LAMBDA_API_KEY"]:
        return {"statusCode": 401}  # Not Authorized

    if (expr := event.get("expression")) is None:
        return {"statusCode": 400}  # No expression
    expr = cast(str, expr)

    try:
        value = roll_by_expr(expr)  # FIXME: 一般の expression に対して実行できるようにする
        return {"statusCode": 200, "body": str(value)}  # OK
    except:  # NOQA
        return {"statusCode": 400, "body": f"invalid expression `{expr}`"}  # Invalid
