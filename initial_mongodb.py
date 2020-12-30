#!/usr/bin/python3
import pymongo

def initialmongodb():
    myclient = pymongo.MongoClient('mongodb://oriyao:cnp200@152.32.132.155:27017/')
    dblist = myclient.list_database_names()
    print(dblist)
    mymongodb = input("Input your new database name:")
    if mymongodb in dblist:
        print("DB already exist!")
        print("Delete DB:" + mymongodb)
        myclient.drop_database(mymongodb)
    else:
        print("Create new dbase!")
    
    my_mongo_db = myclient[mymongodb]
    coll = my_mongo_db["oriyao_users"]
    default_admin = {"name": 'z00290969', "email": 'oriyao@sina.com',"password":'cnp200@HW'}
    coll.insert_one(default_admin)
    dblist = myclient.list_database_names()
    users = coll.find_one({"name":'z00290969'})
    print(users)
    return users
if __name__ == '__main__':
    print('Hello MongoDB!')
    # 获取自动生成的ID
    print(initialmongodb()['_id'])
