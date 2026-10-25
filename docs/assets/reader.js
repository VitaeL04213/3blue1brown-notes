"use strict";
(() => {
 const body=document.body,prefix=body.dataset.prefix||"",embedded=document.documentElement.classList.contains("lab-embedded");
 const menu=document.getElementById("book-sidebar"),toggle=document.getElementById("toggle-contents"),shade=document.querySelector(".sidebar-shade"),mobile=matchMedia("(max-width:800px)");
 function closeMenu(){body.classList.remove("mobile-contents");shade.hidden=true;toggle.setAttribute("aria-expanded",mobile.matches?"false":String(!body.classList.contains("contents-hidden")));}
 function syncMenu(){closeMenu();menu.toggleAttribute("inert",mobile.matches);}
 syncMenu();mobile.addEventListener("change",syncMenu);
 toggle.addEventListener("click",()=>{
  if(mobile.matches){const open=!body.classList.contains("mobile-contents");body.classList.toggle("mobile-contents",open);shade.hidden=!open;toggle.setAttribute("aria-expanded",String(open));menu.toggleAttribute("inert",!open);if(open)menu.querySelector("input").focus();}
  else{body.classList.toggle("contents-hidden");toggle.setAttribute("aria-expanded",String(!body.classList.contains("contents-hidden")));}
 });
 function dismiss(){closeMenu();menu.toggleAttribute("inert",mobile.matches);toggle.focus();}
 document.querySelector(".close-contents").addEventListener("click",dismiss);shade.addEventListener("click",dismiss);
 document.addEventListener("keydown",event=>{
  if(event.key==="Escape"&&body.classList.contains("mobile-contents")){event.preventDefault();dismiss();}
  if(event.key==="Tab"&&body.classList.contains("mobile-contents")){
   const items=[...menu.querySelectorAll("a,button,input,summary")].filter(el=>el.getClientRects().length&&!el.hidden),first=items[0],last=items.at(-1);
   if(event.shiftKey&&document.activeElement===first){event.preventDefault();last.focus();}
   else if(!event.shiftKey&&document.activeElement===last){event.preventDefault();first.focus();}
  }
 });
 const active=menu.querySelector('a[aria-current="page"]');
 if(active&&!mobile.matches&&!embedded)menu.scrollTop=Math.max(0,active.offsetTop-250);
 const input=document.getElementById("book-search"),results=document.getElementById("search-results"),status=document.getElementById("search-status"),toc=document.getElementById("book-toc"),clear=document.getElementById("clear-search"),index=window.BookSearch||[];
 function marked(text,query){
  const fragment=document.createDocumentFragment();let start=0,pos;const lower=text.toLocaleLowerCase(),needle=query.toLocaleLowerCase();
  while(needle&&(pos=lower.indexOf(needle,start))!==-1){fragment.append(document.createTextNode(text.slice(start,pos)));const mark=document.createElement("mark");mark.textContent=text.slice(pos,pos+needle.length);fragment.append(mark);start=pos+needle.length;}
  fragment.append(document.createTextNode(text.slice(start)));return fragment;
 }
 function search(){
  const query=input.value.trim().toLocaleLowerCase();clear.hidden=!query;toc.hidden=!!query;results.hidden=!query;results.replaceChildren();
  if(!query){status.textContent="";return;}
  const terms=query.split(/\s+/),hits=index.map(item=>({item,hay:(item.title+" "+item.english+" "+item.text).toLocaleLowerCase()})).filter(({hay})=>terms.every(term=>hay.includes(term))).sort((a,b)=>Number(b.item.title.toLocaleLowerCase().includes(query))-Number(a.item.title.toLocaleLowerCase().includes(query)));
  status.textContent=hits.length?"找到 "+hits.length+" 节"+(hits.length>12?"，显示前 12 项":""):"未找到匹配内容，请尝试更短的概念或原课英文名称。";
  for(const {item} of hits.slice(0,12)){
   const li=document.createElement("li"),a=document.createElement("a"),p=document.createElement("p");a.href=prefix+"lessons/"+item.slug+".html";a.append(marked(item.number+"　"+item.title,terms[0]));
   const start=Math.max(0,item.text.toLocaleLowerCase().indexOf(terms[0])-22);p.append(marked((start?"…":"")+item.text.slice(start,start+100)+"…",terms[0]));li.append(a,p);results.append(li);
  }
 }
 let timer;input.addEventListener("input",()=>{clearTimeout(timer);timer=setTimeout(search,120);});clear.addEventListener("click",()=>{input.value="";search();input.focus();});
 try{
  const last=localStorage.getItem("3b1b-last-section");if(body.dataset.type==="lesson")localStorage.setItem("3b1b-last-section",body.dataset.page);
  const resume=document.getElementById("resume-reading"),known=index.find(item=>item.slug===last);
  if(resume&&known){resume.href=prefix+"lessons/"+known.slug+".html";resume.textContent="继续阅读 "+known.number+" →";resume.hidden=false;}
 }catch{ /* Reading remains usable without local storage. */ }
 function revealHash(){
  let id;try{id=decodeURIComponent(location.hash.slice(1));}catch{return;}
  const target=document.getElementById(id);if(!target)return;if(target.matches("details"))target.open=true;
  for(let node=target.parentElement;node;node=node.parentElement)if(node.matches("details"))node.open=true;
 }
 window.addEventListener("hashchange",revealHash);revealHash();
 document.querySelectorAll(".load-video").forEach(button=>button.addEventListener("click",()=>{
  const id=button.dataset.video;if(!/^[A-Za-z0-9_-]{11}$/.test(id))return;
  const frame=document.createElement("iframe");frame.src="https://www.youtube-nocookie.com/embed/"+id+"?rel=0";frame.title="3Blue1Brown 原课程视频";frame.allow="accelerometer; encrypted-media; gyroscope; picture-in-picture; fullscreen";frame.allowFullscreen=true;frame.referrerPolicy="strict-origin-when-cross-origin";button.parentElement.querySelector(".embed-slot").replaceChildren(frame);button.remove();
 }));
 const stepButtons=[...document.querySelectorAll('.step-play')];
 function clearStep(){stepButtons.forEach(b=>{b.setAttribute('aria-pressed','false');b.closest('.intuition-step').classList.remove('active');});}
 stepButtons.forEach(button=>button.addEventListener('click',()=>{
  clearStep();button.setAttribute('aria-pressed','true');button.closest('.intuition-step').classList.add('active');
  const title=button.closest('.intuition-step').querySelector('h3').textContent;
  document.dispatchEvent(new CustomEvent('book:step',{detail:{demo:button.dataset.demo,preset:button.dataset.preset,title}}));
  const back=document.querySelector('.return-step');back.href='#'+button.dataset.step;back.textContent='返回当前步骤：'+title+' ↓';
  if(matchMedia('(max-width:1100px)').matches)document.getElementById('interactive').scrollIntoView({behavior:matchMedia('(prefers-reduced-motion:reduce)').matches?'instant':'smooth',block:'start'});
 }));
 document.addEventListener('experiment:changed',clearStep);
 const expand=document.querySelector(".expand-knowl");
 if(expand)expand.addEventListener("click",()=>{const open=expand.getAttribute("aria-pressed")!=="true";document.querySelectorAll("details[data-print-open]").forEach(el=>el.open=open);expand.setAttribute("aria-pressed",String(open));expand.textContent=open?"收起例题与解答":"展开本节例题与解答";});
 let printClosed=[];
 window.addEventListener("beforeprint",()=>{printClosed=[...document.querySelectorAll("details[data-print-open]:not([open])")];printClosed.forEach(el=>el.open=true);});
 window.addEventListener("afterprint",()=>{printClosed.forEach(el=>el.open=false);printClosed=[];});
 document.getElementById("print-page").addEventListener("click",()=>window.print());
 const outline=document.querySelector(".page-outline");
 if(outline&&"IntersectionObserver" in window){const observer=new IntersectionObserver(entries=>{for(const item of entries)if(item.isIntersecting)outline.querySelectorAll("a").forEach(a=>a.classList.toggle("active",a.hash==="#"+item.target.id));},{rootMargin:"-150px 0px -65% 0px"});document.querySelectorAll(".lesson-prose>h2,.lesson-prose>section[id],.lesson-prose>figure[id]").forEach(el=>observer.observe(el));}
})();
