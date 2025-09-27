import random

# ----------------------
# Lớp Rule đại diện cho 1 luật trong ACL
# ----------------------
class Rule:
    def __init__(self, rule_id, latency):
        self.rule_id = rule_id
        self.latency = latency
        self.hit_rate = 1.0  # hit-rate khởi tạo mặc định = 1

    def __repr__(self):
        return f"R{self.rule_id}(λ={self.latency:.2f}, h={self.hit_rate:.2f})"

# ----------------------
# Hàm tính latency kỳ vọng (Expected Latency E)
# ----------------------
def expected_latency(rules):
    total = 0.0
    for i, r in enumerate(rules):
        cumulative = sum(x.latency for x in rules[:i+1])
        total += r.hit_rate * cumulative
    return total

# ----------------------
# Thuật toán δ-opt (delta-opt)
# Ý tưởng: tăng hit-rate cho rule match, sau đó swap nếu trade-off có lợi
# ----------------------
def delta_opt(rules, matched_index, theta=2):
    # B1. tăng hit-rate của rule match
    rules[matched_index].hit_rate *= theta
    # B2. kiểm tra trade-off, nếu có lợi thì swap với rule ngay trước đó
    if matched_index > 0:
        r_i = rules[matched_index]
        r_prev = rules[matched_index - 1]
        if r_i.hit_rate * r_prev.latency > r_prev.hit_rate * r_i.latency:
            rules[matched_index-1], rules[matched_index] = rules[matched_index], rules[matched_index-1]

# ----------------------
# Thuật toán ε-opt (epsilon-opt)
# Ý tưởng: chỉ swap rule match với rule ngay trước nó, không cần tính toán hit-rate
# ----------------------
def epsilon_opt(rules, matched_index):
    if matched_index > 0:
        rules[matched_index-1], rules[matched_index] = rules[matched_index], rules[matched_index-1]

# ----------------------
# DEMO: tạo ACL và sinh traffic
# ----------------------
random.seed(0)

# ACL gồm 5 rule với latency ngẫu nhiên
rules_delta = [Rule(i, random.uniform(0.5, 1.0)) for i in range(1, 6)]
print("Ban đầu (δ-opt):", rules_delta)

# Sinh 20 packet, mỗi packet match 1 rule ngẫu nhiên
for step in range(1, 21):
    idx = random.randint(0, len(rules_delta)-1)
    delta_opt(rules_delta, idx)
    if step % 5 == 0:
        print(f"Sau {step} packet (δ-opt): {rules_delta}, E = {expected_latency(rules_delta):.2f}")

# Reset lại ACL để chạy ε-opt
rules_epsilon = [Rule(i, random.uniform(0.5, 1.0)) for i in range(1, 6)]
print("\nBan đầu (ε-opt):", rules_epsilon)

for step in range(1, 21):
    idx = random.randint(0, len(rules_epsilon)-1)
    epsilon_opt(rules_epsilon, idx)
    if step % 5 == 0:
        print(f"Sau {step} packet (ε-opt): {rules_epsilon}, E = {expected_latency(rules_epsilon):.2f}")
