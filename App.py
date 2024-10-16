from flask import Flask, render_template, jsonify, request, redirect
import cx_Oracle
from datetime import datetime

app = Flask(__name__)
with open(app.root_path + '\config.cfg', 'r') as f:
    app.config['ORACLE_URI'] = f.readline()

con = cx_Oracle.connect("sys", "tiger", "localhost/orclpdb",mode = cx_Oracle.SYSDBA)




@app.route('/')
@app.route('/teams')
def teams():
    teams = []

    cur = con.cursor()
    cur.execute('select * from teams')
    for result in cur:
        team = {}
        team['team_id'] = result[0]
        team['Team_name'] = result[1]
        team['ABB'] = result[2]
        team['team_city'] = result[3]
        team['stadium_id'] = result[4]
        team['manager_id'] = result[5]

        teams.append(team)
    cur.close()

    com = []
    cur = con.cursor()
    cur.execute('select name from stadium')
    # import pdb;pdb.set_trace()
    for result in cur:
        com.append(result[0])
    cur.close()

    com2 = []
    cur = con.cursor()
    cur.execute('select lname from manager')
    # import pdb;pdb.set_trace()
    for result in cur:
        com2.append(result[0])
    cur.close()

    return render_template('teams.html', teams=teams,team=com,team2=com2)


@app.route('/addteams', methods=['GET', 'POST'])
def ad_team():
    error = None
    if request.method == 'POST':
        team = []
        c = "'" + request.form['name'] + "'"

        cur = con.cursor()
        cur.execute('select stadium_id from stadium where name=' + c)
        for result in cur:
            team = result[0]
        cur.close()

        team2 = []
        d = "'" + request.form['lname'] + "'"

        cur = con.cursor()
        cur.execute('select manager_id from manager where lname=' + d)
        for result in cur:
            team2 = result[0]
        cur.close()


        cur = con.cursor()
        values = []
        values.append("'" + request.form['team_id'] + "'")
        values.append("'" + request.form['Team_name'] + "'")
        values.append("'" + request.form['ABB'] + "'")
        values.append("'" + request.form['team_city'] + "'")
        values.append("'" + str(team) + "'")
        values.append("'" + str(team2) + "'")

        fields = ['team_id', 'Team_name', 'ABB', 'team_city', 'stadium_id', 'manager_id']
        query = 'INSERT INTO %s (%s) VALUES (%s)' % (
            'teams',
            ', '.join(fields),
            ', '.join(values)
        )

        cur.execute(query)
        cur.execute('commit')
        return redirect('/teams')


@app.route('/delTeams', methods=['POST'])
def del_team():
    team = request.form['team_id']
    cur = con.cursor()
    cur.execute('delete from teams where team_id=' + team)
    cur.execute('commit')
    return redirect('/teams')


@app.route('/contracts')
def regions():
    counselors = []

    cur = con.cursor()
    cur.execute('select * from contracts')
    for result in cur:
        counselor = {}
        counselor['contract_id'] = result[0]
        counselor['salary_season'] = result[1]
        counselors.append(counselor)
    cur.close()
    return render_template('contracts.html', counselors=counselors)


@app.route('/addContracts', methods=['GET', 'POST'])
def ad_contract():
    error = None
    if request.method == 'POST':

        cur = con.cursor()
        values = []
        values.append("'" + request.form['contract_id'] + "'")
        values.append("'" + request.form['salary_season'] + "'")

        fields = ['contract_id', 'salary_season']
        query = 'INSERT INTO %s (%s) VALUES (%s)' % (
            'contracts',
            ', '.join(fields),
            ', '.join(values)
        )

        cur.execute(query)
        cur.execute('commit')
        return redirect('/contracts')


@app.route('/delContracts', methods=['POST'])
def del_contract():
    contract = request.form['contract_id']
    cur = con.cursor()
    cur.execute('delete from contracts where contract_id=' + contract)
    cur.execute('commit')
    return redirect('/contracts')


@app.route('/stadium')
def std():
    counselors = []

    cur = con.cursor()
    cur.execute('select * from stadium')
    for result in cur:
        counselor = {}
        counselor['stadium_id'] = result[0]
        counselor['name'] = result[1]
        counselor['nr_seats'] = result[2]


        counselors.append(counselor)
    cur.close()

    return render_template('stadium.html', counselors=counselors)


@app.route('/ADDstadium', methods=['POST'])
def ad_loc():
    error = None
    if request.method == 'POST':


        cur = con.cursor()
        values = []
        values.append("'" + request.form['stadium_id'] + "'")
        values.append("'" + request.form['name'] + "'")
        values.append("'" + request.form['nr_seats'] + "'")
        fields = ['stadium_id', 'name', 'nr_seats']
        query = 'INSERT INTO %s (%s) VALUES (%s)' % (
            'stadium',
            ', '.join(fields),
            ', '.join(values)
        )

        cur.execute(query)
        cur.execute('commit')
        return redirect('/stadium')


@app.route('/delStadium', methods=['POST'])
def del_stadium():
    cnp = request.form['stadium_id']
    cur = con.cursor()
    cur.execute('delete from stadium where stadium_id=' + cnp)
    cur.execute('commit')
    return redirect('/stadium')



@app.route('/manager')
def mng():
    counselors = []

    cur = con.cursor()
    cur.execute('select * from manager')
    for result in cur:
        counselor = {}
        counselor['manager_id'] = result[0]
        counselor['fname'] = result[1]
        counselor['lname'] = result[2]
        counselor['age'] = result[3]
        counselor['contract_id'] = result[4]




        counselors.append(counselor)
    cur.close()
    com = []
    cur = con.cursor()
    cur.execute('select contract_id from contracts')
    # import pdb;pdb.set_trace()
    for result in cur:
        com.append(result[0])
    cur.close()



    return render_template('manager.html', counselors=counselors, manager=com)


@app.route('/ADDmanager', methods=['POST'])
def ad_mng():
    error = None
    if request.method == 'POST':


        cur = con.cursor()
        values = []
        values.append("'" + request.form['manager_id'] + "'")
        values.append("'" + request.form['fname'] + "'")
        values.append("'" + request.form['lname'] + "'")
        values.append("'" + request.form['age'] + "'")
        values.append("'" + request.form['contract_id'] + "'")

        fields = ['manager_id', 'fname', 'lname', 'age','contract_id']
        query = 'INSERT INTO %s (%s) VALUES (%s)' % (
            'manager',
            ', '.join(fields),
            ', '.join(values)
        )

        cur.execute(query)
        cur.execute('commit')
        return redirect('/manager')


@app.route('/delManager', methods=['POST'])
def del_manager():
    cnp = request.form['manager_id']
    cur = con.cursor()
    cur.execute('delete from manager where manager_id=' + cnp)
    cur.execute('commit')
    return redirect('/manager')






@app.route('/players')
def ply():
    counselors = []

    cur = con.cursor()
    cur.execute('select * from players')
    for result in cur:
        counselor = {}
        counselor['player_id'] = result[0]
        counselor['first_name'] = result[1]
        counselor['last_name'] = result[2]
        counselor['age'] = result[3]
        counselor['pozitie'] = result[4]
        counselor['weight_kg'] = result[5]
        counselor['height_cm'] = result[6]
        counselor['nationality'] = result[7]
        counselor['team_id'] = result[8]
        counselor['contract_id'] = result[9]
        counselor['kit_number'] = result[10]
        counselors.append(counselor)
    cur.close()
    com = []
    cur = con.cursor()
    cur.execute('select contract_id from contracts')
    # import pdb;pdb.set_trace()
    for result in cur:
        com.append(result[0])
    cur.close()

    com2=[]
    cur = con.cursor()
    cur.execute('select Team_name from teams')
    # import pdb;pdb.set_trace()
    for result in cur:
        com2.append(result[0])
    cur.close()

    return render_template('players.html', counselors=counselors, player=com,player2=com2)


@app.route('/ADDplayer', methods=['POST'])
def ad_ply():
    error = None
    if request.method == 'POST':
        team = []
        c = "'" + request.form['Team_name'] + "'"

        cur = con.cursor()
        cur.execute('select team_id from teams where Team_name=' + c)
        for result in cur:
            team = result[0]
        cur.close()

        cur = con.cursor()
        values = []
        values.append("'" + request.form['player_id'] + "'")
        values.append("'" + request.form['first_name'] + "'")
        values.append("'" + request.form['last_name'] + "'")
        values.append("'" + request.form['age'] + "'")
        values.append("'" + request.form['pozitie'] + "'")
        values.append("'" + request.form['weight_kg'] + "'")
        values.append("'" + request.form['height_cm'] + "'")
        values.append("'" + request.form['nationality'] + "'")
        values.append("'" + str(team) + "'")
        values.append("'" + request.form['contract_id'] + "'")
        values.append("'" + request.form['kit_number'] + "'")
        fields = ['player_id', 'first_name', 'last_name', 'age','pozitie','weight_kg','height_cm','nationality','team_id','contract_id','kit_number']
        query = 'INSERT INTO %s (%s) VALUES (%s)' % (
            'players',
            ', '.join(fields),
            ', '.join(values)
        )

        cur.execute(query)
        cur.execute('commit')
        return redirect('/players')


@app.route('/delPlayer', methods=['POST'])
def del_ply():
    cnp = request.form['player_id']
    cur = con.cursor()
    cur.execute('delete from players where player_id=' + cnp)
    cur.execute('commit')
    return redirect('/players')




if __name__ == '__main__':
	app.run(debug=True)
	con.close()