import flet as ft
from flet import *
from bsdclass import bsdinteraction
from table import Tables
from pages import AppState,LoginPage,RegisterPage,DashboardPage,ProfilePage,FormPage
from appstatus import AppState


# FUNCION QUE INICIA LA APLICACIÓN
def main(page: ft.Page):
    page.title = "Correos de Yury"
    page.vertical_alignment = MainAxisAlignment.START
    page.window_maximized = True

    conex=bsdinteraction()
    conex.connection()
    app_state=AppState()
    dashboard_page = DashboardPage(page,app_state)

    # Función que maneja el cambio de rutas
    def route_change(e: RouteChangeEvent) -> None:
        page.views.clear()
        if page.route == "/":
            login_page = LoginPage(page,app_state)
            page.views.append(
                ft.View(
                    "/",
                    bgcolor="#3e4e84",
                    controls=[login_page.login_card],
                    vertical_alignment=MainAxisAlignment.CENTER,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                    spacing=10
                )
            )
    
        elif page.route == "/crear_cuenta":
            register_page = RegisterPage(page)
            page.views.append(
                ft.View(
                    "/crear_cuenta",
                    bgcolor="#3e4e84",
                    controls=[register_page.register_card],
                    vertical_alignment=MainAxisAlignment.CENTER,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                    spacing=10
                )
            )
            
        elif page.route == "/inicio":
            dashboard_page.build_dashboard_page()
            page.views.append(
                ft.View(
                    "/inicio",
                    bgcolor="#3e4e84",
                    controls=[dashboard_page.inicio,dashboard_page.navbar],
                    vertical_alignment=MainAxisAlignment.CENTER,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                    spacing=10
                )
            )
            
        elif page.route == "/cuenta":
            profile =ProfilePage(page,app_state)
            profile.show_data()
            dashboard_page.build_account_page()
            page.views.append(
                ft.View(
                    "/cuenta",
                    bgcolor="#3e4e84",
                    controls=[dashboard_page.navbar,profile.get_card()],
                    vertical_alignment=MainAxisAlignment.CENTER,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                    spacing=10
                )
            )
        elif page.route == "/tables":
            mydt = Tables(page)
            table = mydt.datatable()
            filter_ui = mydt.table()
            dashboard_page.build_lista_emp()
            page.views.append(
                ft.View(
                    "/tables",
                    bgcolor="#3e4e84",
                    controls=[dashboard_page.navbar, filter_ui],
                    vertical_alignment=MainAxisAlignment.CENTER,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                    spacing=10
                )
            )
            
            
        elif page.route == "/formularios":
            dashboard_page.build_forms()
            form=FormPage(page,app_state)
            
            page.views.append(
                ft.View(
                    "/formularios",
                    bgcolor="#3e4e84",
                    scroll=True,
                    controls=[dashboard_page.navbar,form.get_card()],
                    vertical_alignment=MainAxisAlignment.CENTER,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                    spacing=10,
                )
            ) 
        page.update()

    # Función que maneja el evento de retroceder
    def view_pop(e: ViewPopEvent) -> None:
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)

ft.app(target=main)