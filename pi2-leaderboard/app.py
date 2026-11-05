import sqlite3
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)
DB_FILE = "scores.db"


def init_db():
  """Initializes the SQLite database table for high scores."""
  conn = sqlite3.connect(DB_FILE)
  cursor = conn.cursor()
  cursor.execute("""
        CREATE TABLE IF NOT EXISTS scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            game TEXT NOT NULL,
            name TEXT NOT NULL,
            score INTEGER NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
  conn.commit()
  conn.close()


@app.route("/")
def index():
  """Renders the live web leaderboard page (R5)."""
  conn = sqlite3.connect(DB_FILE)
  cursor = conn.cursor()
  games = ["Dinosaur", "FlappyBird", "Tetris"]
  leaderboards = {}

  for game in games:
    cursor.execute(
        "SELECT name, score FROM scores WHERE game = ? ORDER BY score DESC"
        " LIMIT 10",
        (game,),
    )
    leaderboards[game] = cursor.fetchall()

  conn.close()
  return render_template("index.html", leaderboards=leaderboards)


@app.route("/score", methods=["POST"])
def post_score():
  """Receives and saves a new score from a game client (R3)."""
  data = request.get_json()
  if not data or not all(k in data for k in ("game", "name", "score")):
    return jsonify({"error": "Invalid payload format"}), 400

  try:
    game = str(data["game"])
    name = str(data["name"])[:20]  # Cap name length
    score = int(data["score"])
  except (ValueError, TypeError):
    return jsonify({"error": "Data type mismatch"}), 400

  conn = sqlite3.connect(DB_FILE)
  cursor = conn.cursor()
  cursor.execute(
      "INSERT INTO scores (game, name, score) VALUES (?, ?, ?)",
      (game, name, score),
  )
  conn.commit()
  conn.close()

  return jsonify({"status": "success", "message": "Score recorded"}), 201


@app.route("/top/<game>", methods=["GET"])
def get_top(game):
  """Returns top 10 scores for a specific game as JSON (R3)."""
  conn = sqlite3.connect(DB_FILE)
  cursor = conn.cursor()
  cursor.execute(
      "SELECT name, score FROM scores WHERE game = ? ORDER BY score DESC LIMIT"
      " 10",
      (game,),
  )
  rows = cursor.fetchall()
  conn.close()

  results = [{"name": r[0], "score": r[1]} for r in rows]
  return jsonify(results)


if __name__ == "__main__":
  init_db()
  # Bind to 0.0.0.0 to accept network connections from Pi #1
  app.run(host="0.0.0.0", port=5000, debug=False)