const amqplib = require('amqplib');
const fs=require('fs')
const readline = require('readline');
var q = 'tasks';
var filename = 'test.csv'

async function sendmsg(q,msg){
    try{
        var conn = await  amqplib.connect('amqp://user:password@ip:port/node');
        var ch = await conn.createChannel()
        await ch.sendToQueue(q, Buffer.from(msg));
        await ch.close();
        console.log('msg send ', msg)
        conn.close()
    }catch(e){
        console.log(e)
    }
}

const readInterface = readline.createInterface({
    input: fs.createReadStream(filename)
});

readInterface.on('line', function(line) {
    sendmsg(q,line)
});
