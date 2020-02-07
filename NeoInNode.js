var r=require("request");

var txUrl = "http://username:password;@10.8.0.102:7474/db/data/transaction/commit";
var query = 'match (c:Corp) return c.name limit 1'

var axios = require('axios')
async function cypher(){
    var data = await axios.post(txUrl, json={statements:[{statement:query}]});
    console.log(data.data.results[0].data)
}
cypher()
