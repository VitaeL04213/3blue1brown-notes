/* Independent, dependency-free interactive figures. Geometry is evaluated in data coordinates. */
"use strict";
(() => {
 const root=document.getElementById("experiment-root");if(!root)return;
 const D=window.BookExperiments,$=id=>root.querySelector("#"+id),canvas=$("plot"),ctx=canvas.getContext("2d"),prefix=document.body.dataset.prefix||"";
 const color={input:"#258761",output:"#d85a45",basis:"#346ac4",second:"#ae7b19",sum:"#8758b3",grid:"#e2e7eb",ink:"#304855"};
 let current=root.dataset.demo||location.hash.slice(1),v={},playing=false,raf=0,width=700,height=340,handles=[],drag=null,stepLabel="自由探索",lastRead=0;
 let camera={zoom:1,x:0,y:0,yaw:.7,pitch:.65};
 const f=(x,n=4)=>!Number.isFinite(x)?"未定义":Math.abs(x)>=1e5?x.toExponential(2):Number(x.toFixed(n)).toString();
 const clamp=(x,a,b)=>Math.min(b,Math.max(a,x));
 function text(x,y,s,c=color.ink,size=12,align="left"){ctx.fillStyle=c;ctx.font=size+"px system-ui, sans-serif";ctx.textAlign=align;ctx.fillText(s,x,y);ctx.textAlign="left";}
 function path(points,c,w=2,dash=[]){ctx.beginPath();ctx.strokeStyle=c;ctx.lineWidth=w;ctx.setLineDash(dash);points.forEach((p,i)=>i?ctx.lineTo(...p):ctx.moveTo(...p));ctx.stroke();ctx.setLineDash([]);}
 function arrow(a,b,c,w=2.5){path([a,b],c,w);const t=Math.atan2(b[1]-a[1],b[0]-a[0]);ctx.beginPath();ctx.fillStyle=c;ctx.moveTo(...b);ctx.lineTo(b[0]-9*Math.cos(t-.38),b[1]-9*Math.sin(t-.38));ctx.lineTo(b[0]-9*Math.cos(t+.38),b[1]-9*Math.sin(t+.38));ctx.fill();}
 function dot(p,c,r=4){ctx.beginPath();ctx.fillStyle=c;ctx.arc(...p,r,0,2*Math.PI);ctx.fill();}
 function polygon(points,c){ctx.beginPath();points.forEach((p,i)=>i?ctx.lineTo(...p):ctx.moveTo(...p));ctx.closePath();ctx.fillStyle=c;ctx.fill();}
 function frame(bounds,box={x:0,y:0,w:width,h:height},equal=false,label=""){
  const pad={l:39,r:16,t:label?34:22,b:30},x=box.x+pad.l,y=box.y+pad.t,w=box.w-pad.l-pad.r,h=box.h-pad.t-pad.b;
  let [a,b,c,d]=bounds;if(equal){const half=Math.max((d-c)/2,(b-a)/2*h/w);const mx=(a+b)/2,my=(c+d)/2;a=mx-half*w/h;b=mx+half*w/h;c=my-half;d=my+half;}
  const mx=(a+b)/2+camera.x,my=(c+d)/2+camera.y,sx=(b-a)/(2*camera.zoom),sy=(d-c)/(2*camera.zoom);a=mx-sx;b=mx+sx;c=my-sy;d=my+sy;
  const P={x,y,w,h,a,b,c,d,xy:(u,z)=>[x+(u-a)/(b-a)*w,y+h-(z-c)/(d-c)*h],world:(px,py)=>[a+(px-x)/w*(b-a),c+(y+h-py)/h*(d-c)]};
  ctx.fillStyle="#fbfcfd";ctx.fillRect(x,y,w,h);
  for(let i=0;i<=4;i++){let xx=a+(b-a)*i/4,yy=c+(d-c)*i/4;path([P.xy(xx,c),P.xy(xx,d)],color.grid,1);path([P.xy(a,yy),P.xy(b,yy)],color.grid,1);text(P.xy(xx,c)[0],y+h+19,f(xx,2),"#6c7e87",10,"center");text(x-6,P.xy(a,yy)[1]+4,f(yy,2),"#6c7e87",10,"right");}
  if(a<=0&&b>=0)path([P.xy(0,c),P.xy(0,d)],"#8d9ca5",1.4);
  if(c<=0&&d>=0)path([P.xy(a,0),P.xy(b,0)],"#8d9ca5",1.4);
  if(label)text(box.x+box.w/2,box.y+17,label,color.ink,12,"center");
  return P;
 }
 function clip(P,fn){ctx.save();ctx.beginPath();ctx.rect(P.x,P.y,P.w,P.h);ctx.clip();fn();ctx.restore();}
 function curve(P,fn,c,w=2.5){clip(P,()=>{let segment=[];for(let i=0;i<=350;i++){const x=P.a+(P.b-P.a)*i/350,y=fn(x);if(!Number.isFinite(y)||Math.abs(y)>1e8){if(segment.length>1)path(segment,c,w);segment=[];}else segment.push(P.xy(x,y));}if(segment.length>1)path(segment,c,w);});}
 function vector(P,x,y,c,label){clip(P,()=>{arrow(P.xy(0,0),P.xy(x,y),c);});let pt=P.xy(x,y);if(pt[0]>=P.x&&pt[0]<=P.x+P.w&&pt[1]>=P.y&&pt[1]<=P.y+P.h)text(pt[0]+8,pt[1]-9,label,c,12);}
 function handle(P,x,y,name,move,c=color.input){const p=P.xy(x,y);if(p[0]<P.x||p[0]>P.x+P.w||p[1]<P.y||p[1]>P.y+P.h)return;ctx.beginPath();ctx.arc(...p,7,0,Math.PI*2);ctx.fillStyle="white";ctx.fill();ctx.strokeStyle=c;ctx.lineWidth=2.5;ctx.stroke();handles.push({x:p[0],y:p[1],name,move:(px,py)=>move(...P.world(px,py))});}
 function rawHandle(p,name,move,c){ctx.beginPath();ctx.arc(...p,7,0,Math.PI*2);ctx.fillStyle="white";ctx.fill();ctx.strokeStyle=c;ctx.lineWidth=2.5;ctx.stroke();handles.push({x:p[0],y:p[1],name,move});}
 function set(key,value){const c=D[current].controls.find(c=>c[0]===key);if(c&&Number.isFinite(value))v[key]=clamp(c[4]===1?Math.round(value):value,c[2],c[3]);}
 function fun(x){if(v.family===0)return x*x;if(v.family===1)return x*x*x;if(v.family===2)return Math.sin(x);if(v.family===3)return Math.exp(x);return x>0?Math.log(x):NaN;}
 function df(x){if(v.family===0)return 2*x;if(v.family===1)return 3*x*x;if(v.family===2)return Math.cos(x);if(v.family===3)return Math.exp(x);return x>0?1/x:NaN;}
 function mul(A,p){return [A[0]*p[0]+A[1]*p[1],A[2]*p[0]+A[3]*p[1]];}
 function cross(a,b){return [a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]];}
 function spatial(){
  const u=[v.ax,v.ay,v.az],w=[v.bx,v.by,v.bz],normal=cross(u,w),c=Math.cos(camera.yaw),s=Math.sin(camera.yaw),cp=Math.cos(camera.pitch),sp=Math.sin(camera.pitch);
  const largest=Math.max(2,...u.map(Math.abs),...w.map(Math.abs),...normal.map(Math.abs)),scale=Math.min(width,height)*.32/largest*camera.zoom;
  const project=p=>[width/2+scale*(c*p[0]-s*p[1])+camera.x*20,height*.55-scale*(cp*p[2]-sp*(s*p[0]+c*p[1]))-camera.y*20];
  for(let i=-3;i<=3;i++){path([project([-3,i,0]),project([3,i,0])],color.grid,1);path([project([i,-3,0]),project([i,3,0])],color.grid,1);}
  [[1,0,0],[0,1,0],[0,0,1]].forEach((p,i)=>{const q=p.map(x=>x*2.3);arrow(project([0,0,0]),project(q),"#86949a",1.3);text(...project(q),[" x"," y"," z"][i],"#6c7e87",12);});
  function vec(p,c,label){arrow(project([0,0,0]),project(p),c,3);const q=project(p);text(q[0]+8,q[1]-9,label,c,13);}
  vec(u,color.input,"u");
  if(v.mode===0){polygon([[0,0,0],u,u.map((x,i)=>x+w[i]),w].map(project),"#4e84b51c");vec(w,color.basis,"v");vec(normal,color.output,"u × v");}
  if(v.mode===1){const r=[u[0]*Math.cos(v.angle)-u[1]*Math.sin(v.angle),u[0]*Math.sin(v.angle)+u[1]*Math.cos(v.angle),u[2]];vec(r,color.output,"R u");path([project(u),project(r)],color.output,1,[4,4]);}
  if(v.mode===2){const p=[u[0],u[1],0];vec(p,color.output,"P u");path([project(u),project(p)],"#8899aa",1.5,[4,4]);}
  const movable=(p,keys,name,col)=>rawHandle(project(p),name,(px,py)=>{if(Math.abs(sp)<.15)return;const xx=(px-width/2-camera.x*20)/scale,yy=(height*.55-py-camera.y*20)/scale;const ry=(cp*p[2]-yy)/sp;set(keys[0],c*xx+s*ry);set(keys[1],-s*xx+c*ry);},col);
  movable(u,["ax","ay"],"空间向量 u",color.input);if(v.mode===0)movable(w,["bx","by"],"空间向量 v",color.basis);
  return v.mode===0?"u × v = ("+normal.map(x=>f(x)).join(", ")+")；|u| = "+f(Math.hypot(...u))+"；底面面积 = "+f(Math.hypot(...normal))+"；u · (u × v) = "+f(u.reduce((sum,x,i)=>sum+x*normal[i],0)):
   v.mode===1?"绕 z 轴转动 "+f(v.angle)+" rad；|u| = |R u| = "+f(Math.hypot(...u)):"P(u) = ("+f(u[0])+", "+f(u[1])+")；被舍去的 z 分量 = "+f(u[2]);
 }
 function draw(){
  const rect=canvas.getBoundingClientRect();width=Math.max(250,rect.width);height=rect.height;const ratio=Math.min(devicePixelRatio||1,2);
  if(canvas.width!==Math.round(width*ratio)||canvas.height!==Math.round(height*ratio)){canvas.width=Math.round(width*ratio);canvas.height=Math.round(height*ratio);}
  ctx.setTransform(ratio,0,0,ratio,0,0);ctx.clearRect(0,0,width,height);ctx.fillStyle="#fff";ctx.fillRect(0,0,width,height);handles=[];
  let result="",equation="",P;
  if(current==="vectors"){
   P=frame([-4,4,-3,3],undefined,true);const sum=[v.s*v.ux+v.vx,v.s*v.uy+v.vy];vector(P,v.s*v.ux,v.s*v.uy,color.input,"s u");vector(P,v.vx,v.vy,color.basis,"v");vector(P,...sum,color.output,"s u + v");
   path([P.xy(v.s*v.ux,v.s*v.uy),P.xy(...sum),P.xy(v.vx,v.vy)],"#92a7af",1.5,[5,4]);handle(P,v.ux,v.uy,"u",(x,y)=>{set("ux",x);set("uy",y);});handle(P,v.vx,v.vy,"v",(x,y)=>{set("vx",x);set("vy",y);},color.basis);
   result="s u + v = ("+sum.map(x=>f(x)).join(", ")+")；det[u,v] = "+f(v.ux*v.vy-v.uy*v.vx);equation="位移相加保留方向与长度，平移箭头不改变它代表的向量。";
  }else if(current==="linear"){
   const A=Models.matrix(v.a,v.b,v.c,v.d,v.t),out=mul(A,[v.x,v.y]),r=Math.max(3,...out.map(x=>Math.abs(x)*1.15));
   const left=frame([-3,3,-3,3],{x:0,y:0,w:width/2,h:height},true,"输入空间"),right=frame([-r,r,-r,r],{x:width/2,y:0,w:width/2,h:height},true,"输出空间");
   polygon([[0,0],[1,0],[1,1],[0,1]].map(p=>left.xy(...p)),"#3075ac20");vector(left,v.x,v.y,color.input,"x");handle(left,v.x,v.y,"输入 x",(x,y)=>{set("x",x);set("y",y);});
   clip(right,()=>{for(let k=-4;k<=4;k++){path([right.xy(...mul(A,[-4,k])),right.xy(...mul(A,[4,k]))],"#d4dfe5",1);path([right.xy(...mul(A,[k,-4])),right.xy(...mul(A,[k,4]))],"#d4dfe5",1);}polygon([[0,0],[1,0],[1,1],[0,1]].map(p=>right.xy(...mul(A,p))),"#bf922a27");});
   vector(right,A[0],A[2],color.basis,"A e₁");vector(right,A[1],A[3],color.second,"A e₂");vector(right,...out,color.output,"A x");
   handle(right,A[0],A[2],"第一列",(x,y)=>{v.t=1;set("a",x);set("c",y);},color.basis);handle(right,A[1],A[3],"第二列",(x,y)=>{v.t=1;set("b",x);set("d",y);},color.second);
   const det=Models.determinant(A);result="A x = ("+out.map(x=>f(x)).join(", ")+")；det A = "+f(det)+"；面积倍率 = "+f(Math.abs(det))+(Math.abs(det)<1e-9?"，压扁、失去唯一逆像":det<0?"，定向翻转":"，保持定向");
   equation="A = [ "+f(A[0],2)+"  "+f(A[1],2)+" ; "+f(A[2],2)+"  "+f(A[3],2)+" ]，x = ("+f(v.x,2)+", "+f(v.y,2)+")";
  }else if(current==="compose"){
   const A=[v.s,v.k,0,1],B=[Math.cos(v.theta),-Math.sin(v.theta),Math.sin(v.theta),Math.cos(v.theta)],input=[v.x,v.y],mid=mul(v.order?A:B,input),out=mul(v.order?B:A,mid);
   [input,mid,out].forEach((p,i)=>{const F=frame([-3,3,-3,3],{x:i*width/3,y:0,w:width/3,h:height},true,["输入",v.order?"先 A":"先 B",v.order?"再 B":"再 A"][i]);vector(F,...p,[color.input,color.sum,color.output][i],["x","中间","结果"][i]);if(i===0)handle(F,...p,"输入 x",(x,y)=>{set("x",x);set("y",y);});});
   result=(v.order?"B(Ax)":"A(Bx)")+" = ("+out.map(x=>f(x)).join(", ")+")";equation="A：横向缩放与剪切；B：旋转 θ。复合从右向左作用。";
  }else if(current==="spatial"){result=spatial();equation="绿色 u，蓝色 v，红色结果；相机转动不会改变空间向量。";
  }else if(current==="projection"){
   P=frame([-3.5,3.5,-3,3],undefined,true);const square=v.ux*v.ux+v.uy*v.uy,dotValue=v.ux*v.vx+v.uy*v.vy,coeff=dotValue/square,p=[coeff*v.ux,coeff*v.uy];vector(P,v.ux,v.uy,color.basis,"u");vector(P,v.vx,v.vy,color.input,"v");
   if(square>1e-10){vector(P,...p,color.output,"projᵤ v");path([P.xy(v.vx,v.vy),P.xy(...p)],"#95a1a7",1.5,[4,4]);}
   handle(P,v.ux,v.uy,"测量方向",(x,y)=>{set("ux",x);set("uy",y);},color.basis);handle(P,v.vx,v.vy,"待测向量",(x,y)=>{set("vx",x);set("vy",y);});
   result="u · v = "+f(dotValue)+(square>1e-10?"；投影系数 = "+f(coeff)+"；投影 = ("+p.map(x=>f(x)).join(", ")+")":"；u=0，向该方向的投影公式未定义");equation="projᵤ v = (u·v)/(u·u) u，条件是 u ≠ 0。";
  }else if(current==="eigen"){
   P=frame([-4,4,-3.5,3.5],undefined,true);const x=[Math.cos(v.theta),Math.sin(v.theta)],A=[v.a,v.b,v.b,v.d],out=mul(A,x),center=(v.a+v.d)/2,offset=Math.hypot((v.a-v.d)/2,v.b),angle=.5*Math.atan2(2*v.b,v.a-v.d);
   [angle,angle+Math.PI/2].forEach(t=>path([P.xy(-4*Math.cos(t),-4*Math.sin(t)),P.xy(4*Math.cos(t),4*Math.sin(t))],"#9caeb6",1,[5,4]));vector(P,...x,color.input,"v");vector(P,...out,color.output,"A v");handle(P,...x,"输入方向",(x,y)=>set("theta",(Math.atan2(y,x)+2*Math.PI)%(2*Math.PI)));
   result="λ₁ = "+f(center+offset)+"；λ₂ = "+f(center-offset)+"；det[v,Av] = "+f(x[0]*out[1]-x[1]*out[0]);equation="A = [ "+f(v.a)+"  "+f(v.b)+" ; "+f(v.b)+"  "+f(v.d)+" ]（实对称矩阵）";
  }else if(current==="derivative"){
   P=frame([-2,3,v.family===4?-3:-2,v.family===3?16:9]);curve(P,fun,color.basis);const y=fun(v.a),z=fun(v.a+v.h),slope=v.h===0?NaN:(z-y)/v.h,der=df(v.a);
   curve(P,x=>y+der*(x-v.a),color.input,1.8);if(Number.isFinite(slope))curve(P,x=>y+slope*(x-v.a),color.output,2);
   if(Number.isFinite(y))handle(P,v.a,y,"固定点",x=>set("a",x));if(Number.isFinite(z))handle(P,v.a+v.h,z,"移动点",x=>set("h",x-v.a),color.output);
   result="差商 = "+f(slope)+(v.h===0?"（h=0）":"")+"；导数 = "+f(der)+"；Δx = "+f(v.h)+"；Δy = "+f(z-y);equation="橙色割线读有限增量；绿色切线读当前位置的极限变化率。";
  }else if(current==="integral"){
   P=frame([0,3,0,9]);curve(P,x=>x*x,color.basis);let sum=0;const dx=v.b/v.n;clip(P,()=>{for(let i=0;i<v.n;i++){const x=i*dx,h=x*x;sum+=h*dx;polygon([[x,0],[x+dx,0],[x+dx,h],[x,h]].map(p=>P.xy(...p)),"#d39b3844");}});handle(P,v.b,v.b*v.b,"积分上限",x=>set("b",x),color.output);
   result="左端点和 = "+f(sum)+"；真实积分 = "+f(v.b**3/3)+"；低估量 = "+f(v.b**3/3-sum);equation="f(x)=x²，区间 [0,b]；矩形宽度 Δx=b/n。";
  }else if(current==="gradient"){
   const pts=Models.gradient(v.w0,v.eta,v.k),r=Math.max(2.2,...pts.map(x=>Math.abs(x)*1.15));P=frame([-r,r,0,r*r]);curve(P,x=>x*x,color.basis);path(pts.map(x=>P.xy(x,x*x)),color.output,2);pts.forEach(x=>dot(P.xy(x,x*x),color.output));handle(P,v.w0,v.w0*v.w0,"起始参数",x=>set("w0",x));
   result="wₖ = "+f(pts.at(-1))+"；损失 = "+f(pts.at(-1)**2)+"；每步倍率 = "+f(1-2*v.eta);equation="L(w)=w²，wₖ₊₁=(1−2η)wₖ。";
  }else if(current==="network"){
   P=frame([-2,2,-.5,5]);const activation=x=>Math.max(0,v.w1*x+v.w2*v.x2+v.bias),z=v.w1*v.x1+v.w2*v.x2+v.bias,out=activation(v.x1),loss=(out-v.target)**2;
   curve(P,activation,color.basis);path([P.xy(-2,v.target),P.xy(2,v.target)],color.second,1.4,[5,4]);handle(P,v.x1,out,"输入 x₁",x=>set("x1",x));path([P.xy(v.x1,out),P.xy(v.x1,v.target)],color.output,3);
   result="z = "+f(z)+"；ŷ = "+f(out)+"；L = "+f(loss)+"；∂L/∂w₁ = "+(z===0?"折点处不适用通常导数":f(z>0?2*(out-v.target)*v.x1:0));equation="z=w₁x₁+w₂x₂+b → ŷ=max(0,z) → L=(ŷ−y)²。";
  }else if(current==="attention"){
   P=frame([0,12,0,1.15]);const a=Models.attention(v.delta,v.temp);[[2,a.w1,color.basis],[10,a.w2,color.second]].forEach(([x,y,c])=>polygon([[x-1,0],[x+1,0],[x+1,y],[x-1,y]].map(p=>P.xy(...p)),c+"77"));path([P.xy(2,0.08),P.xy(10,.08)],"#9da9ad",2);dot(P.xy(a.value,.08),color.output,6);
   handle(P,10,a.w2,"第二权重",(x,y)=>{const p=clamp(y,.001,.999);set("delta",v.temp*Math.log(p/(1-p)));},color.second);
   result="权重 = ("+f(a.w1)+", "+f(a.w2)+")；加权输出 = "+f(a.value);equation="分数 (0, Δ) 经 Softmax / T，汇总的值为 (2, 10)。";
  }else if(current==="noise"){
   const z=Math.sqrt(v.alpha)*v.clean+Math.sqrt(1-v.alpha)*v.epsilon,estimate=(z-Math.sqrt(1-v.alpha)*v.estimate)/Math.sqrt(v.alpha),r=Math.max(4,Math.abs(estimate)*1.35);P=frame([-r,r,-.5,3]);
   [[v.clean,2.4,color.input,"真实 x₀"],[z,1.4,color.basis,"带噪观测"],[estimate,.4,color.output,"重建 x̂₀"]].forEach(([x,y,c,label])=>{path([P.xy(-r,y),P.xy(r,y)],color.grid,1);dot(P.xy(x,y),c,7);text(P.xy(x,y)[0]+10,P.xy(x,y)[1]-10,label,c);});
   result="带噪值 = "+f(z)+"；重建 = "+f(estimate)+"；重建误差 = "+f(estimate-v.clean);equation="xₜ=√α x₀+√(1−α)ε；x̂₀=(xₜ−√(1−α)ε̂)/√α。";
  }else if(current==="heat"){
   P=frame([0,2*Math.PI,-1.7,1.7]);curve(P,x=>Math.exp(-v.t)*Math.sin(x),color.basis);curve(P,x=>v.amp*Math.exp(-v.n*v.n*v.t)*Math.sin(v.n*x),color.second);curve(P,x=>Models.heat(x,v.t,v.amp,v.n),color.sum,3);
   result="低频振幅 = "+f(Math.exp(-v.t))+"；高频振幅 = "+f(v.amp*Math.exp(-v.n*v.n*v.t));equation="u(x,t)=e⁻ᵗ sin x + A e⁻ⁿ²ᵗ sin(nx)，周期边界，扩散系数 1。";
  }else if(current==="phase"){
   const amp=Math.exp(v.lambda*v.t)*Math.hypot(v.x0,v.y0),r=Math.max(2,amp*1.2);P=frame([-r,r,-r,r],undefined,true);
   clip(P,()=>{for(let x=-r;x<=r;x+=r/3)for(let y=-r;y<=r;y+=r/3){const dx=v.lambda*x-v.omega*y,dy=v.omega*x+v.lambda*y,n=Math.hypot(dx,dy)||1;arrow(P.xy(x,y),P.xy(x+dx/n*r*.11,y+dy/n*r*.11),"#a2b6bd",1);}});
   const point=t=>{const a=Math.exp(v.lambda*t),c=Math.cos(v.omega*t),s=Math.sin(v.omega*t);return [a*(c*v.x0-s*v.y0),a*(s*v.x0+c*v.y0)];};path(Array.from({length:150},(_,i)=>P.xy(...point(i*v.t/149))),color.output,2.7);handle(P,v.x0,v.y0,"初始状态",(x,y)=>{set("x0",x);set("y0",y);});dot(P.xy(...point(v.t)),color.output,5);
   result="状态 = ("+point(v.t).map(x=>f(x)).join(", ")+")；散度 = "+f(2*v.lambda)+"；二维旋度 = "+f(2*v.omega);equation="x′=λx−ωy，y′=ωx+λy；径向增长与旋转相互独立。";
  }else if(current==="complex"){
   const radius=v.r*Math.exp(v.sigma*v.theta),r=Math.max(2.2,radius*1.2);P=frame([-r,r,-r,r],undefined,true);const z=Models.rotate(v.theta,radius),points=Array.from({length:180},(_,i)=>{let t=i*2*Math.PI/179;return P.xy(...Models.rotate(t,v.r*Math.exp(v.sigma*t)));});clip(P,()=>path(points,"#adbbc2",1.5));vector(P,...z,color.input,"z");
   const velocity=[v.sigma*z[0]-z[1],z[0]+v.sigma*z[1]];arrow(P.xy(...z),P.xy(z[0]+.35*velocity[0],z[1]+.35*velocity[1]),color.basis,2);path([P.xy(z[0],0),P.xy(...z),P.xy(0,z[1])],"#a6b2b9",1,[4,4]);handle(P,...z,"复数位置",(x,y)=>{const t=(Math.atan2(y,x)+2*Math.PI)%(2*Math.PI);set("theta",t);set("r",Math.hypot(x,y)*Math.exp(-v.sigma*t));});
   result="z = "+f(z[0])+" + ("+f(z[1])+") i；|z| = "+f(radius);equation="z(θ)=r exp((σ+i)θ)；速度为 (σ+i)z。σ=0 时是纯旋转。";
  }else if(current==="iteration"){
   P=frame([0,4,0,4],undefined,true);curve(P,x=>Math.pow(v.base,x),color.basis);curve(P,x=>x,"#97a4ab",1.5);let x=v.start,segments=[P.xy(x,0)],count=0;
   for(let i=0;i<v.k;i++){let y=Math.pow(v.base,x);if(!Number.isFinite(y)||y>1000){x=Infinity;break;}segments.push(P.xy(x,y),P.xy(y,y));x=y;count++;}
   clip(P,()=>path(segments,color.output,1.8));handle(P,v.start,0,"迭代起点",x=>set("start",x));result="xₖ = "+(Number.isFinite(x)?f(x):"超过可显示范围")+"；已计算 "+count+" 步";equation="xₖ₊₁=b^(xₖ)；稳定性还要考察不动点附近的斜率。";
  }else if(current==="entropy"){
   P=frame([.01,.99,0,7]);const H=Models.entropy(v.p),ce=Models.crossEntropy(v.p,v.q);curve(P,q=>Models.crossEntropy(v.p,q),color.basis);path([P.xy(.01,H),P.xy(.99,H)],color.second,2);handle(P,v.q,ce,"模型概率",x=>set("q",x));
   result="H(p) = "+f(H,6)+" bit；H(p,q) = "+f(ce,6)+" bit；KL(p∥q) = "+f(ce-H,6)+" bit";equation="固定真实分布 (p,1−p)，比较模型分布 (q,1−q) 的平均编码代价。";
  }else if(current==="taylor"){
   P=frame([-2,2,-2,8]);curve(P,Math.exp,color.basis);curve(P,x=>Models.taylor(x,v.n),color.output);path([P.xy(v.x,Models.taylor(v.x,v.n)),P.xy(v.x,Math.exp(v.x))],color.second,3);handle(P,v.x,Math.exp(v.x),"观察位置",x=>set("x",x));
   result="exp(x) = "+f(Math.exp(v.x),6)+"；近似 = "+f(Models.taylor(v.x,v.n),6)+"；绝对误差 = "+f(Math.abs(Math.exp(v.x)-Models.taylor(v.x,v.n)),6);equation="Pₙ(x)=1+x+x²/2!+⋯+xⁿ/n!，展开中心为 0。";
  }
  $("equation").textContent=equation;const now=performance.now();if(!playing||now-lastRead>350){$("readout").textContent=result;lastRead=now;}
  for(const [key] of D[current].controls){const range=$("control-"+key),num=$("number-"+key);range.value=v[key];if(num&&document.activeElement!==num)num.value=f(v[key],5);}
  const previous=$("drag-target").value;$("drag-target").replaceChildren();handles.forEach((h,i)=>{let o=document.createElement("option");o.value=i;o.textContent=h.name;$("drag-target").append(o);});$("drag-target").value=previous||"0";$("drag-tools").hidden=!handles.length;
 }
 function stop(){playing=false;cancelAnimationFrame(raf);$("play").textContent="播放变化";$("play").setAttribute("aria-pressed","false");}
 function changed(){stepLabel="自由探索 · 参数已调整";$("step-status").textContent=stepLabel;document.dispatchEvent(new CustomEvent("experiment:changed"));}
 function select(id,initial=null){
  stop();current=Object.hasOwn(D,id)?id:"linear";v={};D[current].controls.forEach(c=>v[c[0]]=c[5]);if(initial)for(const [k,x] of Object.entries(initial))set(k,x);
  camera={zoom:1,x:0,y:0,yaw:.7,pitch:.65};$("lab-title").textContent=D[current].title;$("plot-hint").textContent=D[current].hint;canvas.setAttribute("aria-label",D[current].title+"。"+D[current].hint);root.dataset.current=current;root.querySelector('.open-lab').href=prefix+'lab.html#'+current;
  $("controls").replaceChildren();
  for(const [key,label,min,max,step,,choices] of D[current].controls){
   const wrap=document.createElement("div");wrap.className="parameter";const lab=document.createElement("label");lab.textContent=label;lab.htmlFor=choices?"control-"+key:"number-"+key;wrap.append(lab);
   const range=document.createElement(choices?"select":"input");range.id="control-"+key;
   if(choices)choices.forEach((name,i)=>{let o=document.createElement("option");o.value=i;o.textContent=name;range.append(o);});
   else{Object.assign(range,{type:"range",min,max,step});range.setAttribute("aria-label",label);const num=document.createElement("input");Object.assign(num,{type:"number",min,max,step,id:"number-"+key});num.addEventListener("input",()=>{if(num.value!==""&&Number.isFinite(num.valueAsNumber)){stop();set(key,num.valueAsNumber);changed();draw();}});num.addEventListener("change",()=>{num.value=f(v[key],5);draw();});wrap.append(num);}
   range.addEventListener("input",()=>{stop();set(key,Number(range.value));changed();draw();});wrap.append(range);$("controls").append(wrap);
  }
  $("presets").replaceChildren();Object.keys(D[current].presets).forEach((name,i)=>{const b=document.createElement("button");b.textContent="情形 "+(i+1);b.title=name;b.dataset.preset=name;b.addEventListener("click",()=>{changed();applyPreset(name,"预设情形 "+(i+1));});$("presets").append(b);});
  const scene=D[current].scene;$("movie-area").hidden=!scene;if(scene){$("movie").src=prefix+"media/"+scene+".mp4";$("movie").poster=prefix+"media/"+scene+".png";}else{$("movie").pause();$("movie").removeAttribute("src");}
  $("step-status").textContent="自由探索";document.querySelectorAll(".lab-menu a").forEach(a=>a.setAttribute("aria-current",a.hash==="#"+current?"true":"false"));draw();
 }
 function applyPreset(name,label){const preset=D[current].presets[name];if(!preset)return;stop();D[current].controls.forEach(c=>v[c[0]]=c[5]);for(const [key,x] of Object.entries(preset))set(key,x);camera={zoom:1,x:0,y:0,yaw:.7,pitch:.65};stepLabel=label||name;$("step-status").textContent=stepLabel;draw();}
 $("reset").addEventListener("click",()=>{select(current);changed();});
 $("play").addEventListener("click",()=>{if(playing){stop();draw();return;}playing=true;$("play").textContent="暂停";$("play").setAttribute("aria-pressed","true");changed();const animated=current==='spatial'&&v.mode!==1?'az':D[current].animate,control=D[current].controls.find(c=>c[0]===animated),[key,label,min,max,step]=control,start=performance.now();$("step-status").textContent='自动改变：'+label;
  function tick(time){if(!playing)return;const p=Math.min(1,(time-start)/6500);v[key]=clamp(min+Math.round(p*(max-min)/step)*step,min,max);draw();if(p===1){stop();draw();}else raf=requestAnimationFrame(tick);}raf=requestAnimationFrame(tick);
 });
 $("zoom-in").addEventListener("click",()=>{camera.zoom=clamp(camera.zoom*1.25,.3,5);draw();});$("zoom-out").addEventListener("click",()=>{camera.zoom=clamp(camera.zoom/1.25,.3,5);draw();});$("reset-view").addEventListener("click",()=>{camera={zoom:1,x:0,y:0,yaw:.7,pitch:.65};draw();});
 function coords(e){const r=canvas.getBoundingClientRect();return [e.clientX-r.left,e.clientY-r.top];}
 canvas.addEventListener("pointerdown",e=>{const [x,y]=coords(e),hit=handles.map((h,i)=>({i,d:Math.hypot(h.x-x,h.y-y)})).filter(p=>p.d<18).sort((a,b)=>a.d-b.d)[0];drag={handle:hit?handles[hit.i]:null,x,y,camera:{...camera}};canvas.focus();canvas.setPointerCapture(e.pointerId);stop();});
 canvas.addEventListener("pointermove",e=>{if(!drag)return;const [x,y]=coords(e);if(drag.handle){drag.handle.move(x,y);changed();}else if(current==="spatial"){camera.yaw=drag.camera.yaw+(x-drag.x)*.009;camera.pitch=clamp(drag.camera.pitch-(y-drag.y)*.009,-1.3,1.3);}else{camera.x=drag.camera.x-(x-drag.x)/width*6/camera.zoom;camera.y=drag.camera.y+(y-drag.y)/height*6/camera.zoom;}draw();});
 function endDrag(){drag=null;}canvas.addEventListener("pointerup",endDrag);canvas.addEventListener("pointercancel",endDrag);canvas.addEventListener("lostpointercapture",endDrag);
 canvas.addEventListener("keydown",e=>{const deltas={ArrowLeft:[-8,0],ArrowRight:[8,0],ArrowUp:[0,-8],ArrowDown:[0,8]};if(!deltas[e.key])return;const h=handles[Number($("drag-target").value)||0];if(h){e.preventDefault();stop();h.move(h.x+deltas[e.key][0],h.y+deltas[e.key][1]);changed();draw();}});
 canvas.addEventListener("wheel",e=>{if(document.activeElement!==canvas)return;e.preventDefault();camera.zoom=clamp(camera.zoom*(e.deltaY<0?1.1:1/1.1),.3,5);draw();},{passive:false});
 document.addEventListener("book:step",e=>{if(e.detail.demo!==current)select(e.detail.demo);applyPreset(e.detail.preset,e.detail.title);});
 const menu=document.getElementById("lab-menu");if(menu){Object.entries(D).forEach(([id,d])=>{let a=document.createElement("a");a.href="#"+id;a.textContent=d.title;menu.append(a);});window.addEventListener("hashchange",()=>select(location.hash.slice(1)));}
 window.BookExperiment={snapshot:()=>({demo:current,values:{...v},camera:{...camera},handles:handles.map(h=>({x:h.x,y:h.y,name:h.name})),playing}),select,applyPreset};
 select(current,JSON.parse(root.dataset.initial||"null"));new ResizeObserver(draw).observe(canvas);
})();
