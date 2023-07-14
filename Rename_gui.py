# GUI IMPORT 
import flet as ft
from flet import ElevatedButton, FilePicker, FilePickerResultEvent, Text, icons
#RENAME FILES IMPORT
import os
import shutil


def main(page: ft.Page):
    # ALTER DIALOG WHEN A SPACE IS EMPTY
    dlg = ft.AlertDialog(
        title=ft.Text("Something is empty wachuchi"), on_dismiss=lambda e: None)

    def open_dlg(e):
        page.dialog = dlg
        dlg.open = True
        page.update()
    # RENAME FUNCTION SHUTIL
    def rename_files(e):
        if directory_path.value is None:
            open_dlg(e)
        else:
            for filename in os.listdir(directory_path.value):
                try:
                    if word_del.value in filename and (file_exten.value == "" or filename.endswith(file_exten.value)):
                        new_filename = filename.replace(word_del.value, word_new.value)
                        old_path = os.path.join(directory_path.value, filename)
                        new_path = os.path.join(directory_path.value, new_filename)
                        shutil.move(old_path, new_path)
                except:
                    open_dlg(e)
    
    # PAGE THINGS
    page.title = "Flet Rename Files"
    page.window_width = 600        # window's width is 200 px
    page.window_height = 800       # window's height is 200 px
    page.window_resizable = False  # window is not resizable

    # ROUte thin to change page
    def route_change(route):
        page.views.clear()
        page.views.append(
            ft.View(
                "/",
                [
                    ft.AppBar(title=ft.Text("Flet app"), bgcolor=ft.colors.SURFACE_VARIANT),
                    ft.ElevatedButton("Rename GUI", on_click=lambda _: page.go("/rename")),
                ],
            )
        )
        if page.route == "/rename":
            page.views.append(
                ft.View(
                "/",
                [
                    ft.AppBar(title=ft.Text("Rename GUI"), bgcolor=ft.colors.SURFACE_VARIANT),
                    path_btn, directory_path,
                    ft.Row([word_del, file_exten]),
                    word_new,
                    ft.ElevatedButton(text="Action", on_click=rename_files)
                ],
                )
            )
        page.update()
            
    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    # PATH NECESSARY
    def get_directory_result(e: FilePickerResultEvent):
        directory_path.value = e.path if e.path else "Cancelled!"
        directory_path.update()

    get_directory_dialog = FilePicker(on_result=get_directory_result)
    directory_path = Text()
    page.overlay.extend([get_directory_dialog])

    # THINGS TO ADD TO PAGE.ADD
    path_btn = ElevatedButton(
        "Folder Path",
        icon=icons.FOLDER_OPEN,
        on_click=lambda _: get_directory_dialog.get_directory_path(),
        disabled=page.web
    )
    
    word_del = ft.TextField(hint_text='Word to delete', width=300)
    file_exten = ft.TextField(hint_text='Extension', width=90)
    word_new = ft.TextField(hint_text='New Word, empty to delete', width=300)

    page.add( 
        path_btn, directory_path,
        ft.Row([word_del, file_exten]),
        word_new,
        ft.ElevatedButton(text="Action", on_click=rename_files)
    )
    


    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)

ft.app(target=main)
