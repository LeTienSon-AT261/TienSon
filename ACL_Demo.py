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
# Kiểm tra xem 2 rule có thể hoán đổi không dựa vào ma trận phụ thuộc D
# ----------------------
def can_swap(i, j, D):
    # Chỉ được swap nếu 2 rule không phụ thuộc nhau
    return D[i][j] == 0 and D[j][i] == 0

# ----------------------
# Thuật toán δ-opt (delta-opt) có kiểm tra ma trận phụ thuộc
# ----------------------
def delta_opt(rules, matched_index, D, theta=2):
    # B1. tăng hit-rate của rule match
    rules[matched_index].hit_rate *= theta

    # B2. kiểm tra trade-off + ràng buộc phụ thuộc, nếu có lợi thì swap
    if matched_index > 0 and can_swap(matched_index, matched_index - 1, D):
        r_i = rules[matched_index]
        r_prev = rules[matched_index - 1]
        if r_i.hit_rate * r_prev.latency > r_prev.hit_rate * r_i.latency:
            rules[matched_index-1], rules[matched_index] = rules[matched_index], rules[matched_index-1]

# ----------------------
# Thuật toán ε-opt (epsilon-opt) có kiểm tra ma trận phụ thuộc
# ----------------------
def epsilon_opt(rules, matched_index, D):
    if matched_index > 0 and can_swap(matched_index, matched_index - 1, D):
        rules[matched_index-1], rules[matched_index] = rules[matched_index], rules[matched_index-1]

# ----------------------
# DEMO: tạo ACL, ma trận phụ thuộc, và sinh traffic
# ----------------------
random.seed(0)

# ACL gồm 5 rule với latency ngẫu nhiên
rules_delta = [Rule(i, random.uniform(0.5, 1.0)) for i in range(1, 6)]

# Tạo ma trận phụ thuộc 5x5 (ban đầu giả định độc lập)
D = [[0 for _ in range(5)] for _ in range(5)]

# Giả lập một số phụ thuộc (ví dụ R1 che phủ R2)
D[0][1] = 1  # R1 phụ thuộc vào R2 ⇒ không được đổi chỗ với nhau
# bạn có thể chỉnh D tùy theo ACL thực tế

print("Ban đầu (δ-opt):", rules_delta)

# Sinh 20 packet, mỗi packet match 1 rule ngẫu nhiên
for step in range(1, 21):
    idx = random.randint(0, len(rules_delta)-1)
    delta_opt(rules_delta, idx, D)
    if step % 5 == 0:
        print(f"Sau {step} packet (δ-opt): {rules_delta}, E = {expected_latency(rules_delta):.2f}")

# Reset lại ACL để chạy ε-opt
rules_epsilon = [Rule(i, random.uniform(0.5, 1.0)) for i in range(1, 6)]
print("\nBan đầu (ε-opt):", rules_epsilon)

for step in range(1, 21):
    idx = random.randint(0, len(rules_epsilon)-1)
    epsilon_opt(rules_epsilon, idx, D)
    if step % 5 == 0:
        print(f"Sau {step} packet (ε-opt): {rules_epsilon}, E = {expected_latency(rules_epsilon):.2f}")
