import tkinter as tk
import re

# 폰트 및 크기 설정
FONT = ("맑은 고딕", 24)
LABEL_FONT = ("맑은 고딕", 18)

def parse_linear(expr):
    """일차식 파싱 함수 (ax+b, ax, b, x 등 모든 형태 허용)"""
    expr = expr.replace(' ', '')
    if expr == '':
        return None
    # x만 있을 때
    if expr == 'x':
        return (1, 0)
    if expr == '-x':
        return (-1, 0)
    if expr == '+x':
        return (1, 0)
    # 상수만 있을 때
    if re.fullmatch(r'[+-]?\d+', expr):
        return (0, int(expr))
    # ax 형태
    m = re.fullmatch(r'([+-]?\d*)x', expr)
    if m:
        a = m.group(1)
        a = int(a) if a not in ('', '+', '-') else (1 if a in ('', '+') else -1)
        return (a, 0)
    # ax+b 형태
    m = re.fullmatch(r'([+-]?\d*)x([+-]\d+)', expr)
    if m:
        a = m.group(1)
        a = int(a) if a not in ('', '+', '-') else (1 if a in ('', '+') else -1)
        b = int(m.group(2))
        return (a, b)
    return None

def multiply_linear(expr1, expr2):
    """두 일차식 곱셈 연산"""
    p1 = parse_linear(expr1)
    p2 = parse_linear(expr2)
    if not p1 or not p2:
        return '잘못된 입력'
    a1, b1 = p1
    a2, b2 = p2
    # (a1x+b1)*(a2x+b2) = a1a2 x^2 + (a1b2+a2b1)x + b1b2
    c2 = a1*a2
    c1 = a1*b2 + a2*b1
    c0 = b1*b2
    result = []
    if c2 != 0:
        result.append(f"{'' if c2 == 1 else '-' if c2 == -1 else c2}x²")
    if c1 != 0:
        sign = '+' if c1 > 0 and result else ('-' if c1 < 0 else '')
        coeff = '' if abs(c1) == 1 else str(abs(c1))
        result.append(f"{sign}{coeff}x")
    if c0 != 0 or not result:
        sign = '+' if c0 > 0 and result else ('-' if c0 < 0 else '')
        result.append(f"{sign}{abs(c0)}")
    return ''.join(result)

class MathNode:
    def __init__(self, canvas, x, y, text):
        self.canvas = canvas
        self.rect = canvas.create_rectangle(x-90, y-45, x+90, y+45, fill="#E1F5FE", outline="#90A4AE", width=4)
        self.entry = tk.Entry(canvas, justify='center', font=FONT)
        self.entry.insert(0, text)
        self.window = canvas.create_window(x, y, window=self.entry, width=150, height=50)
        self.lines = []
        self._drag_data = {"x": 0, "y": 0, "items": [self.rect, self.window]}
        self.bind_events()
        
    def bind_events(self):
        for item in [self.rect, self.window]:
            self.canvas.tag_bind(item, "<Button-1>", self.start_drag)
            self.canvas.tag_bind(item, "<B1-Motion>", self.on_drag)
            
    def start_drag(self, event):
        self._drag_data = {
            "x": event.x,
            "y": event.y,
            "items": [self.rect, self.window]
        }
        
    def on_drag(self, event):
        dx = event.x - self._drag_data["x"]
        dy = event.y - self._drag_data["y"]
        if "items" in self._drag_data:
            for item in self._drag_data["items"]:
                self.canvas.move(item, dx, dy)
        else:
            self.canvas.move(self.rect, dx, dy)
            self.canvas.move(self.window, dx, dy)
        for line in self.lines:
            line.update_position()
        self._drag_data = {
            "x": event.x,
            "y": event.y,
            "items": self._drag_data["items"]
        }
    
    def get_center(self):
        x1, y1, x2, y2 = self.canvas.coords(self.rect)
        return ((x1+x2)//2, (y1+y2)//2)

class ConnectionLine:
    def __init__(self, canvas, node1, node2, label):
        self.canvas = canvas
        self.node1 = node1
        self.node2 = node2
        self.label = label
        self.line = None
        node1.lines.append(self)
        node2.lines.append(self)
        self.update_position()
        
    def update_position(self):
        x1, y1 = self.node1.get_center()
        x2, y2 = self.node2.get_center()
        if self.line:
            self.canvas.coords(self.line, x1, y1, x2, y2)
        else:
            self.line = self.canvas.create_line(x1, y1, x2, y2, width=4, fill="#78909C")
        self.update_label()
        
    def update_label(self):
        expr1 = self.node1.entry.get()
        expr2 = self.node2.entry.get()
        result = multiply_linear(expr1, expr2)
        self.label.config(text=f"({expr1}) × ({expr2}) = {result}")

# GUI 설정
root = tk.Tk()
root.title("분배법칙 시각화 도구")
canvas = tk.Canvas(root, width=1200, height=1000, bg="white")
canvas.pack(expand=True, fill=tk.BOTH)

# 노드 생성 (9개로 확장)
nodes = [
    MathNode(canvas, 250, 150, "2x"),
    MathNode(canvas, 750, 150, "3"),
    MathNode(canvas, 350, 350, "x"),
    MathNode(canvas, 650, 350, "5"),
    MathNode(canvas, 950, 350, "4"),
    MathNode(canvas, 850, 550, "6"),
    MathNode(canvas, 200, 550, "7"),
    MathNode(canvas, 500, 550, "8"),
    MathNode(canvas, 650, 750, "9")
]

# 결과 라벨 생성 (9개로 확장)
labels = [tk.Label(root, font=LABEL_FONT) for _ in range(9)]
for label in labels:
    label.pack(pady=6)

# 연결 설정 (9개로 확장)
connections = [
    ConnectionLine(canvas, nodes[0], nodes[2], labels[0]),
    ConnectionLine(canvas, nodes[0], nodes[3], labels[1]),
    ConnectionLine(canvas, nodes[1], nodes[2], labels[2]),
    ConnectionLine(canvas, nodes[1], nodes[3], labels[3]),
    ConnectionLine(canvas, nodes[1], nodes[4], labels[4]),
    ConnectionLine(canvas, nodes[3], nodes[5], labels[5]),
    ConnectionLine(canvas, nodes[2], nodes[6], labels[6]),
    ConnectionLine(canvas, nodes[3], nodes[7], labels[7]),
    ConnectionLine(canvas, nodes[5], nodes[8], labels[8]),
]

for conn in connections:
    conn.update_label()

for node in nodes:
    node.entry.bind("<KeyRelease>", lambda e: [conn.update_label() for conn in connections])

def add_quadratics(expr1, expr2):
    """두 식의 덧셈 연산 (일차식/이차식 지원, 여러 항도 지원)"""
    import re

    def parse_quadratic(expr):
        expr = expr.replace(' ', '')
        # 항목별 분리 (예: 3x+10x+5 → ['3x', '+10x', '+5'])
        terms = re.findall(r'[+-]?\d*x²|[+-]?\d*x(?!²)|[+-]?\d+', expr)
        a = b = c = 0
        for term in terms:
            if 'x²' in term:
                coeff = term.replace('x²', '')
                if coeff in ('', '+'):
                    a += 1
                elif coeff == '-':
                    a += -1
                else:
                    a += int(coeff)
            elif 'x' in term:
                coeff = term.replace('x', '')
                if coeff in ('', '+'):
                    b += 1
                elif coeff == '-':
                    b += -1
                else:
                    b += int(coeff)
            else:
                c += int(term)
        return [a, b, c]

    q1 = parse_quadratic(expr1)
    q2 = parse_quadratic(expr2)
    a = q1[0] + q2[0]
    b = q1[1] + q2[1]
    c = q1[2] + q2[2]
    result = []
    if a != 0:
        if a == 1:
            result.append("x²")
        elif a == -1:
            result.append("-x²")
        else:
            result.append(f"{a}x²")
    if b != 0:
        if result:
            if b > 0:
                if b == 1:
                    result.append("+x")
                else:
                    result.append(f"+{b}x")
            else:
                if b == -1:
                    result.append("-x")
                else:
                    result.append(f"{b}x")
        else:
            if b == 1:
                result.append("x")
            elif b == -1:
                result.append("-x")
            else:
                result.append(f"{b}x")
    if c != 0 or not result:
        if result and c > 0:
            result.append(f"+{c}")
        else:
            result.append(f"{c}")
    return ''.join(result)

def update_result_rectangles(event=None):
    expr1 = nodes[0].entry.get()
    expr3 = nodes[2].entry.get()
    result7 = multiply_linear(expr1, expr3)
    expr2 = nodes[1].entry.get()
    expr4 = nodes[3].entry.get()
    result8 = multiply_linear(expr2, expr4)
    result5 = multiply_linear(expr2, expr3)
    result6 = multiply_linear(expr1, expr4)
    update_entry(nodes[6].entry, result7)
    update_entry(nodes[7].entry, result8)
    update_entry(nodes[4].entry, result5)
    update_entry(nodes[5].entry, result6)
    result9 = add_quadratics(result5, result6)
    update_entry(nodes[8].entry, result9)

def update_entry(entry, value):
    state = entry.cget('state')
    entry.config(state='normal')
    entry.delete(0, tk.END)
    entry.insert(0, value)
    entry.config(state=state)

for i in range(4, 9):
    nodes[i].entry.config(state='readonly')

for i in range(4):
    nodes[i].entry.bind("<KeyRelease>", update_result_rectangles)

update_result_rectangles()

root.mainloop()
