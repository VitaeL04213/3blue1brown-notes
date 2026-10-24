const assert = require("node:assert/strict");
const M = require("../docs/assets/models.js");
const near = (a,b,e=1e-10) => assert.ok(Math.abs(a-b)<e, a+" != "+b);
// Independent geometric and analytic invariants for the teaching examples.
near(M.determinant([1,3,0,1]),1);
near(M.determinant([1,2,2,4]),0);
assert.deepEqual(M.apply(M.matrix(2,1,0,3,0),3,4),[3,4]);
for(const a of [-1.2,0,2])for(const h of [-.4,.1,.7])
  near(M.secant(a,h),((a+h)**2-a*a)/h);
let previous=0;
for(const n of [2,4,8,16,32,64]){const value=M.riemann(n);assert(value>previous&&value<8/3);previous=value;}
near(M.gradient(3,.5,1)[1],0);
assert(M.gradient(3,1.1,8).at(-1)>3);
for(const d of [-5,0,5])for(const t of [.2,1,3]){
 const a=M.attention(d,t);near(a.w1+a.w2,1);assert(a.value>=2&&a.value<=10);
}
for(const x of [0,.5,2,Math.PI])near(M.heat(x,0,.5,3),Math.sin(x)+.5*Math.sin(3*x));
for(const angle of [0,.5,Math.PI,2*Math.PI]){
 const z=M.rotate(angle,1.7);near(z[0]**2+z[1]**2,1.7**2);
}
near(M.entropy(.5),1);near(M.entropy(0),0);near(M.entropy(1),0);
for(const p of [.1,.3,.5,.9])for(const q of [.01,.2,.5,.99])
 assert(M.crossEntropy(p,q)>=M.entropy(p)-1e-12);
for(const p of [.1,.3,.5,.9])near(M.crossEntropy(p,p),M.entropy(p));
assert.equal(M.crossEntropy(.5,0),Infinity);
near(M.taylor(0,8),1);near(M.taylor(1,2),2.5);
assert(Math.abs(Math.exp(.2)-M.taylor(.2,8))<1e-10);
console.log("All 9 mathematical model checks passed.");
