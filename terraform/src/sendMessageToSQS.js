
const AWS = require('aws-sdk');
const SQS = new AWS.SQS();
/* 宛先QueueのURL */
const QUEUE_URL = 'hogehoge.sqs';

exports.handler = function(event, context) {

    // SendMessage
    var params = {
        MessageBody: QUEUE_URL
    };

    console.log(params);
};
