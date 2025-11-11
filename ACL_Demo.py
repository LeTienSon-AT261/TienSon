import random

class Rule:
    def __init__(self, rule_id, latency):
        self.rule_id = rule_id
        self.latency = latency
        self.hit_rate = 1.0

    def __repr__(self):
        return f"R{self.rule_id}(λ={self.latency:.2f}, h={self.hit_rate:.2f})"

def expected_latency(rules):
    total = 0.0
    for i, r in enumerate(rules):
        cumulative = sum(x.latency for x in rules[:i+1])
        total += r.hit_rate * cumulative
    return total

def can_swap(i, j, D):
    return D[i][j] == 0 and D[j][i] == 0

# ---------------------- δ-opt có chuẩn hóa ----------------------
def delta_opt(rules, matched_index, D, theta=2, step=0, DSIZE=5):
    # B1: tăng hit-rate
    rules[matched_index].hit_rate *= theta

    # B2: kiểm tra trade-off + phụ thuộc
    if matched_index > 0 and can_swap(matched_index, matched_index - 1, D):
        r_i = rules[matched_index]
        r_prev = rules[matched_index - 1]
        if r_i.hit_rate * r_prev.latency > r_prev.hit_rate * r_i.latency:
            rules[matched_index-1], rules[matched_index] = rules[matched_index], rules[matched_index-1]

    # B3: chuẩn hóa định kỳ
    if step % DSIZE == 0:
        total_h = sum(r.hit_rate for r in rules)
        for r in rules:
            r.hit_rate /= total_h

# ---------------------- ε-opt ----------------------
def epsilon_opt(rules, matched_index, D):
    if matched_index > 0 and can_swap(matched_index, matched_index - 1, D):
        rules[matched_index-1], rules[matched_index] = rules[matched_index], rules[matched_index-1]

# ---------------------- DEMO ----------------------
random.seed(0)
rules_delta = [Rule(i, random.uniform(0.5, 1.0)) for i in range(1, 6)]
D = [[0 for _ in range(5)] for _ in range(5)]
D[0][1] = 1  # R1 phụ thuộc R2

print("Ban đầu (δ-opt):", rules_delta)

for step in range(1, 21):
    idx = random.randint(0, len(rules_delta)-1)
    delta_opt(rules_delta, idx, D, theta=2, step=step, DSIZE=5)
    if step % 5 == 0:
        print(f"Sau {step} packet (δ-opt): {rules_delta}, E = {expected_latency(rules_delta):.2f}")

# Reset và chạy ε-opt
rules_epsilon = [Rule(i, random.uniform(0.5, 1.0)) for i in range(1, 6)]
print("\nBan đầu (ε-opt):", rules_epsilon)

for step in range(1, 21):
    idx = random.randint(0, len(rules_epsilon)-1)
    epsilon_opt(rules_epsilon, idx, D)
    if step % 5 == 0:
        print(f"Sau {step} packet (ε-opt): {rules_epsilon}, E = {expected_latency(rules_epsilon):.2f}")
