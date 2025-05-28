from flask import Flask, request, jsonify
import subprocess
import uuid
import os
import json

app = Flask(__name__)

@app.route('/execute', methods=['POST'])
def execute():
    data = request.get_json()

    if not data or 'script' not in data:
        return jsonify({"error": "Missing 'script' in request"}), 400

    script = data['script']

    # Write script to a temporary file
    script_id = str(uuid.uuid4())
    script_path = f"/tmp/{script_id}.py"
    with open(script_path, 'w') as f:
        f.write(script)

    try:
        result = subprocess.run(
            [
                "nsjail",
                "-Mo",
                "--rlimit_as", "256",
                "--time_limit", "5",
                "--cwd", "/tmp",
                "--bindmount", "/tmp",
                "--bindmount", "/usr",
                "--bindmount", "/lib",
                "--bindmount", "/lib64",
                "--bindmount", "/usr/local",
                "--",
                "/usr/local/bin/python", script_path
            ],
            capture_output=True, text=True, timeout=5
        )

        if result.returncode != 0:
            return jsonify({"error": result.stderr.strip()}), 400

        lines = result.stdout.strip().split('\n')

        try:
            output_json = json.loads(lines[-1]) if lines else {}
        except json.JSONDecodeError:
            return jsonify({"error": "Script did not return valid JSON"}), 500

        return jsonify({
            "result": output_json,
            "stdout": '\n'.join(lines[:-1])
        })

    except subprocess.TimeoutExpired:
        return jsonify({"error": "Execution timed out"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if os.path.exists(script_path):
            os.remove(script_path)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
