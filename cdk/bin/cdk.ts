#!/usr/bin/env node
/* eslint-disable import/no-extraneous-dependencies */
import * as cdk from 'aws-cdk-lib';
import { DiscordDicebotAppStack } from '../lib/discord-dicebot-app-stack';

const app = new cdk.App();
const _ = new DiscordDicebotAppStack(app, 'DiscordDicebotAppStack');
