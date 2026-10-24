"use strict";
const demos={
 linear:{title:"矩阵的列与面积",scene:"LinearMap",lesson:"linear-transformations",
 question:"先让两列平行，再让其中一列穿过另一侧：面积和定向分别怎样变化？",
 explanation:"蓝、黄箭头是两个基向量的像，白箭头是它们的和。网格显示同一个线性规则作用于许多输入。行列式记录有向面积倍率；绝对值才是普通面积倍率。",
 limits:"播放进度 t 展示从单位矩阵到目标矩阵的线性插值，中间阶段不一定可逆。灰色背景轴保持不动。",
 legend:"蓝：第一列　黄：第二列　白：T(1,1)　半透明区域：单位方形的像",
 controls:[["a","第一列：横坐标",-2,2,.1,1],["c","第一列：纵坐标",-2,2,.1,0],["b","第二列：横坐标",-2,2,.1,1],["d","第二列：纵坐标",-2,2,.1,1],["t","变换进度",0,1,.01,1]],animate:"t"},
 derivative:{title:"割线怎样接近切线",scene:"Derivative",lesson:"derivatives",
 question:"把 h 从正侧、负侧接近零，割线斜率是否到达同一个数？",
 explanation:"f(x)=x² 在 a 处的切线斜率是 2a；非零步长的差商恰为 2a+h。图上两点越靠近，割线越接近切线。",
 limits:"h=0 时原差商没有定义；此时只画切线并标为极限状态，不把两个零相除。",
 legend:"蓝：平方函数　黄：割线与移动点　白色虚线：切线",
 controls:[["a","固定点 a",-1.5,1.5,.05,.5],["h","步长 h（可正可负）",-1.5,1.5,.01,1]],animate:"h"},
 integral:{title:"矩形和与真实积分",scene:"Integral",lesson:"integration",
 question:"先预测左端点矩形和偏高还是偏低；把切分数加倍后误差怎样变化？",
 explanation:"每个矩形宽为 2/n，高为左端点的平方。由于 x² 在 [0,2] 递增，左端点和低估积分，真实值为 8/3。",
 limits:"此处演示等宽左端点求和；其他采样点、非单调函数的误差方向需要另行判断。",
 legend:"蓝：f(x)=x²　黄：左端点矩形　区间：[0,2]",
 controls:[["n","矩形个数",2,64,1,8]],animate:"n"},
 gradient:{title:"学习率与收敛",scene:"GradientDescent",lesson:"gradient-descent",
 question:"分别尝试 η=0.2、0.8、1.1，预测参数靠近零、振荡还是发散。",
 explanation:"L(w)=w²，更新为 w←(1−2η)w。0<η<1 时绝对值缩小；η=1 时来回翻号；η>1 时非零初值的绝对值增大。",
 limits:"这是一维二次损失的精确更新，不代表一般深度网络的收敛保证。坐标范围会随轨迹调整。",
 legend:"蓝：二次损失　黄：更新轨迹　白点：当前参数",
 controls:[["eta","学习率 η",0,1.4,.02,.2],["k","更新次数",0,12,1,4]],animate:"k"},
 attention:{title:"从分数到注意力权重",scene:"Attention",lesson:"attention",
 question:"只增加第二个键的匹配分数，哪个值对输出的影响会增加？温度又改变什么？",
 explanation:"两个分数取 0 与 Δ，温度 T>0。归一化指数给出两权重，再对值 2 与 10 加权。输出始终处在这两个值之间。",
 limits:"演示单头的标量值汇总；输出投影、多个头和残差之后不受同一个区间约束。",
 legend:"蓝柱：值 2 的权重　黄柱：值 10 的权重　白点：加权输出",
 controls:[["delta","第二个分数 − 第一个分数",-5,5,.1,1],["temp","温度 T",.2,3,.05,1]],animate:"delta"},
 heat:{title:"傅里叶模式与热扩散",scene:"FourierHeat",lesson:"heat-equation",
 question:"先增大第二个模式的频率，再推进时间；更细的起伏会保留更久吗？",
 explanation:"周期边界下 u=exp(−t)sin x+A exp(−n²t)sin(nx)，扩散系数为 1。每个正弦保持形状，只改变振幅；频率平方控制衰减速率。",
 limits:"这是两个模式的精确有限叠加，不证明任意初值的无限级数收敛。区间为 [0,2π]，使用周期边界。",
 legend:"蓝：低频　黄：高频　白：两模式之和",
 controls:[["t","时间 t",0,3,.01,0],["amp","高频初始振幅",-1,1,.05,.5],["n","高频频率",2,9,1,3]],animate:"t"},
 complex:{title:"复数乘法与旋转",scene:"ComplexRotation",lesson:"eulers-formula-dynamically",
 question:"旋转一整圈后坐标是否恢复？改变半径会改变角度吗？",
 explanation:"z=r(cos θ+i sin θ)。角度滑块改变旋转，半径滑块改变模长。黄箭头给出对 θ 的变化方向，与位置向量垂直。",
 limits:"黄箭头为便于观察缩短了长度；表示切向方向。真实导数对 θ 为 r(−sin θ,cos θ)。",
 legend:"蓝：位置向量　黄：切向方向　虚线：实部与虚部投影",
 controls:[["theta","角度 θ（弧度）",0,6.283185307,.01,1.05],["r","半径 r",.5,2,.05,1]],animate:"theta"},
 entropy:{title:"熵、交叉熵与模型失配",scene:"Entropy",lesson:"cross-entropy",
 question:"固定真实概率 p，只调模型概率 q。交叉熵在哪个位置最小？",
 explanation:"真实来源为 (p,1−p)，模型为 (q,1−q)。蓝线是固定 p 下随 q 变化的交叉熵；黄线是真实熵。两者之差是 KL 散度，单位均为 bit。",
 limits:"滑块限制在严格正概率范围内。若模型给真实可能事件零概率，代价应视为无穷，不能套有限实数值。",
 legend:"蓝：H(p,q) 随 q 的变化　黄：H(p)　白点：当前模型",
 controls:[["p","真实概率 p",.01,.99,.01,.5],["q","模型概率 q",.01,.99,.01,.75]],animate:"q"},
 taylor:{title:"逐阶匹配与局部近似",scene:"Taylor",lesson:"taylor-series",
 question:"固定阶数，把观察点移离零；误差怎样变化？再增加阶数比较。",
 explanation:"以零为中心，用 ∑ xᵏ/k! 近似 exp(x)。增加阶数匹配更多导数。当前观察点显示精确函数值、近似值和绝对误差。",
 limits:"展示区间为 [−2,2]，蓝线是数值指数函数；图形贴合不替代余项界，也不说明任意光滑函数都等于其泰勒级数。",
 legend:"蓝：exp(x)　黄：泰勒多项式　白色竖线：当前观察点",
 controls:[["n","多项式阶数",0,8,1,2],["x","观察点 x",-2,2,.05,1]],animate:"n"}
};
const $=id=>document.getElementById(id), canvas=$("plot"), ctx=canvas.getContext("2d");
const C={blue:"#54d5d0",gold:"#ffd27a",white:"#f5f8fa",grid:"#34475c"};
let current,values={},playing=false,raf=0,started=0,lastAnnounce=0;
const f=(x,d=4)=>Math.abs(x)>1e5?x.toExponential(3):Number(x.toFixed(d)).toString();
let view;
function xy(x,y){return [75+(x-view[0])/(view[1]-view[0])*750,390-(y-view[2])/(view[3]-view[2])*340];}
function line(x1,y1,x2,y2,color,width=2,dash=[]){let a=xy(x1,y1),b=xy(x2,y2);ctx.beginPath();ctx.setLineDash(dash);ctx.strokeStyle=color;ctx.lineWidth=width;ctx.moveTo(...a);ctx.lineTo(...b);ctx.stroke();ctx.setLineDash([]);}
function dot(x,y,color,r=5){ctx.beginPath();ctx.fillStyle=color;ctx.arc(...xy(x,y),r,0,2*Math.PI);ctx.fill();}
function text(x,y,s,color=C.white){ctx.fillStyle=color;ctx.font="17px sans-serif";ctx.fillText(s,x,y);}
function frame(x0,x1,y0,y1){
 view=[x0,x1,y0,y1];ctx.clearRect(0,0,900,460);ctx.fillStyle="#101e31";ctx.fillRect(0,0,900,460);
 for(let i=0;i<=4;i++){const x=x0+(x1-x0)*i/4,y=y0+(y1-y0)*i/4;
 line(x,y0,x,y1,C.grid,1);line(x0,y,x1,y,C.grid,1);
 text(xy(x,y0)[0]-14,421,f(x,2),"#bdcbd8");text(8,xy(x0,y)[1]+5,f(y,2),"#bdcbd8");}
 if(x0<=0&&x1>=0)line(0,y0,0,y1,"#8197aa",1.5);
 if(y0<=0&&y1>=0)line(x0,0,x1,0,"#8197aa",1.5);
}
function clipped(fn){ctx.save();ctx.beginPath();ctx.rect(75,50,750,340);ctx.clip();fn();ctx.restore();}
function curve(fn,color,width=3){clipped(()=>{ctx.beginPath();ctx.strokeStyle=color;ctx.lineWidth=width;
 for(let i=0;i<=500;i++){let x=view[0]+i/500*(view[1]-view[0]),p=xy(x,fn(x));if(i===0)ctx.moveTo(...p);else ctx.lineTo(...p);}ctx.stroke();});}
function arrow(x,y,color){line(0,0,x,y,color,3);const end=xy(x,y),start=xy(0,0);let a=Math.atan2(end[1]-start[1],end[0]-start[0]);ctx.beginPath();ctx.fillStyle=color;ctx.moveTo(...end);ctx.lineTo(end[0]-12*Math.cos(a-.4),end[1]-12*Math.sin(a-.4));ctx.lineTo(end[0]-12*Math.cos(a+.4),end[1]-12*Math.sin(a+.4));ctx.closePath();ctx.fill();}
function draw(){
 const v=values;let result="";
 if(current==="linear"){
  const A=Models.matrix(v.a,v.b,v.c,v.d,v.t),u=Models.apply(A,1,0),w=Models.apply(A,0,1),sum=Models.apply(A,1,1);
  const r=Math.max(2,Math.abs(sum[1])+.6,Math.abs(sum[0])*.453+.6,Math.abs(u[1])+.6,Math.abs(w[1])+.6);
  frame(-r*750/340,r*750/340,-r,r);
  clipped(()=>{for(let k=-4;k<=4;k++){let p=Models.apply(A,k,-4),q=Models.apply(A,k,4);line(...p,...q,"#365e72",1);p=Models.apply(A,-4,k);q=Models.apply(A,4,k);line(...p,...q,"#365e72",1);}
   ctx.beginPath();[[0,0],u,sum,w].forEach((p,i)=>i?ctx.lineTo(...xy(...p)):ctx.moveTo(...xy(...p)));ctx.closePath();ctx.fillStyle="#ffd27a44";ctx.fill();arrow(...u,C.blue);arrow(...w,C.gold);arrow(...sum,C.white);});
  let det=Models.determinant(A);result="当前矩阵 [ "+f(A[0],2)+"  "+f(A[1],2)+" ; "+f(A[2],2)+"  "+f(A[3],2)+" ]。det = "+f(det)+"，面积倍率 = "+f(Math.abs(det))+"；"+(Math.abs(det)<1e-10?"压扁，信息丢失":det<0?"定向翻转":"保持定向")+"。";
 }else if(current==="derivative"){
  frame(-3.2,3.2,-1,10);curve(x=>x*x,C.blue);
  clipped(()=>{line(-3.2,v.a*v.a+2*v.a*(-3.2-v.a),3.2,v.a*v.a+2*v.a*(3.2-v.a),C.white,2,[7,5]);
  if(Math.abs(v.h)>1e-10){let slope=Models.secant(v.a,v.h);line(-3.2,v.a*v.a+slope*(-3.2-v.a),3.2,v.a*v.a+slope*(3.2-v.a),C.gold);dot(v.a+v.h,(v.a+v.h)**2,C.gold);}
  dot(v.a,v.a*v.a,C.blue);});
  result=Math.abs(v.h)<1e-10?"h = 0：差商未定义；显示极限切线，斜率 = "+f(2*v.a):"割线斜率 = "+f(Models.secant(v.a,v.h))+"；切线斜率 = "+f(2*v.a)+"；差异 = "+f(v.h)+"。";
 }else if(current==="integral"){
  frame(0,2.2,0,4.6);let dx=2/v.n;
  for(let i=0;i<v.n;i++){let p=xy(i*dx,(i*dx)**2),q=xy((i+1)*dx,0);ctx.fillStyle="#ffd27a66";ctx.fillRect(p[0],p[1],q[0]-p[0],q[1]-p[1]);ctx.strokeStyle=C.gold;ctx.lineWidth=.8;ctx.strokeRect(p[0],p[1],q[0]-p[0],q[1]-p[1]);}
  curve(x=>x*x,C.blue);let sum=Models.riemann(v.n);result="左端点和 = "+f(sum,6)+"；真实积分 = 8/3 ≈ 2.666667；低估量 = "+f(8/3-sum,6)+"。";
 }else if(current==="gradient"){
  let pts=Models.gradient(3,v.eta,v.k),r=Math.max(3.5,...pts.map(x=>Math.abs(x)*1.15));
  frame(-r,r,-.05*r*r,r*r);curve(x=>x*x,C.blue);
  for(let i=1;i<pts.length;i++)line(pts[i-1],pts[i-1]**2,pts[i],pts[i]**2,C.gold,2);
  pts.forEach(x=>dot(x,x*x,C.gold,4));let w=pts.at(-1);dot(w,w*w,C.white,7);
  result="第 "+v.k+" 步：w = "+f(w,6)+"，L(w) = "+f(w*w,6)+"；每步损失倍率 (1−2η)² = "+f((1-2*v.eta)**2)+"。";
 }else if(current==="attention"){
  frame(0,12,0,1.2);let a=Models.attention(v.delta,v.temp);
  line(2,0,2,a.w1,C.blue,35);line(10,0,10,a.w2,C.gold,35);dot(a.value,.03,C.white,8);
  text(185,28,"值 2 的权重",C.blue);text(640,28,"值 10 的权重",C.gold);
  result="权重 = ("+f(a.w1)+", "+f(a.w2)+")；和 = 1；输出 = 2×"+f(a.w1)+" + 10×"+f(a.w2)+" = "+f(a.value)+"。";
 }else if(current==="heat"){
  frame(0,Math.PI*2,-2.1,2.1);curve(x=>Math.exp(-v.t)*Math.sin(x),C.blue);curve(x=>v.amp*Math.exp(-v.n*v.n*v.t)*Math.sin(v.n*x),C.gold);curve(x=>Models.heat(x,v.t,v.amp,v.n),C.white);
  result="低频振幅 = "+f(Math.exp(-v.t),6)+"；高频振幅 = "+f(v.amp*Math.exp(-v.n*v.n*v.t),6)+"；高频的衰减指数是低频的 "+v.n*v.n+" 倍。";
 }else if(current==="complex"){
  frame(-5.515,5.515,-2.5,2.5);let [x,y]=Models.rotate(v.theta,v.r);
  ctx.beginPath();ctx.strokeStyle=C.grid;ctx.lineWidth=2;ctx.arc(...xy(0,0),v.r*68,0,2*Math.PI);ctx.stroke();
  arrow(x,y,C.blue);line(x,y,x-.6*Math.sin(v.theta),y+.6*Math.cos(v.theta),C.gold,4);
  line(x,0,x,y,C.white,1,[5,5]);line(0,y,x,y,C.white,1,[5,5]);dot(x,y,C.gold);
  result="z = "+f(x)+" "+(y<0?"−":"+")+" "+f(Math.abs(y))+" i；|z| = "+f(Math.hypot(x,y))+"；θ = "+f(v.theta)+" rad。";
 }else if(current==="entropy"){
  const H=Models.entropy(v.p),ce=Models.crossEntropy(v.p,v.q);frame(.01,.99,0,7);
  curve(q=>Models.crossEntropy(v.p,q),C.blue);line(.01,H,.99,H,C.gold);dot(v.q,ce,C.white,7);
  result="H(p) = "+f(H,6)+" bit；H(p,q) = "+f(ce,6)+" bit；KL(p∥q) = "+f(ce-H,6)+" bit。";
 }else if(current==="taylor"){
  frame(-2,2,-2,8);curve(Math.exp,C.blue);curve(x=>Models.taylor(x,v.n),C.gold);
  line(v.x,-2,v.x,8,C.white,1,[4,5]);dot(v.x,Models.taylor(v.x,v.n),C.gold);dot(v.x,Math.exp(v.x),C.blue);
  let approx=Models.taylor(v.x,v.n);result="exp(x) = "+f(Math.exp(v.x),6)+"；"+v.n+" 阶近似 = "+f(approx,6)+"；绝对误差 = "+f(Math.abs(Math.exp(v.x)-approx),6)+"。";
 }
 if(!playing||performance.now()-lastAnnounce>350){$("readout").textContent=result;lastAnnounce=performance.now();}
 for(const [key] of demos[current].controls){$("value-"+key).textContent=f(values[key],3);$("control-"+key).value=values[key];}
}
function stop(){playing=false;cancelAnimationFrame(raf);$("play").textContent="播放变化";$("play").setAttribute("aria-pressed","false");}
function select(){
 stop();current=location.hash.slice(1);if(!demos[current])current="linear";const d=demos[current];values={};
 for(const [key,label,min,max,step,initial] of d.controls)values[key]=initial;
 $("title").textContent=d.title;$("question").textContent=d.question;$("explanation").textContent=d.explanation;$("limits").textContent=d.limits;$("legend").textContent=d.legend;
 $("plot").setAttribute("aria-label",d.title+"。"+d.legend+"。下方实时显示计算结果。");
 $("controls").replaceChildren();
 for(const [key,label,min,max,step] of d.controls){
  const wrap=document.createElement("div");wrap.className="control";
  const lab=document.createElement("label");lab.htmlFor="control-"+key;lab.textContent=label;
  const out=document.createElement("output");out.id="value-"+key;out.htmlFor="control-"+key;lab.append(out);
  const inp=document.createElement("input");Object.assign(inp,{type:"range",id:"control-"+key,min,max,step,value:values[key]});
  inp.addEventListener("input",()=>{stop();values[key]=Number(inp.value);draw();});wrap.append(lab,inp);$("controls").append(wrap);
 }
 document.querySelectorAll(".lab-menu a").forEach(a=>a.setAttribute("aria-current",a.hash==="#"+current?"true":"false"));
 $("lesson-link").innerHTML='<a href="lessons/'+d.lesson+'.html">回到相关课程：'+d.title+' →</a>';
 $("movie").pause();$("movie").src="media/"+d.scene+".mp4";$("movie").poster="media/"+d.scene+".png";$("movie").setAttribute("aria-label",d.title+"的原创 Manim 动画");
 $("movie-caption").textContent="原创 Manim 动画，无音频。"+d.explanation;
 $("movie-download").href="media/"+d.scene+".mp4";draw();
}
for(const [id,d] of Object.entries(demos)){const a=document.createElement("a");a.href="#"+id;a.textContent=d.title;$("lab-menu").append(a);}
$("reset").addEventListener("click",select);
$("play").addEventListener("click",()=>{
 if(playing){stop();draw();return;}
 playing=true;started=performance.now();$("play").textContent="暂停";$("play").setAttribute("aria-pressed","true");
 const control=demos[current].controls.find(c=>c[0]===demos[current].animate),[key,,min,max,step]=control;
 function tick(time){if(!playing)return;let u=(time-started)/7000;if(u>=1){values[key]=max;stop();draw();return;}
  values[key]=Math.min(max,min+Math.round(u*(max-min)/step)*step);draw();raf=requestAnimationFrame(tick);}
 raf=requestAnimationFrame(tick);
});
window.addEventListener("hashchange",select);select();
