async(page)=>{
 const results=[];
 for(const theme of ['dark','light'])for(const width of [1100,850,600,375]){
  await page.setViewportSize({width,height:900});
  await page.goto('file:///E:/Zylus08-profile/reports/preview/after-'+theme+'.html');
  await page.evaluate(()=>Promise.all([...document.images].map(i=>i.decode().catch(()=>{}))));
  results.push({theme,width,...await page.evaluate(()=>({overflow:document.documentElement.scrollWidth>innerWidth,broken:[...document.images].filter(i=>!i.complete||!i.naturalWidth).map(i=>i.src),height:document.body.scrollHeight}))});
  await page.screenshot({path:'E:/Zylus08-profile/reports/screenshots/after-'+theme+'-'+width+'.png',fullPage:true});
 }
 for(const theme of ['dark','light']){
  await page.setViewportSize({width:1100,height:900});
  await page.goto('file:///E:/Zylus08-profile/reports/preview/before-'+theme+'.html');
  await page.screenshot({path:'E:/Zylus08-profile/reports/screenshots/before-'+theme+'-1100.png',fullPage:true});
 }
 const svgErrors=[];
 for(const f of ["assets/banner.svg","assets/telemetry.svg","assets/footer/signature.svg","assets/hero/hero.svg","assets/hero/mobile.svg","assets/navigation/cv.svg","assets/navigation/email.svg","assets/navigation/linkedin.svg","assets/navigation/portfolio.svg","assets/navigation/repositories.svg","assets/projects/AQC.svg","assets/projects/Axiom.svg","assets/projects/DeepHedge-RL.svg","assets/projects/FORGE.svg","assets/projects/Neural-Surrogate-Monte-Carlo-Collision-Simulator.svg","assets/projects/NOMOS.svg","assets/projects/PRAXIS.svg","assets/projects/Project-Janus.svg","assets/projects/Regime-Shift.svg","assets/projects/RiskLab.svg","assets/projects/RoadVision.svg","assets/projects/Rolls-Royce-Aerospace-RUL.svg","assets/projects/Satoshi_Flow.svg","assets/projects/Thermodynamic-Evolution-UCS503.svg","assets/projects/TradeCore.svg","assets/projects/VECTRA.svg","assets/research/frontiers-mobile.svg","assets/research/frontiers.svg","assets/research/quant-mobile.svg","assets/research/quant.svg","assets/skyline/mobile.svg","assets/skyline/skyline.svg","assets/technology/matrix-01.svg","assets/technology/matrix-02.svg","assets/technology/matrix-03.svg","assets/technology/matrix-04.svg","assets/telemetry/activity.svg","assets/telemetry/repositories.svg","assets/technology/icons/cmake.svg","assets/technology/icons/cplusplus.svg","assets/technology/icons/docker.svg","assets/technology/icons/git.svg","assets/technology/icons/githubactions.svg","assets/technology/icons/go.svg","assets/technology/icons/javascript.svg","assets/technology/icons/numpy.svg","assets/technology/icons/pandas.svg","assets/technology/icons/python.svg","assets/technology/icons/pytorch.svg","assets/technology/icons/react.svg","assets/technology/icons/rust.svg","assets/technology/icons/scikitlearn.svg","assets/technology/icons/typescript.svg","assets/technology/icons/vite.svg"]){
  await page.goto('file:///E:/Zylus08-profile/'+f);
  const check=await page.evaluate(()=>{
   const root=document.documentElement,v=root.viewBox.baseVal;
   const ctx=document.createElement('canvas').getContext('2d');
   const texts=[...document.querySelectorAll('text')].map(t=>{const box=t.getBBox(),cs=getComputedStyle(t);ctx.font=cs.fontWeight+' '+cs.fontSize+' '+cs.fontFamily;const ink=ctx.measureText(t.textContent);return {text:t.textContent,b:{x:box.x,y:Number(t.getAttribute('y'))-ink.actualBoundingBoxAscent,width:box.width,height:ink.actualBoundingBoxAscent+ink.actualBoundingBoxDescent}};});
   const clipped=texts.filter(({b})=>b.x<0||b.y<0||b.x+b.width>v.width+.1||b.y+b.height>v.height+.1).map(t=>t.text);
   const overlaps=[];
   for(let i=0;i<texts.length;i++)for(let j=i+1;j<texts.length;j++){const a=texts[i].b,b=texts[j].b;if(a.x<b.x+b.width&&a.x+a.width>b.x&&a.y<b.y+b.height&&a.y+a.height>b.y)overlaps.push([texts[i].text,texts[j].text]);}
   return {width:v.width,height:v.height,clipped,overlaps};
  });
  if(check.clipped.length||check.overlaps.length)svgErrors.push({f,...check});
  if(!f.includes('/icons/')&&!['assets/banner.svg','assets/telemetry.svg'].includes(f)){
   await page.setViewportSize({width:Math.ceil(check.width),height:Math.ceil(check.height)});
   await page.screenshot({path:'E:/Zylus08-profile/reports/screenshots/'+f.replaceAll('/','-').replace('.svg','.png')});
  }
 }
 return {layouts:results,svgCount:54,svgErrors};
}
