import * as nacl from 'tweetnacl';

type Event = {
  headers: {
    'x-signature-ed25519': string;
    'x-signature-timestamp': string;
  };
  body: string;
}

const DiscordMessageType = {
  Ping: 1,
  AnswerWithInvocation: 4
}

exports.handler = async (event: Event) => {
  const PUBLIC_KEY = process.env.PUBLIC_KEY as string;
  const signature = event.headers['x-signature-ed25519']
  const timestamp = event.headers['x-signature-timestamp'];
  const strBody = event.body;

  const isVerified = nacl.sign.detached.verify(
    Buffer.from(timestamp + strBody),
    Buffer.from(signature, 'hex'),
    Buffer.from(PUBLIC_KEY, 'hex')
  );

  if (!isVerified) {
    return {
      statusCode: 401,  // Unauthorized
      body: JSON.stringify('invalid request signature'),
    };
  }

  const body = JSON.parse(strBody)

  // Ping
  if (body.type == DiscordMessageType.Ping) {
    return {
      statusCode: 200,  // OK
      body: JSON.stringify({ "type": DiscordMessageType.Ping }),
    }
  }

  // Handle /foo Command
  if (body.data.name == 'foo') {  // FIXME
    return JSON.stringify({  // should return without statusCode
      "type": DiscordMessageType.AnswerWithInvocation,
      "data": { "content": "engine response here" }  // FIXME
    })
  }
  // Handle /bar Command
  else if (body.data.name == 'bar') {
    return JSON.stringify({
      "type": DiscordMessageType.AnswerWithInvocation,
      "data": { "content": "engine response here" }
    })
  }

  // Dafault
  return { statusCode: 404 };
};