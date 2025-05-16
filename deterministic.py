import matplotlib
matplotlib.use('Agg')

from flask import Flask, request, send_file, jsonify
import matplotlib.pyplot as plt
import numpy as np
import os
import io

app = Flask(__name__)

def apply_affine(x, y, a, b, c, d, e, f):
    x_new = a * x + b * y + e
    y_new = c * x + d * y + f
    return x_new, y_new

def load_transforms(file_storage):
    transforms = []
    for line in file_storage.read().decode("utf-8").splitlines():
        if line.strip() and not line.strip().startswith("#"):
            values = list(map(float, line.strip().split()))
            if len(values) == 6:
                transforms.append(values)
    return transforms

@app.route('/generate', methods=['POST'])
def generate_fractal():
    try:
        x0 = float(request.form['x0'])
        y0 = float(request.form['y0'])
        iterations = int(request.form['iterations'])
        file = request.files['file']

        transforms = load_transforms(file)
        if not transforms:
            return jsonify({"error": "No valid transform data"}), 400

        points = [(x0, y0)]
        for _ in range(iterations):
            new_points = []
            for x, y in points:
                for t in transforms:
                    new_points.append(apply_affine(x, y, *t))
            points = new_points

        x_vals, y_vals = zip(*points)
        fig, ax = plt.subplots(figsize=(6, 6), dpi=300)
        ax.scatter(x_vals, y_vals, s=0.2, color='black')
        ax.axis('equal')
        ax.axis('off')
        plt.tight_layout()

        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=300, bbox_inches='tight')
        plt.close()
        buf.seek(0)
        return send_file(buf, mimetype='image/png')
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000)
