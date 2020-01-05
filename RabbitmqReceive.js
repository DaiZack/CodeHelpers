var amqp = require('amqplib');
var q = 'tasks';

async function readmsg(q, callback){
    try{
        var conn = await amqp.connect('amqp://user:password@ip:port/node');
        var ch = await conn.createChannel();
        // var queue =  await ch.assertQueue(q);
        await ch.consume(q, callback,{noAck: true})
    }catch(e){
        console.log(e)
    }
}

function callback(msg){
    console.log(msg.content.toString())
}


readmsg(q,callback)
