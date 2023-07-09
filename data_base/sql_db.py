from create_bot import bot
import pymysql.cursors

class sqldb():
    connection = pymysql.connect(host='',
                             port = ,user='',
                             password='',
                             database='',
                             cursorclass=pymysql.cursors.DictCursor)

def sql_start():
    if sqldb.connection:
        with sqldb.connection.cursor() as cursor:
            create_table_query = "CREATE TABLE IF NOT EXISTS `pizzaOrders`(`id` int(11) NOT NULL AUTO_INCREMENT," \
                                 " `order`varchar(250) ," \
                                 "`adress` varchar(50)," \
                                 "`price` varchar(50),PRIMARY KEY (`id`))"
            cursor.execute(create_table_query)
            print('Data base connected Ok!')
            sqldb.connection.commit()
            

async def sql_add_command(order):
    with sqldb.connection.cursor() as cursor:
        insert_query = 'INSERT INTO `pizzaOrders` (`order`,`adress`,`price`) VALUES (%s,%s,%s)'
        cursor.execute(insert_query,tuple(order))
        sqldb.connection.commit()
    # cur.execute('INSERT INTO menu VALUES (?,?,?,?)', tuple(data.values()))


# async def sql_read(message):
#     with connection.cursor() as cursor:
#         select_all_rows = 'SELECT * FROM `menu`'
#         cursor.execute(select_all_rows)
#         rows = cursor.fetchall()
#         for row in rows:
#             await bot.send_photo(message.from_user.id, row['img'], f'{row["name"]}\n Description: {row["description"]}\n Price: {row["price"]}')

# async def sql_read2():
#     with connection.cursor() as cursor:
#         cursor.execute('SELECT * FROM `orders`')
#         return cursor.fetchall()

# async def sql_delete_command(data):
#     with connection.cursor() as cursor:
#         delete_query = "DELETE FROM `menu` WHERE name = %s;"
#         cursor.execute(delete_query,(data,))
#         connection.commit()

