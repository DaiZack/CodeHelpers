const axios = require('axios');
const cheerio = require('cheerio');
const fs = require('fs');
const _ = require('lodash');

var keywords = fs.readFileSync('Vendor.txt').toString().split('\n');
// console.log(keywords)

var visibleText = (res)=>{
  var $ = cheerio.load(res.data);
  for (droptag in ['style', 'script', 'footer', 'header', 'head', 'title', 'meta', '[document]']){
    $(droptag).remove()
  }
  return $('body').text()

};

var checkKeywords = (text, keywords)=>{
  keywords = keywords.map(x=>'\\W'+x+'\\W')
  let pattern =new RegExp('\\W'+keywords.join('|')+'\\W','gi');
  return text.match(pattern)
};


var checkpage = async (url, keywords)=>{
  try{
      console.log(url)
      var res = await axios.get(url);
      var vtext = visibleText(res);
      // return [...new Set(checkKeywords(vtext, keywords))];
      return checkKeywords(vtext, keywords)
  }catch{
    return null
  }

};

var checksite =async (url, keywords)=>{
  var domain = url.replace(/^.*:\/\//,'')
  if(!domain.endsWith('/')){
    domain += '/'
  }
  // console.log('http://'+domain)
  try{
    var home = await axios.get(url);
  }catch{
    console.log('bad domain ', domain)
    return
  }
  
  var $ = cheerio.load(home.data);
  var links = ['http://'+domain];
  $('a').each((i,a)=>{
    var href = $(a).attr('href')
    if(href && (href.replace(/^.*?:\/\//,'').startsWith(domain)||!href.startsWith('http'))){
      href ='http://'+domain+href.replace(/^.*?:\/+|^\W+|domain/,'')
      links.push(href)
    }
  })

  // for (l of links){
  //   var p = await checkpage(l,keywords)
  //   console.log(p)
  // }
  var out = await Promise.all(links.map(async (l)=>checkpage(l, keywords)))
  console.log(_.flatten(out))
};

checksite('https://rel8ed.to/', keywords)
// checkpage('http://ibm.com', keywords).then(console.log)
// let keyword = ['bc','ab']
// keyword = keyword.map(x=>'\\b'+x+'\\b')
// console.log(keyword)
// let pattern =new RegExp(keyword.join('|','gi'));
// console.log(pattern)
// var test = 'abc bc'.match(pattern)
// console.log(test)
