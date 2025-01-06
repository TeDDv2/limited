module.exports = {
    apps : [{
      name: "limited_rework",
      script: "main.py",
      interpreter: "venv/bin/python",
      watch: true,
      env: {
        "PYTHONUNBUFFERED": "1"
      }
    }]
  }