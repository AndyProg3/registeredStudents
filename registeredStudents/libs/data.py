import mysql.connector

mydb = mysql.connector.connect(host="euler.wiregrass.edu", user="LoginQueryUsr", password="welcome1n")

def getTerms():
    cursor = mydb.cursor()

    _query = " select distinct semester from appusers.registered_students group by semester order by semester desc "

    cursor.execute(_query)
    results = cursor.fetchall()

    resultDict = []

    for x in results:
        resultDict.append({"semester":x[0], })

    return resultDict

def getMajors():
    cursor = mydb.cursor()

    _query = " select * from appusers.degree_codes order by degree_code "

    cursor.execute(_query)
    results = cursor.fetchall()

    resultDict = []

    for x in results:
        resultDict.append({"code":x[0], "desc":x[1], })

    return resultDict

def getData(Term, Majors):
    cursor = mydb.cursor()
    format_strings = None

    _where = None

    if isinstance(Majors, (list, tuple, dict, set)):
        format_strings = ','.join(['%s'] * len(Majors))
        _where = " and dc.degree_code in (%s) " % format_strings
    else:
        _where = ""

    _query = " select rs.FName, rs.LName, rs.StudentID, rs.degree_code from appusers.registered_students rs join appusers.degree_codes dc on dc.degree_code = rs.degree_code where rs.semester = %s " + _where + " order by FName"
    _params = (Term, )

    if(_where != ""):
        _params = _params + tuple(Majors)

    cursor.execute(_query, _params)
    results = cursor.fetchall()

    resultDict = []

    for x in results:
        resultDict.append({"FName":x[0], "LName":x[1], "StudentID":x[2], "degree_code":x[3], })
        
    return resultDict