import psycopg2
from configparser import ConfigParser

def config(filename="database.ini",section='postgresql'):
    #Create a parser
    parser = ConfigParser()
    
    #Read the config file
    parser.read(filename)
    
    #Get section, default to postgresql
    db={}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]]=param[1]
    else:
        raise Exception('Section{0} not found in the {1} file'.format(section,filename))
    return db
def getConnection():
    #Obtain connection to the database
    connection = None
    try:
        #Read connection parameters
        params = config()
        
        #Connect to the server
        connection = psycopg2.connect(**params)
        return connection
    except(Exception,psycopg2.DatabaseError) as error:
        print(error)
        raise Exception("Failed to get connection to Postgres server")
     
mydb = getConnection()
mycursor=mydb.cursor()
def menu():
    #function to display menu
    print("MAIN MENU".center(140))
    print("1. Insert Products".center(140))
    print("2. Insert stock details".center(140))
    print("3. Insert Transaction details".center(140))
    print("4. Display Product records as per Product id".center(140))
    print("   a. Sorted as per product ID ".center(140))
    print("   b. Sorted as per Category ".center(140))
    print("5. Display Stock records as per stock id".center(140))
    print("   a. Sorted as per stock ID ".center(140))
    print("   b. Sorted as per Units ".center(140))
    print("6. Display Transaction Records as per item ID ".center(140))
    print("7. Search Product Records with Product ID ".center(140))
    print("8. Search Stock Records with Stock ID ".center(140))
    print("9.  Update Stock Records ".center(140))
    print("10. Delete Stock Records".center(140))
    print("11. Exit".center(140))
def menu_sort():
    print("   a. Sorted as per ID ".center(140))
    print("   b. Sorted as per Category ".center(140))
    print("   c. Back".center(140))
def menu_sort_stock():
    print("   a. Sorted as per stock ID ".center(140))
    print("   b. Sorted as per Category ".center(140))
    print("   c. Back".center(140))     
def create_p():
    try:
        mycursor.execute("Create table Product(Id varchar(10),Name varchar(20),Category varchar(20))")
        print("Table created")
        insert_p()
    except:
        mydb.rollback()
        print("Table exists")
        insert_p()
def insert_p():
    # Loop for accepting product records
    while True:
        id=input("Enter id Number:")
        name=input("Enter Name:")
        category=input("Enter Category of item:")
        rec=(id,name.upper(),category.upper())
        cmd="Insert into product values(%s,%s,%s)"
        mycursor.execute(cmd,rec)
        mydb.commit()
        ch=input("Do you want to enter more records(Y/N):")
        if ch=='n' or ch=='N':
            break
def create_stock():
    try:
        mycursor.execute("Create table stock (Id varchar(10),Units varchar(10),purchase_price decimal(20),Selling_price decimal(20))")
        print("Table created")
        stockid_check()
    except:
        mydb.rollback()
        print("Table exists")
        stockid_check()
def stockid_check():
    try:
        cmd="select * from product order by id"
        mycursor.execute(cmd)
        id = input("Enter Product Id:")
        found = False
        for i in mycursor:
            if i[0].strip()==id:
                insert_s()
                found = True
                break
        if(not(found)):
            print("Product with id: %s not found"%(id))
    except:
       print(" Product with this id doesn't exists")
def insert_s():
    while True:
        id = input("Re-enter Product id Number:")
        selling_price = input("Enter item selling_price:")
        purchase_price = input("Enter item purchase_price:")
        units = input("Enter number of units:")
        rec = (id, purchase_price, selling_price, units)
        cmd = "Insert into stock values(%s,%s,%s,%s)"
        mycursor.execute(cmd, rec)
        mydb.commit()
        ch = input("Do you want to enter more records(Y/N):")
        if ch == 'n' or ch == 'N':
            break
def create_transaction():
     try:
          mycursor.execute("Create table transaction (Date varchar(10),c_id varchar(10),Id varchar(10),sold_price decimal(20),Units_sold int)")
          print("Table created")
          id_check()
     except:
          mydb.rollback()
          print("Table exists")
          id_check()
def id_check():
    try:
        cmd="select * from stock order by id"
        mycursor.execute(cmd)
        id = input("Enter Product Id:")
        found = False
        for i in mycursor:
            if i[0].strip()==id:
                insert_t()
                found = True
                break
        if(not(found)):
            print("Record with id: %s not found"%(id))
    except:
       print("item with this id doesn't exists")
def insert_t():
    while True:
        date = input("Enter Date:")
        c_id = input("Enter customer Id:")
        id = input("Re-enter product Id:")
        sold_p = input("Enter sold price of units:")
        units_s = input("Enter units sold:")
        updated_stock(units_s,id)
        rec = (date, c_id, id, sold_p, units_s)
        cmd = "Insert into transaction values(%s, %s, %s, %s ,%s)"
        mycursor.execute(cmd, rec)
        
        mydb.commit()
        ch = input("Do you want to enter more records(Y/N):")
        if ch == 'n' or ch == 'N':
            break
def dispsortid():
    # function to sort & display product table as per id in asc
    try:
        cmd="select * from product order by id"
        mycursor.execute(cmd)
        f="%32s %32s %40s"
        print(f%("id", "name", "category"))
        print("="*125)
        for i in mycursor:
            for j in i:
                print("%40s" %j, end='')
            print()
        print("="*125)
    except:
         print("Table doesn't exist")
def dispsortcategory():
    # function to display product table as per asc order of category
    try:
        cmd="Select * from product order by category"
        mycursor.execute(cmd)
        f="%32s %32s %40s"
        print(f%("id", "name", "category"))
        print("=" * 125)
        for i in mycursor:
            for j in i:
                print("%40s" %j, end='')
            print()
        print("=" * 125)
    except:
        print("Table doesn't exists")
def dispsortid_stock():
    # function to sort & display stock table as per id in asc
    try:
        cmd="select * from stock order by id"
        mycursor.execute(cmd)
        f="%24s %38s %33s %22s"
        print(f%("id","purchase_price", "selling_price","units"))
        print("="*125)
        for i in mycursor:
            for j in i:
                print("%30s" %j, end='')
            print()
        print("="*125)
    except:
        print("Table doesn't exist")
def dispsortunits():
    # function to display stock table as per asc order of units
    try:
        cmd="Select * from stock order by units"
        mycursor.execute(cmd)
        f="%24s %38s %33s %22s"
        print(f%("id","purchase_price", "selling_price","units"))
        print("=" * 125)
        for i in mycursor:
            for j in i:
                print("%30s" %j, end='')
            print()
        print("=" * 125)
    except:
        print("Table doesn't exists")
def disp_transaction_records():
    try:
        cmd="select * from transaction order by id"
        mycursor.execute(cmd)
        f="%30s %30s %30s %30s %30s"
        print(f%("date","c_id", "id","sold_price", "units_sold"))
        print("=" * 155)
        for i in mycursor:
            for j in i:
                print("%30s" %j, end='')
            print()
        print("=" * 155)
    except:
        print("Table doesn't exists")
def dispsearchid():
    # function to search for the records from product table with id number
    try:
        cmd="Select * from product"
        mycursor.execute(cmd)
        ch=input("Enter id to be searched:")
        found = False
        for i in mycursor:
            if i[0].strip()==ch:
                f="%32s %32s %40s"
                print(f%("id", "name", "category"))
                print("="*125)
                for j in i:
                    print("%40s" %j, end='')
                print()
                print("=" * 125)
                found = True
                break
        if(not(found)):
            print("Record with id: %s not found"%(ch))
    except:
        print("Table doesn't exist")
def dispsearchstock_id():
    #function to search for the records from stock table w.r.t id number
    try:
        cmd = "Select s.id,s.purchase_price,s.selling_price,(s.units) as units from stock as s"
        mycursor.execute(cmd)
        ch = input("Enter stock id to be searched:")
        found = False
        for i in mycursor:
            if i[0].strip() == ch:
                f="%24s %38s %33s %22s"
                print(f%("id","purchase_price", "selling_price","units"))
                print("=" * 125)
                for j in i:
                     print("%30s" %j, end='')
                print()
                print("=" * 125)
                found = True
                break
        if(not(found)):
            print("Stock record with id: %s not found"%ch)
    except:
        print("Table doesn't exist")
def updated_stock(units_s,id_input):
    # function to update stock table w.r.t stock id
    cmd="update stock set units=units-%s where stock.id=%s"
    val=(units_s,id_input)
    mycursor.execute(cmd,val)
    mydb.commit()
def update_s():
    try:
        cmd="select * from stock"
        mycursor.execute(cmd)
        A=input("Enter the stock id whose details need to be changed: ")
        found=False
        for i in mycursor:
            i=list(i)
            if i[0].strip()==A:
                ch=input("change purchase_price(Y/N):")
                if ch=='y' or ch=='Y':
                     i[1]=input("Enter purchase_price:")
                ch=input("Change selling_price(Y/N):")
                if ch=='y' or ch=='Y':
                     i[2]=input("Enter selling_price:")
                ch=input("Change units(Y/N):")
                if ch=='y' or ch=='Y':
                     i[3]=input("Enter units:")
                cmd="update stock SET  purchase_price=%s, selling_price=%s,units=%s where id=%s"
                val=(i[1],i[2],i[3],i[0])
                mycursor.execute(cmd,val)
                mydb.commit()
                print("Id updated")
                found=True
                break
        if(not(found)):
                print("Stock record with id: %s not found"%A)
    except:
         print("No such details")
def delete():
    # function to delete records from stock table
    try:
        cmd="Select * from stock"
        mycursor.execute(cmd)
        A=input("Enter the stock Id number whose details need to be deleted: ")
        found=False
        for i in mycursor:
            i=list(i)
            if i[0].strip()==A:
                cmd="Delete from stock where id=%s"
                val=(i[0],)
                mycursor.execute(cmd,val)
                mydb.commit()
                print("Id Deleted")
                found=True
                break
        if(not(found)):
                print("Stock record with id: %s not found"%A)
    except:
        print("No such Table")
while True:
    menu()
    ch=input("Enter your choice:")
    if ch=='1':
         create_p()
    elif ch=='2':
         create_stock()
    elif ch=='3':
         create_transaction()
    elif ch=='4':
         while True:
              menu_sort()
              ch1=input("Enter your choice a/b/c:")
              if ch1 in ['a','A']:
                   dispsortid()
              elif ch1 in ['b','B']:
                   dispsortcategory()
              elif ch1 in ['c','C']:
                   print("Back to the main menu")
                   break
              else:
                   print("Invalid choice")
    elif ch=='5':
         while True:
              menu_sort_stock()
              ch1=input("Enter your choice a/b/c: ")
              if ch1 in ['a','A']:
                   dispsortid_stock()
              elif ch1 in ['b','B']:
                   dispsortunits()
              elif ch1 in ['c','C']:
                   print("Back to the main menu")
                   break
              else:
                   print("Invalid choice")
    elif ch=='6':
         disp_transaction_records()
    elif ch=='7':
         dispsearchid()
    elif ch=='8':
         dispsearchstock_id()
    elif ch=='9':
         update_s()
    elif ch=='10':
          delete()
    elif ch=='11':
          print("Exiting..")
          break
    else:
          print("Wrong choice entered")
