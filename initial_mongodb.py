#!/usr/bin/python3
import pymongo

def initialmongodb():
    myclient = pymongo.MongoClient('mongodb://XXX/')
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
    default_admin = {"name": 'xxx', "email": 'oriyao@sina.com',"password":'xxx'}
    coll.insert_one(default_admin)
    dblist = myclient.list_database_names()
    users = coll.find_one({"name":'xxx'})
    print(users)
    return users
if __name__ == '__main__':
    print('Hello MongoDB!')
    # 获取自动生成的ID
    print(initialmongodb()['_id'])
