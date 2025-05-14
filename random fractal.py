import matplotlib.pyplot as plt
import numpy as np
import random

def get_initial_points():
    print("=== 초기 셀 점 입력 ===")
    num_points = int(input("점 개수 입력 (예: 3): "))
    points = []
    for i in range(num_points):
        while True:
            try:
                xy = input(f"점 {i+1} 입력 (x,y): ").strip().split(',')
                if len(xy) != 2:
                    raise ValueError
                x, y = map(float, xy)
                points.append([x, y])
                break
            except ValueError:
                print("잘못된 형식입니다. 예: 0.5,0.866")
    return np.array(points)

def generate_random_fractal(initial_points, total_points=50000):
    x, y = 0.0, 0.0
    result = []

    for _ in range(total_points):
        target = random.choice(initial_points)
        x = (x + target[0]) / 2
        y = (y + target[1]) / 2
        result.append([x, y])

    return np.array(result)

def main():
    initial_points = get_initial_points()
    total_points = int(input("생성할 점 개수 (예: 50000): "))
    filename = "fractal.png"

    fractal_points = generate_random_fractal(initial_points, total_points)

    # 시각화 및 저장
    plt.figure(figsize=(6, 6))
    plt.scatter(fractal_points[:, 0], fractal_points[:, 1], s=0.2, color='purple')
    plt.axis('equal')
    plt.axis('off')
    plt.title("Random Fractal from Initial Cell")
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()

    print(f">>> 이미지 저장 완료: {filename}")

if __name__ == "__main__":
    main()