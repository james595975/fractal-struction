from flask import Flask, request, send_file, jsonify
import matplotlib.pyplot as plt
import numpy as np
import random
import io
import os
import logging

app = Flask(__name__)
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")

logging.basicConfig(level=logging.DEBUG)

def chaos_game(points, total_points):
    x, y = 0.0, 0.0
    result = []

    for _ in range(total_points):
        target = random.choice(points)
        x = (x + target[0]) / 2
        y = (y + target[1]) / 2
        result.append([x, y])

    fractal_points = np.array(result)
    app.logger.debug(f"Generated fractal points: {fractal_points[:10]}")  # 처음 10개 점 디버깅
    return fractal_points

def deterministic_method(transforms, iterations):
    result = [(0.0, 0.0)]
    for _ in range(iterations):
        new_points = []
        for x, y in result:
            for t in transforms:
                x_new = t[0] * x + t[1] * y + t[4]
                y_new = t[2] * x + t[3] * y + t[5]
                new_points.append((x_new, y_new))
        result = new_points
    return np.array(result)

def load_transform_file(filename):
    filepath = os.path.join(STATIC_DIR, filename)
    transforms = []
    with open(filepath, 'r') as f:
        for line in f:
            parts = line.strip().split(',')
            if len(parts) == 6:
                transforms.append([float(p) for p in parts])
    return transforms

@app.route('/generate', methods=['POST'])
def generate_fractal():
    try:
        data = request.get_json()
        app.logger.debug(f"Received data: {data}")

        mode = data.get("mode")
        total_points = int(data.get("total_points"))

        if mode == "chaos":
            points = np.array(data.get("points"))
            app.logger.debug(f"Chaos points: {points}")
            if points.size == 0:
                return jsonify({"error": "No points provided for chaos game"}), 400
            fractal_points = chaos_game(points, total_points)

        elif mode == "deterministic":
            filename = data.get("transform_file")
            app.logger.debug(f"Deterministic file: {filename}")
            if not filename:
                return jsonify({"error": "transform_file is required"}), 400
            transforms = load_transform_file(filename)
            iterations = int(data.get("iterations", 10))
            fractal_points = deterministic_method(transforms, iterations)

        else:
            return jsonify({"error": "Invalid mode"}), 400

        # 이미지 생성
        plt.figure(figsize=(6, 6))
        plt.scatter(fractal_points[:, 0], fractal_points[:, 1], s=0.2, color='black')
        plt.axis('equal')
        plt.axis('off')

        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=300, bbox_inches='tight')
        plt.close()
        buf.seek(0)
        app.logger.debug(f"Generated image size: {buf.getbuffer().nbytes} bytes")
        return send_file(buf, mimetype='image/png')

    except Exception as e:
        app.logger.error(f"Exception: {e}")
        return jsonify({"error": str(e)}), 500
if __name__ == '__main__':
    app.run(port=5000)
