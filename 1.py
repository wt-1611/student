import os
filename='student.txt'
def main():
    while True:
        menu()
        choice=int(input('请选择:'))
        if choice in [1,2,3,4,5,6,7,0]:
            if choice == 0:
                answer = input('您确定要退出系统吗？y/n')
                if answer == 'y' or answer == 'Y':
                    print('谢谢使用')
                    break
                else:
                    continue
            elif choice == 1:
                insert() # 录入学生信息
            elif choice == 2:
                search()
            elif choice == 3:
                delete()
            elif choice == 4:
                modify()
            elif choice == 5:
                sort()
            elif choice == 6:
                total()
            elif choice == 7:
                show()


def menu():
    print('学生信息管理系统'.center(20,'='))
    print('功能菜单'.center(20,'='))
    print('1.录入学生信息'.center(20))
    print('2.查看学生信息'.center(20))
    print('3.删除学生信息'.center(20))
    print('4.修改学生信息'.center(20))
    print('5.排序'.center(16))
    print('6.统计学生总人数'.center(21))
    print('7.显示所有学生信息'.center(21))
    print('0.退出'.center(16))


def insert():
    student_list = []
    while True:
        id = input('请输入ID:')
        if not id:
            break
        name = input('请输入姓名:')
        if not name:
            break

        try:
            englist=int(input('请输入英语成绩:'))
            python=int(input('请输入python成绩:'))
            java=int(input('请输入java成绩:'))

        except:
            print('输入无效，不是整数类型,请重新输入')
            continue
        # 将录入的学生信息保存到字典中
        student = {'id':id,'name':name,'englist':englist,'python':python,'java':java}
        # 将学生信息添加到列表中
        student_list.append(student)
        answer = input('是否继续添加？y/n')

        if answer == 'y' or answer == 'Y':
            continue
        else:
            break

    # 调用save()函数
    save(student_list)
    print('学生信息录入完毕！！')

def save(lst):
    try:
        stu_txt = open(filename,'a',encoding='utf-8')
    except:
        stu_txt = open(filename,'w',encoding='utf-8')

    for item in lst:
        stu_txt.write(str(item)+'\n')
    stu_txt.close()

def search():
    student_query = []
    while True:
        id = ''
        name = ''
        if os.path.exists(filename):
            mode = input('按学生id查找输入1,按学生姓名查找输入2：')
            if mode == '1':
                id = input('请输入学生id：')
            elif mode == '2':
                name = input("请输入学生姓名：")
            else:
                print('输入无效！')
                search()
            with open(filename,'r',encoding='utf-8') as rfile:
                student = rfile.readlines() # 列表
                for item in student:
                    d=eval(item)
                    if id != '':
                        if d['id'] == id:
                            student_query.append(d)
                    elif name != '':
                        if d['name'] == name:
                            student_query.append(d)
            # 显示查询结果
            show_student(student_query)
            # 清空列表
            student_query.clear()
            answer = input('是否继续查询？y/n')
            if answer == 'y':
                continue
            else:
                print('暂时保存学生信息')
                return 0
        else:
            print('暂未保存学生信息')
            return 1

def show_student(lst):
    # 如果列表长度为0
    if len(lst) == 0:
        print('没有查询到学生信息，无数据显示')
        return 1
    # 定义标题的显示格式
    format_title='{:^6}\t{:^12}\t{:^8}\t{:^10}\t{:^10}\t{:^8}'
    print(format_title.format('ID','姓名','英语成绩','python成绩','java成绩','总成绩'))
    # 定义内容显示格式
    format_data='{:^6}\t{:^12}\t{:^8}\t{:^10}\t{:^10}\t{:^8}'
    for item in lst:
        avg=int(item.get('englist'))+int(item.get('python'))+int(item.get('java'))

        print(format_data.format(item.get('id'),item.get('name'),item.get('englist'),item.get('python'),item.get('java'),avg))

def delete():
    while True:
        student_id = input('请输入要删除学生的id:')
        if student_id != '':
            if os.path.exists(filename):
                with open(filename,'r',encoding='utf-8') as file:
                    student_old = file.readlines()
            else:
                student_old=[]
            flag = False # 标记是否删除
            if student_old:
                with open(filename,'w',encoding='utf-8') as wfile:
                    #d={}
                    for  item in student_old:
                        d=eval(item)  # eval() 函数用来执行一个字符串表达式，并返回表达式的值。.例如：print(eval('5+3'))输出8
                        if d['id'] != student_id:
                            wfile.write(str(d)+'\n')
                        else:
                            flag=True # 已删除
                    if flag:
                        print(f'id为{student_id}的学生信息已经被删除')
                    else:
                        print(f'没有找到id为{student_id}的学生信息')
            else:
                print('无学生信息')
                break
            show() # 删除后显示所有学生信息
            answer = input('是否继续删除？y/n')
            if answer == 'y' or answer == 'Y':
                continue # 退出当前while中的本次循环
            else:
                break # 退出当前while中的循环


def modify():
    show()
    if os.path.exists(filename):
        with open(filename,'r',encoding ='utf-8') as rfile:
            student_old = rfile.readlines() # 存入列表
    else:
        return 1
    student_id = input('请输入要修改的学员id:')
    if student_id != '':
        with open(filename,'w',encoding='utf-8') as wfile:
            for item in student_old:
                d = eval(item)
                if d['id'] == student_id:
                    print('找到学生信息，可以修改他的相关信息！')
                    while True:
                        try:
                            d['name']=input('请输入姓名：')
                            d['englist']=int(input('请输入英语成绩'))
                            d['python']=int(input('请输入python成绩'))
                            d['java']=int(input('请输入java成绩'))
                        except:
                            print('您的输入有误请重新输入')
                        else:
                            break
                    wfile.write(str(d)+'\n')
                    print('修改成功！！！')
                else:
                    wfile.write(str(d)+'\n')
        answer=input('是否继续修改其他学生信息：y/n：')
        if answer == 'y':
            modify()
    else:
        print('请输入学员id！！！')



def sort():
    show()
    if os.path.exists(filename):
        with open(filename,'r',encoding='utf-8') as rfile:
            student_lst = rfile.readlines()
        student_new = []
        for item in student_lst:
            d = eval(item)
            student_new.append(d)

    else:
        return
    asc_or_desc = input('请选择（0.升序,1.降序）')
    if asc_or_desc == '0':
        asc_or_desc = False
    elif asc_or_desc == '1':
        asc_or_desc = True
    else:
        print('您输入有误请重新输入！！')
        sort()
    mode = input('请选择排序方式(1.按英语成绩排序，2.按python成绩排序，3.按java程序排序，0.按照总成绩排序)：')



    if mode == '1':
        # 实例方法在调用的时候 会默认传递实例对象回去 ，这个实例对象就被当作 匿名函数的实参了
        student_new.sort(key=lambda x : int(x['englist']),reverse=asc_or_desc)
    elif mode == '2':
        student_new.sort(key=lambda x : int(x['python']),reverse=asc_or_desc)
    elif mode == '3':
        student_new.sort(key=lambda x : int(x['java']),reverse=asc_or_desc)
    elif mode == '0':
        student_new.sort(key=lambda x : int(x['englist'])+int(x['java'])+int(x['python']),reverse=asc_or_desc)
    else:
        print('您输入有误会，请重新输入！')
        sort()
    show_student(student_new)



def total():
    if os.path.exists(filename):
        with open(filename,'r',encoding='utf-8') as rfile:
            students = rfile.readlines() # 存储到列表
            if students:
                print(f'一共有{len(students)}名学生')
            else:
                print('还没有录入学生信息！')
    else:
        print('暂未保存数据！')

def show():
    student_lst = []
    if os.path.exists(filename):
        with open(filename,'r',encoding='utf-8') as rfile:
            students = rfile.readlines()
            for item in students:
                student_lst.append(eval(item))
            if student_lst:
                show_student(student_lst)
    else:
        print('暂未保存数据')

if __name__ == '__main__':
    main()


