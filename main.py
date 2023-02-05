from flask import Flask, request, jsonify
import pymysql

app = Flask(__name__)
conn = pymysql.connect(host='localhost', user='root', password='root', database='Shortlist')

class College:
    def __init__(self, id, name, points,tier):
        self.id = id
        self.name = name
        self.points = points
        self.tier = tier

def get_college(conn, name):
    cursor = conn.cursor()
    sql = f"SELECT * FROM shortlist.bachelor_school WHERE bachelor_school.name='{name}'"
    cursor.execute(sql)
    college = cursor.fetchone()
    if college:
        return College(*college)
    return None

def get_mba(conn, name):
    cursor = conn.cursor()
    sql = f"SELECT * FROM shortlist.mba_school WHERE mba_school.name='{name}'"
    cursor.execute(sql)
    mba= cursor.fetchone()
    if mba:
        return College(*mba)
    return None

@app.route("/test-db")
def test_db_connection():
    cursor = conn.cursor()
    sql = "SELECT * FROM shortlist.bachelor_school"
    cursor.execute(sql)
    result = cursor.fetchall()
    return jsonify({"result": result})

@app.route("/", methods=["POST", "GET"])
def calculate_score():
    if request.method == "POST":
        bachelor_school = request.form.get("bachelor_school")
        mba_school = request.form.get("mba_school")

        bachelor_school_data = get_college(conn, bachelor_school)
        mba_school_data = get_mba(conn, mba_school)

        if not bachelor_school_data or not mba_school_data:
            return jsonify({"error": "College not found"}), 404

        score1 = 0
        score2 = 0
        print(bachelor_school_data.tier)
        print(mba_school_data.tier)
        if bachelor_school_data.tier == 'Tier1':
            score1 += 10
        elif bachelor_school_data.tier == 'Tier2':
            score1 += 5
        elif bachelor_school_data.tier == 'Tier3':
            score1 += 2

        if mba_school_data.tier == 'Tier1':
            score2 += 10
        else:
            score2 += 5

        print(score1)
        print(score2)

        final=score1+score2

        return jsonify({"score": final})

    return '''
        <form method="post">
            Bachelor School: <input type="text" name="bachelor_school"><br>
            MBA School: <input type="text" name="mba_school"><br>
            <input type="submit" value="Submit">
        </form>
    '''

if __name__ == "__main__":
    app.run(debug=True)
