function delay(one){
    var p = new Promise(resolve => {setTimeout(resolve, 300)})
    console.log(one)
    return p
  }

var a = [1,2,3,4,5,6,7,8,9,10,11,12,13];

async function loopInlimit(array,limit, callback){
    var box = [];
    var num = array.length/limit
    for (var i=0;i<=num;i++){
        if(array.length>0){
            box.push(array.splice(0,limit))
        }
    }
    await box.map(async(smallbox)=>{
        // console.log(smallbox)
        for(one of smallbox){
            // console.log(one)
            await callback(one)
        }
    })
}

loopInlimit(a,4, delay)
