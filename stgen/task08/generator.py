from random import randint
import subprocess, json, sys, hmac, hashlib

task = 'Запишите число, которое будет напечатано в результате выполнения следующей программы. Для Вашего удобства программа представлена на четырёх языках программирования.'

code = {'Basic':
"""DIM s, n AS INTEGER
s = {0}
n = {1}
WHILE n < {2}
    s = s {5} {3}
    n = n {6} {4}
WEND
PRINT s""", 'Python': """s = {0}
n = {1}
while n < {2}:
    s {5}= {3}
    n {6}= {4}
print(s)""", 'Pascal': """var s, n: integer;
begin
    s := {0};
    n := {1};
    while n < {2} do
    begin
        s := s {5} {3};
        n := n {6} {4};
    end;
    writeln(s);
end.""", 'C++': """#include &lt;iostream&gt;
int main()
{{
    int s = {0};
    int n = {1};
    while (n < {2})
    {{
        s {5}= {3};
        n {6}= {4};
    }}
    std::cout << s;
    return 0;
}}"""}

def generate():
	r = {"category": "ЕГЭ по информатике задача 8", "question_type": "numerical", "questions": []}
	for i in range(10 if len(sys.argv) == 1 else int(sys.argv[1])):
		a = randint(-10**3, 10**3)
		b = randint(-10**3, 10**3)
		c = randint(-10**3, 10**3)
		d = randint(-10**3, 10**3)
		e = randint(-10**3, 10**3)
		var1 = randint(0, 1)
		var2 = randint(0, 1)

		if var1:
			sign3, sign5 = +1, "+"
		else:
			sign3, sign5 = -1, "-"

		if var2:
			sign4, sign6 = +1, "+"
		else:
			sign4, sign6 = -1, "-"

		ans = a + max((c - b + e - 1) // e, 0) * d

		argv = list(map(str, [a, b, c, sign3*d, sign4*e, sign5, sign6]))
		result = """<table border=1px>
    <tbody>
        <tr align="center"><td>{0}</td><td>{2}</td></tr>
        <tr><td><pre>{1}</pre></td><td><pre>{3}</pre></td></tr>
        <tr align="center"><td>{4}</td><td>{6}</td></tr>
        <tr><td><pre>{5}</pre></td><td><pre>{7}</pre></td></tr>
    </tbody>
</table>"""
		argtable = []
		for x in code:
			argtable += [x, code[x].format(*argv)]

		r["questions"].append({"question_name": "Задача №" + hmac.new(bytearray(''.join(argv), 'utf-8'), bytearray('text','utf-8'), hashlib.sha1).hexdigest(), "question_text": task + result.format(*argtable), "question_answer": str(ans)})
	return json.dumps(r)

if __name__ == '__main__':
	print(generate())