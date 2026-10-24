"use strict";
// Exact finite formulas for the teaching models; floating-point evaluation.
const Models = {
  matrix(a,b,c,d,t=1) {return [1+t*(a-1),t*b,t*c,1+t*(d-1)];},
  apply(A,x,y) {return [A[0]*x+A[1]*y,A[2]*x+A[3]*y];},
  determinant(A) {return A[0]*A[3]-A[1]*A[2];},
  secant(a,h) {return 2*a+h;},
  riemann(n) {let sum=0;const dx=2/n;for(let i=0;i<n;i++)sum+=(i*dx)**2*dx;return sum;},
  gradient(w,eta,n) {const points=[w];for(let i=0;i<n;i++){w=(1-2*eta)*w;points.push(w);}return points;},
  attention(delta,temp) {const z=delta/temp;const w=z>=0?1/(1+Math.exp(-z)):Math.exp(z)/(1+Math.exp(z));return {w1:1-w,w2:w,value:2*(1-w)+10*w};},
  heat(x,t,amp,n) {return Math.exp(-t)*Math.sin(x)+amp*Math.exp(-n*n*t)*Math.sin(n*x);},
  rotate(theta,r) {return [r*Math.cos(theta),r*Math.sin(theta)];},
  entropy(p) {return p<=0||p>=1?0:-p*Math.log2(p)-(1-p)*Math.log2(1-p);},
  crossEntropy(p,q) {if(q===0)return p===0?0:Infinity;if(q===1)return p===1?0:Infinity;return -p*Math.log2(q)-(1-p)*Math.log2(1-q);},
  taylor(x,n) {let sum=1,term=1;for(let k=1;k<=n;k++){term*=x/k;sum+=term;}return sum;}
};
if(typeof module!=="undefined")module.exports=Models;
