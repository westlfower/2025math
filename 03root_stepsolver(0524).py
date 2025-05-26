import tkinter as tk
import random

l_font=("Malgun Gothic",25)
e_font=("Malgun Gothic",25)
b_font=("Malgun Gothic",15)

def get_steps(a,b,c,d):

    if a==1:
        a_str=""
    elif a==-1:
        a_str="-"
    else:
        a_str=f"{a}"
        
    if b==1:
        b_str="+"
    elif b==-1:
        b_str="-"
    else:
        b_str=f"{b}" if b<0 else f"+{b}"
    c_str=f"{c}" if c<0 else f"+{c}"
    d_str=f"{d}" if d<0 else f"+{d}"
    return [ f"문제:{a_str}x\u00b2{b_str}x {c_str}={d}를 완전제곱식=상수로 표현하면?",
             f"1단계 양변을 x\u00b2의 계수로 나눈다.",f" {a}/{a}x\u00b2+({b}/{a})x+({c}/{a})={d}/{a}",
             f" 각항을 계산하면 {a/a}x\u00b2+({b/a})x+({c/a})={d/a}",
             f"2단계 상수항을 이항하면",
             f"{a/a}x\u00b2+({b/a})x={d/a}-({c/a})",
             f"{a/a}x\u00b2+({b/a})x={d/a-c/a}",
             f"3단계 (x항의 계수\u00d70.5)\u00b2을 양변에 더하면",
             f"{a/a}x\u00b2+({b/a})x+({b/a*0.5})\u00b2={d/a-c/a}+({b/a*0.5})\u00b2",
             f"4단계 좌변을 완전 제곱식으로 표현하면,",
             f"({a/a}x+{b/a*0.5})\u00b2={d/a-c/a}+({b/a*0.5})\u00b2"]

class QuadraticStepSolver:
    
    def __init__(self,root):
        self.root=root
        self.root.title("동암중학교 이차함수식의 계산")
        self.create_widgets()
        self.reset_problem()

    def create_widgets(self):
        frame_input=tk.Frame(self.root)
        frame_input.pack(pady=10)

        tk.Label(frame_input,text="a:",font=l_font).grid(row=0,column=0)
        self.entry_a=tk.Entry(frame_input,width=5, font=e_font)
        self.entry_a.insert(0,"2")
        self.entry_a.grid(row=0,column=1)
        tk.Label(frame_input,text="b:",font=l_font).grid(row=0,column=2)
        self.entry_b=tk.Entry(frame_input,width=5, font=e_font)
        self.entry_b.insert(0,"28")
        self.entry_b.grid(row=0,column=3)
        tk.Label(frame_input,text="c:",font=l_font).grid(row=0,column=4)
        self.entry_c=tk.Entry(frame_input,width=5, font=e_font)
        self.entry_c.insert(0,"-8")
        self.entry_c.grid(row=0,column=5)
        tk.Label(frame_input,text="d:",font=l_font).grid(row=0,column=6)
        self.entry_d=tk.Entry(frame_input,width=5, font=e_font)
        self.entry_d.insert(0,"-4")
        self.entry_d.grid(row=0,column=7)
        self.btn_random = tk.Button(frame_input, text="랜덤", command=self.set_random_abc, width=8, font=("Arial", 10, "bold"))
        self.btn_random.grid(row=0, column=8, padx=8)        


        #텍스트+스크롤프레임
        frame_text=tk.Frame(self.root)
        frame_text.pack(padx=10,pady=10,fill="both",expand=True)
        self.text=tk.Text(frame_text,height=7,width=30,font=l_font,bg="#f0f0f0")
        self.text.pack(side=tk.LEFT,fill="both",expand=True)

        scrollb=tk.Scrollbar(frame_text,orient=tk.VERTICAL,command=self.text.yview)
        scrollb.pack(side=tk.RIGHT,fill=tk.Y)

        self.text.config(yscrollcommand=scrollb.set)
        
        frame_btn=tk.Frame(self.root)
        frame_btn.pack(pady=5)

        self.btn_prev=tk.Button(frame_btn,text="이전 단계",command=self.prev_step,width=15,font=b_font)
        self.btn_prev.grid(row=0,column=0,padx=5)
        
        self.btn_reset=tk.Button(frame_btn,text="문제 리셋",command=self.reset_problem,width=15,font=b_font)
        self.btn_reset.grid(row=0,column=1,padx=5)

        self.btn_next=tk.Button(frame_btn,text="다음  단계",command=self.next_step,width=15,font=b_font)
        self.btn_next.grid(row=0,column=2,padx=5)


    def set_random_abc(self):
        # -3~3 중에서 a, b, c 각각 랜덤 선택
        self.entry_a.delete(0, tk.END)
        a_value=random.randint(2, 3)
        self.entry_a.insert(0, str(a_value))
        k_value=2*random.randint(7, 8)
        b_value=a_value*k_value
        c_value=a_value*random.randint(-5,-3)
        d_value=a_value*random.randint(3,5)
            
        self.entry_b.delete(0, tk.END)
        self.entry_b.insert(0, str(b_value))
        self.entry_c.delete(0, tk.END)
        self.entry_c.insert(0, str(c_value))
        self.entry_d.delete(0, tk.END)
        self.entry_d.insert(0, str(d_value))
        # 문제 자동 리셋
        self.reset_problem()

    def reset_problem(self):
        try:
            a = int(self.entry_a.get())
            b = int(self.entry_b.get())
            c = int(self.entry_c.get())
            d = int(self.entry_d.get())
        except ValueError:
            self.text.delete("1.0", "end")
            self.text.insert("end", "a, b, c, d에 정수를 입력하세요.\n")
            self.steps = []
            self.current_step = 0
            return
        self.steps = get_steps(a, b, c, d)
        self.current_step = 0
        self.text.delete("1.0", "end")
        self.text.insert("end", self.steps[0] + "\n")

    def next_step(self):
        if not self.steps:
            return
        if self.current_step < len(self.steps) - 1:
            self.current_step += 1
            self.text.insert("end", self.steps[self.current_step] + "\n")
            self.text.see("end")

    def prev_step(self):
        if not self.steps:
            return
        if self.current_step > 0:
            self.current_step -= 1
            content = self.text.get("1.0", "end").splitlines()
            content = content[:self.current_step + 1]
            self.text.delete("1.0", "end")
            for line in content:
                self.text.insert("end", line + "\n")
            self.text.see("end")
        

root=tk.Tk()

app=QuadraticStepSolver(root)
root.mainloop()
    
      

    
