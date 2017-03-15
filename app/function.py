#-*- coding: utf-8 -*-
import sqlite3

#member.db 만드는 함수
#Email, PW, PN, CC, AP
# PN: 펫 수 (1, 0) , 0으로 초기화
# CC: 집등록할경우 해당 집의 city code, 0으로 초기화
# AP: 펫시팅 가능 여부 (1, 0) , 0으로 초기화
def Make_db():
    con = sqlite3.connect("member.db")
    cursor = con.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS member(Email text NOT NULL UNIQUE, PW text NOT NULL,PN text DEFAULT 0, CC text DEFAULT 0, AP text DEFAULT 0)")
    con.commit()
    con.close()

#pet.db 만드는 함수
#Host, P_key, Name, Birth, Gender, Kind, NS, Vac
#HosT: member.db 의 Email
#P_key: 이메일#Pet
def Make_db_pet():
    con = sqlite3.connect("pet.db")
    cursor = con.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS pet(Host text NOT NULL,P_key text, Name text, Birth text, Gender text, Kind text,NS text, Vac text, PRIMARY KEY(Host), CONSTRAINT fk_PerPet FOREIGN KEY (Host) REFERENCES member(Email))")
    con.commit()
    con.close()

#house.db 만드는 함수
#Host, H_key, State, City, Street, Apt, Address,citycode, Type, Room, Area, Elevator, Parking
#Host, H_key, Address, Type, Room, Area, Elevator, Parking
#Type :  집타입 아파트 : A, 빌라 : V, 개인주택 : P, 다세대 주택 : M
#Host -> member.db 의 Email
def Make_db_house():
    con = sqlite3.connect("house.db")
    cursor = con.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS house(Host text NOT NULL, H_key text NOT NULL, State text NOT NULL, City text NOT NULL, Street text NOT NULL, Apt text NOT NULL, Address text NOT NULL, Citycode text DEFAULT 0 ,Type text DEFAULT 0, Room text DEFAULT 0, Area text DEFAULT 0, Elevator text, Parking text, PRIMARY KEY(Host), CONSTRAINT fk_PerPet FOREIGN KEY (Host) REFERENCES member(Email))")
    con.commit()
    con.close()

#C_key, PSID, CSID, TS, TE, TC, TA, TH
# def Make_db_transaction():
#     con = sqlite3.connect("transaction.db")
#     cursor = con.cursor()
#     cursor.execute("CREATE TABLE house(C_key text NOT NULL, PSID text NOT NULL, CSID text NOT NULL, TS text NOT NULL, TE text NOT NULL, TC text NOT NULL, TA text NOT NULL, TH text NOT NULL, PRIMARY KEY(PSID), CONSTRAINT fk_PerPet FOREIGN KEY (PSID) REFERENCES member(Email), CONSTRAINT fk_PerPet FOREIGN KEY (CSID) REFERENCES member(Email))")
#     con.commit()
#     con.close()

def Check_email(E):
    con = sqlite3.connect("member.db")
    cursor = con.cursor()
    cursor.execute("SELECT Email FROM member WHERE Email=? ",(E, ))
    data = cursor.fetchall()
    con.commit()
    con.close()
    return data

def Check_pw(E, P):
    con = sqlite3.connect("member.db")
    cursor = con.cursor()
    cursor.execute("SELECT Email FROM member WHERE Email=? AND PW = ?",(E, P))
    data = cursor.fetchall()
    con.commit()
    con.close()
    return data

def Check_citycode(E):
    con = sqlite3.connect("member.db")
    cursor = con.cursor()
    cursor.execute("SELECT CC FROM member WHERE Email=?",(E, ))
    data = cursor.fetchall()
    con.commit()
    con.close()
    return data

#Email : E, Password: P로 회원가입 할 경우 디비에 이를 저장
def Save_mem(E, P):
    con = sqlite3.connect("member.db")
    cursor = con.cursor()
    try:
        cursor.execute("INSERT INTO member (Email, PW) VALUES (?,?)", (E,P))
    except:
        return 0 # 이미 있는 이메일인 경우 -중복가입 방지
    con.commit()
    con.close()
    return 1

#db에서 Citycode 수정하는 함수
def Update_Citycode(E, city):
    con = sqlite3.connect("member.db")
    cursor = con.cursor()
    cursor.execute("UPDATE member SET CC = ? WHERE Email = ? ", (city,E))
    con.commit()
    con.close()

#pet 등록할 경우 db에서 해당 고객 N_pet 증가시켜주는 함수
def Increase_npet(E):
    con = sqlite3.connect("member.db")
    cursor = con.cursor()
    cursor.execute("UPDATE  member SET PN = 1 WHERE Email = ? ", (E,))
    con.commit()
    con.close()

#house 등록할 경우 db에 집 정보 저장하는 함수
#Host, H_key, State, City, Street, Apt, Address, Zipcode
def Save_home_address(E, H_State, H_City, H_Street, H_Apt,H_Zipcode):
    con = sqlite3.connect("house.db")
    cursor = con.cursor()
    key = E + "#Home"
    H_Address = H_State + " "+ H_City + " " + H_Street + " " + H_Apt
    cursor.execute("INSERT INTO house(Host, H_key, State, City, Street, Apt, Address,  Citycode) VALUES (?, ?, ?, ?, ?,?,?,?)", (E,key, H_State, H_City, H_Street, H_Apt, H_Address, H_Zipcode))
    con.commit()
    con.close()

#house 등록할 경우 db에 집 정보 저장하는 함수
#Type, Room
def Save_home_room(E, H_Type, H_Room):
    con = sqlite3.connect("house.db")
    cursor = con.cursor()
    cursor.execute("UPDATE house set Type = ?, Room = ? WHERE Host = ?", (H_Type, H_Room, E))

#house 등록할 경우 db에 집 정보 저장하는 함수
#Elevator, Parking
def Save_home_car_elevator(E, H_Elevator, H_Parking):
    con = sqlite3.connect("house.db")
    cursor = con.cursor()
    cursor.execute("UPDATE house set Elevator = ?, Parking= ? WHERE Host = ?", (H_Elevator, H_Parking, E))

#pet 등록할 경우 db에 펫 정보 저장하는 함수
#Host, P_key, Name, Birth, Gender, Kind, NS, Vac
#P_size : S= 소형견, M= 중형견, L=대형경
#NS, Vac : Y, N
def Save_pet(E, P_Name, P_Birth, P_Gender, P_Kind, P_NS, P_Vac):
    con = sqlite3.connect("pet.db")
    cursor = con.cursor()
    key = E + "#Pet"
    cursor.execute("INSERT INTO pet (Host, P_key, Name, Birth, Gender, Kind, NS, Vac) VALUES (?,?,?,?,?,?,?,?)", (E, key, P_Name, P_Birth, P_Gender, P_Kind, P_NS, P_Vac))
    con.commit()
    con.close()


#Host, H_key, Address, Type, Room, Area, Elevator, Parking
def Save_House(E,H_Address, H_Type, H_Room, H_Area, H_Elevator, H_Parking):
    con = sqlite3.connect("house.db")
    cursor = con.cursor()
    key = E + "#Home"
    cursor.execute("INSERT INTO house(Host, H_key, Address, Type, Room, Area, Elevator, Parking) VALUES (?,?,?,?,?,?,?,?)", (E,key,H_Address, H_Type, H_Room, H_Area, H_Elevator, H_Parking))
    con.commit()
    con.close()

#petsitter로 등록할 경우 해당고객의 F_Petsitter를 1로 업데이트
def Update_F_pesitter(E):
    con = sqlite3.connect("member.db")
    cursor = con.cursor()
    cursor.execute("UPDATE  member SET F_petsitter = 1 WHERE Email = ? ", (E,))
    con.commit()
    con.close()

#member.db 전체 읽는 함수 - 테스트용
def Read_member():
    con = sqlite3.connect("member.db")
    cursor = con.cursor()
    cursor.execute("SELECT * FROM member")
    data = cursor.fetchall()
    con.commit()
    con.close()
    return data

#pet.db 전체 읽는 함수 - 테스트용
def Read_pet():
    con = sqlite3.connect("pet.db")
    cursor = con.cursor()
    cursor.execute("SELECT * FROM pet")
    data = cursor.fetchall()
    con.commit()
    con.close()
    return data

#pet.db 전체 읽는 함수 - 테스트용
def Read_house():
    con = sqlite3.connect("house.db")
    cursor = con.cursor()
    cursor.execute("SELECT * FROM house")
    data = cursor.fetchall()
    con.commit()
    con.close()
    return data

#db 전체 지우는 함수 - 테스트용
def Delete_member():
    con = sqlite3.connect("member.db")
    cursor = con.cursor()
    cursor.execute("DROP TABLE member")
    con.commit()
    con.close()

#db 전체 지우는 함수 - 테스트용
def Delete_pet():
    con = sqlite3.connect("pet.db")
    cursor = con.cursor()
    cursor.execute("DROP TABLE pet")
    con.commit()
    con.close()

#db 전체 지우는 함수 - 테스트용
def Delete_house():
    con = sqlite3.connect("house.db")
    cursor = con.cursor()
    cursor.execute("DROP TABLE house")
    con.commit()
    con.close()
