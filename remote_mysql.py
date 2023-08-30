import pymysql


def use_mysql(sql):
    try:
        host = '8.105.53.134'
        port = 3306
        user = 'root'
        password = '**********'
        db = 'Face_recognition'


        conn = pymysql.connect(host=host, port=port, user=user, password=password, db=db)
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute(sql)
        p = cursor.fetchone()
        conn.commit()
        cursor.close()
        conn.close()
        return p
    except:
        print("mysql_error")
        pass