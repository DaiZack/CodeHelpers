const fs = require('fs')
function myFunction(one){
    return new Promise(resolve=>{
        fs.readFile('geosample.csv',(err,data)=>{
            var r = resolve(1)
            console.log(one)
            return r
        })
    })

  }

async function loopInlimit(array,limit, callback){
    var box = [];
    var num = array.length/limit
    
    for (var i=0;i<=limit;i++){
        if(array.length>0){
            box.push(array.splice(0,num))
        }
    }
    var ps = await box.map(async(smallbox)=>{
        // console.log(smallbox)
        var ps = []
        for(one of smallbox){
            // console.log(one)
            var k = await callback(one)
            ps.push(k)
        }
        console.log('small box done') // do something when a thread done!
        return ps
    })
    await Promise.all(ps)
    console.log('all done!') // do something when all threadsd one!
}

var alist = [1,2,3,4,5,6,7,8];
numofThreads = 3
loopInlimit(alist,numoThreads, myFunction)
