import UserController
controller = UserController()

while True:
    select_nenu = int(input('메뉴 번호 입력'))
    match select_nenu:
        case 1 :            
            controller.print_list()
        case 2 :
            controller.search_user()
        case 3 :
            controller.add_user(controller.input_user())            
        case 4 :
            controller.edit_user()
        case 5 :
            controller.delete_user()
        case 6 :
            print('프로그램을 종료합니다.')
            break
        case _ :
            print('정확한 메뉴를 입력해주세요')