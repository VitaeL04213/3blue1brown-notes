"""Original teaching animations. Render with Manim Community 0.19.0.

Text uses Pango, so no external LaTeX executable is required for these scenes.
All plotted objects are generated here; no original course media is copied.
"""
from manim import *
import numpy as np
import os

FONT = os.environ.get('TEXTBOOK_FONT', 'Microsoft YaHei')
BG = '#101e31'
TEAL = '#54d5d0'
GOLD = '#ffd27a'
config.background_color = BG


class TeachingScene(Scene):
    def heading(self, title, subtitle):
        self.add(Text(title, font=FONT, font_size=33).to_edge(UP, buff=.25))
        self.add(Text(subtitle, font=FONT, font_size=22, color=GOLD).to_edge(DOWN, buff=.23))

    def axes(self, xr, yr, width=9, height=4.8):
        a = Axes(x_range=xr, y_range=yr, x_length=width, y_length=height,
                 axis_config={'include_tip': False, 'color': GREY_B})
        self.add(a)
        return a


class LinearMap(TeachingScene):
    def construct(self):
        self.heading('矩阵的列决定基向量的去向', '先预测：剪切改变面积吗？两列平行后又会怎样？')
        p = NumberPlane(x_range=[-3, 3, 1], y_range=[-2, 2, 1],
                        x_length=8, y_length=4.8, background_line_style={'stroke_opacity': .35})
        square = Polygon(p.c2p(0,0),p.c2p(1,0),p.c2p(1,1),p.c2p(0,1),
                         color=GOLD, fill_opacity=.3)
        u = Arrow(p.c2p(0,0),p.c2p(1,0),buff=0,color=TEAL)
        v = Arrow(p.c2p(0,0),p.c2p(0,1),buff=0,color=GOLD)
        self.add(p,square,u,v)
        group=VGroup(p,square,u,v)
        self.wait(1)
        self.play(group.animate.apply_matrix([[1,.8],[0,1]]),run_time=3)
        self.wait(1)
        self.play(group.animate.apply_matrix([[1,0],[0,0]]),run_time=3)
        self.wait(2)


class Derivative(TeachingScene):
    def construct(self):
        self.heading('割线怎样接近切线', 'f(x) = x²，a = 1；差商 = 2 + h，h 始终不取零')
        a=self.axes([-1,3,1],[-1,7,1]); self.add(a.plot(lambda x:x*x,x_range=[-.8,2.5],color=TEAL))
        h=ValueTracker(1.4)
        sec=always_redraw(lambda:Line(a.c2p(.5,1+(2+h.get_value())*(-.5)),
                                     a.c2p(2.4,1+(2+h.get_value())*1.4),color=GOLD))
        dot=always_redraw(lambda:Dot(a.c2p(1+h.get_value(),(1+h.get_value())**2),color=GOLD))
        tangent=DashedLine(a.c2p(.5,0),a.c2p(2.4,3.8),color=WHITE)
        self.add(tangent,sec,dot,Dot(a.c2p(1,1),color=TEAL));self.wait(1)
        self.play(h.animate.set_value(.025),run_time=5,rate_func=smooth);self.wait(2)


class Integral(TeachingScene):
    def construct(self):
        self.heading('累积面积来自越来越细的小矩形', '左端点和：∑ f(xᵢ) Δx；本例 f(x) = x²，区间 [0, 2]')
        a=self.axes([0,2.5,.5],[0,5,1]);f=a.plot(lambda x:x*x,x_range=[0,2],color=TEAL);self.add(f)
        r=a.get_riemann_rectangles(f,x_range=[0,2],dx=.5,input_sample_type='left',
                                  color=[TEAL,GOLD],fill_opacity=.5,stroke_width=1)
        self.play(Create(r));self.wait(1)
        for step in [.25,.125,.0625]:
            new=a.get_riemann_rectangles(f,x_range=[0,2],dx=step,input_sample_type='left',
                                        color=[TEAL,GOLD],fill_opacity=.5,stroke_width=1)
            self.play(Transform(r,new),run_time=1.5)
        self.wait(2)


class GradientDescent(TeachingScene):
    def construct(self):
        self.heading('梯度给方向，步长决定走多远', 'L(w) = w²，η = 0.2；每步 w ← 0.6 w')
        a=self.axes([-3.5,3.5,1],[-.5,10,2]);self.add(a.plot(lambda x:x*x,x_range=[-3,3],color=TEAL))
        w=3.;dot=Dot(a.c2p(w,w*w),color=GOLD);self.add(dot);self.wait(1)
        for _ in range(7):
            nxt=.6*w
            path=Line(a.c2p(w,w*w),a.c2p(nxt,nxt*nxt),color=GOLD,stroke_opacity=.6)
            self.play(Create(path),dot.animate.move_to(a.c2p(nxt,nxt*nxt)),run_time=.7);w=nxt
        self.wait(2)


class Attention(TeachingScene):
    def construct(self):
        self.heading('注意力汇总：分数变权重，权重组合值', '玩具示例：两个值 2 与 10；权重相加为 1，输出留在两者之间')
        a=self.axes([0,12,2],[0,1.4,.2],width=10,height=3.5)
        w=ValueTracker(.25)
        bars=always_redraw(lambda:VGroup(
            Line(a.c2p(2,0),a.c2p(2,1-w.get_value()),color=TEAL,stroke_width=32),
            Line(a.c2p(10,0),a.c2p(10,w.get_value()),color=GOLD,stroke_width=32)))
        output=always_redraw(lambda:Dot(a.c2p(2*(1-w.get_value())+10*w.get_value(),.03),color=WHITE,radius=.12))
        self.add(bars,output)
        self.add(Text('值 2',font=FONT,font_size=22,color=TEAL).next_to(a.c2p(2,0),DOWN))
        self.add(Text('值 10',font=FONT,font_size=22,color=GOLD).next_to(a.c2p(10,0),DOWN))
        self.wait(1);self.play(w.animate.set_value(.85),run_time=3)
        self.play(w.animate.set_value(.15),run_time=3);self.wait(2)


class FourierHeat(TeachingScene):
    def construct(self):
        self.heading('热扩散优先抹平短波起伏', '周期边界，α = 1；sin(x) + 0.5 sin(3x) 中的高频衰减更快')
        a=self.axes([0,TAU,PI/2],[-1.6,1.6,.5]);t=ValueTracker(0)
        low=always_redraw(lambda:a.plot(lambda x:np.exp(-t.get_value())*np.sin(x),color=TEAL))
        high=always_redraw(lambda:a.plot(lambda x:.5*np.exp(-9*t.get_value())*np.sin(3*x),color=GOLD))
        total=always_redraw(lambda:a.plot(lambda x:np.exp(-t.get_value())*np.sin(x)+.5*np.exp(-9*t.get_value())*np.sin(3*x),color=WHITE))
        self.add(low,high,total);self.wait(1);self.play(t.animate.set_value(1.5),run_time=6);self.wait(2)


class ComplexRotation(TeachingScene):
    def construct(self):
        self.heading('乘以复指数：把角度相加', 'z = cos θ + i sin θ；位置与速度垂直，模长始终为 1')
        p=NumberPlane(x_range=[-1.5,1.5,.5],y_range=[-1.5,1.5,.5],x_length=5,y_length=5,
                      background_line_style={'stroke_opacity':.25})
        th=ValueTracker(0);self.add(p,Circle(radius=5/3,color=GREY_B))
        tip=lambda:p.c2p(np.cos(th.get_value()),np.sin(th.get_value()))
        arr=always_redraw(lambda:Arrow(p.c2p(0,0),tip(),buff=0,color=TEAL))
        vel=always_redraw(lambda:Arrow(tip(),tip()+.7*np.array([-np.sin(th.get_value()),np.cos(th.get_value()),0]),buff=0,color=GOLD))
        self.add(arr,vel);self.wait(1);self.play(th.animate.set_value(TAU),run_time=7,rate_func=linear);self.wait(1)


class Entropy(TeachingScene):
    def construct(self):
        self.heading('公平的二选一，平均信息量最大', 'H(p) = −p log₂ p − (1−p) log₂(1−p)；约定 0 log 0 = 0')
        a=self.axes([0,1,.2],[0,1.25,.25]);
        H=lambda p:0 if p<=0 or p>=1 else -p*np.log2(p)-(1-p)*np.log2(1-p)
        self.add(a.plot(H,x_range=[.001,.999],color=TEAL));p=ValueTracker(.02)
        dot=always_redraw(lambda:Dot(a.c2p(p.get_value(),H(p.get_value())),color=GOLD))
        self.add(dot);self.wait(1);self.play(p.animate.set_value(.5),run_time=3);self.wait(1)
        self.play(p.animate.set_value(.98),run_time=3);self.wait(1)


class Taylor(TeachingScene):
    def construct(self):
        self.heading('逐阶匹配局部信息', 'exp(x) 的 0 至 5 阶多项式；中心附近先贴合，远处误差仍需检查')
        a=self.axes([-2,2,1],[-1,6,1]);self.add(a.plot(np.exp,x_range=[-2,1.75],color=TEAL))
        import math
        curve=a.plot(lambda x:1,x_range=[-2,2],color=GOLD);self.add(curve);self.wait(1)
        for n in range(1,6):
            target=a.plot(lambda x,n=n:sum(x**k/math.factorial(k) for k in range(n+1)),x_range=[-2,1.75],color=GOLD)
            self.play(Transform(curve,target),run_time=1.2)
        self.wait(2)
