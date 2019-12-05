const axios = require('axios');
const cheerio = require('cheerio');
const fs = require('fs');
const _ = require('lodash');

try{
  var keywords = fs.readFileSync('keywords.txt').toString().split('\n');
}catch{
  var keywords = ['test','about','contact']
}
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
  links = _.uniq(links)
  var out = await Promise.all(links.map(async (l)=>checkpage(l, keywords)))
  out = _.flatten(out)
  out = out.filter(x=>x != null)
  out = out.map(x=>x.replace(/\W/g,' ').trim().toLowerCase())
  console.log(out)
};

checksite('https://www.data-blue.com/', keywords)
