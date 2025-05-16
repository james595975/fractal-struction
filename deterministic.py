import matplotlib.pyplot as plt
from tkinter import Tk, filedialog

# 파일 탐색기 열기
def select_file():
    root = Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    filepath = filedialog.askopenfilename(title="변환 함수 파일 선택", filetypes=[("Text Files", "*.txt")])
    root.destroy()
    return filepath

print("초기 메시지 출력 등 다른 코드 실행 중...")

input("준비되면 엔터 누르세요. 그 후 파일 탐색기 열림.")

file = select_file()

if file:
    print("선택한 파일:", file)
else:
    print("파일 선택 취소")
# Affine 변환 함수
def apply_affine(x, y, a, b, c, d, e, f):
    x_new = a * x + b * y + e
    y_new = c * x + d * y + f
    return x_new, y_new

# 변환 파일 로드
def load_transform_file(filepath):
    transforms = []
    for line in open(filepath, "r"):
        if line.strip() and not line.strip().startswith("#"):
            values = list(map(float, line.strip().split()))
            if len(values) == 6:
                transforms.append(values)
    return transforms

# ===================
# 프로그램 시작
# ===================
print("=== 결정론적 IFS 프랙탈 생성기 ===")

# 초기점 x y 한 줄 입력
x0, y0 = map(float, input("초기점 (x y): ").strip().split(','))

# 반복 횟수
iterations = int(input("반복 횟수 (예: 5 ~ 10): "))

# 파일 선택
print("변환 함수 파일을 선택하세요...")
filepath = select_file()
if not filepath:
    print("❌ 파일을 선택하지 않았습니다. 종료합니다.")
    exit()

# 파일 불러오기
transforms = load_transform_file(filepath)
if not transforms:
    print("❌ 유효한 변환 함수가 없습니다. 종료합니다.")
    exit()

# 결정론 방식 실행
points = [(x0, y0)]
for _ in range(iterations):
    new_points = []
    for x, y in points:
        for t in transforms:
            new_points.append(apply_affine(x, y, *t))
    points = new_points

# 저장 및 시각화
x_vals, y_vals = zip(*points)
plt.figure(figsize=(6, 6), dpi=800)
plt.scatter(x_vals, y_vals, s=0.2, color='black')
plt.axis("equal")
plt.axis("off")
plt.tight_layout()
plt.savefig("fractal-deterministic.png", dpi=800, bbox_inches='tight')
plt.show()

print("\n✅ 'fractal-deterministic.png'에 저장 완료.")
