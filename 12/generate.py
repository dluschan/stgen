import random, sys, json, hmac, hashlib

def bytes(x):
    assert (2 ** 24 <= x < 2 ** 32)
    ranks = [24, 16, 8, 0]
    return '.'.join(map(lambda k: str(x >> k & 0xff), ranks))

def netmask(k):
    assert (0 < k < 32)
    return (2 ** 32 - 1) << (32 - k) & 0xFFFFFFFF

def network(x, mask):
    assert (2 ** 24 <= x < 2 ** 32)
    return x & mask

def bigbit(x):
    assert (x)
    k = 0
    while x:
        x //= 2
        k += 1
    return k - 1

def get(determinated=False):
    ip = random.randint(2 ** 24, 2 ** 32 - 1)
    ones = random.randint(32 - bigbit(ip), 30)
    if determinated:
        ip |= 3 << (31 - ones)
    mask = netmask(ones)
    net = network(ip, mask)
    return (ones, ip, mask, net, bytes(ip), bytes(mask), bytes(net))

def override(ip, net):
    return [mask for mask in range(1, 32) if network(ip, netmask(mask)) == net]

text = """В терминологии сетей TCP/IP маской сети называется двоичное число, определяющее, какая часть IP-адреса узла сети относится к адресу сети, а какая — к адресу самого узла в этой сети. При этом в маске сначала (в старших разрядах) стоят единицы, а затем с некоторого места — нули. Обычно маска записывается по тем же правилам, что и IP-адрес — в виде четырёх байтов, причём каждый байт записывается в виде десятичного числа. Адрес сети получается в результате применения поразрядной конъюнкции к заданному IP-адресу узла и маске.
Например, если IP-адрес узла равен {ip_sample}, а маска равна {mask_sample}, то адрес сети равен {net_sample}."""

q0 = " Определите адрес сети, если адрес компьютера в этой сети {ip}, а маска сети {mask}. В качестве ответа укажите сумму всех байт адреса сети в виде десятичного числа."

d0 = " Для узла с IP-адресом {ip} адрес сети равен {net}."
q1 = " Определите чему равен {order} байт маски."

q2 = " Определите сколько компьютеров может быть в этой сети, если два служебные адреса: широковещательный и адрес сети — не используются компьютерами."

q3 = " Определите для скольких различных значений маски это возможно."

q4 = " Определите какое {extrem} значение может принимать {order} байт в маске сети."

q5 = " Определите какое {extrem} количество {digit} может быть в маске сети."

e0 = " Ответ запишите в виде десятичного числа."

order = [["первый слева", "четвёртый справа"], ["второй слева", "третий справа"], ["третий слева", "второй справа"],
         ["четвёртый слева", "первый справа"]]
extrem = [["максимальное", [max, min]], ["минимальное", [min, max]]]
digit = [["нулей", 1, lambda x: 32 - x], ["единиц", 0, lambda x: x]]

question = [q0, d0 + q1 + e0, d0 + q2, d0 + q3, d0 + q4 + e0, d0 + q5]

def generate():
    qtype = 0 if len(sys.argv) < 2 else int(sys.argv[1])
    n = 10 if len(sys.argv) < 3 else int(sys.argv[2])
    r = {"category": "$course$/ЕГЭ/Задача 12/Тип " + str(qtype), "question_type": "numerical", "questions": []}
    for i in range(n):
        sample = get()
        task = get(qtype in [1, 2])
        var_extrem = {0, 1}.pop()
        var_digit = {0, 1}.pop()
        masks = override(task[1], task[3])
        params = {"ip_sample": sample[4], "mask_sample": sample[5], "net_sample": sample[6], "ip": task[4],
                  "mask": task[5], "net": task[6], "order": random.choice(order[(task[0] - 1) // 8]), "extrem": extrem[var_extrem][0],
                  "digit": digit[var_digit][0]}
        ready_text = (text + question[qtype]).format(**params)
        answer = [sum(list(map(int, task[6].split('.')))), task[5].split('.')[(task[0] - 1) // 8], 2 ** (32 - task[0]) - 2,
                  len(masks), bytes(netmask(extrem[var_extrem][1][0](masks))).split('.')[(task[0] - 1) // 8],
                  digit[var_digit][2](extrem[var_extrem][1][digit[var_digit][1]](masks))]

        r["questions"].append({"question_name": "Задача №" + hmac.new(bytearray(task[4], 'utf-8'),
                                                                      bytearray('text', 'utf-8'),
                                                                      hashlib.sha1).hexdigest(),
                               "question_text": ready_text, "question_answer": answer[qtype]})
    return json.dumps(r)

if __name__ == "__main__":
    print(generate())
