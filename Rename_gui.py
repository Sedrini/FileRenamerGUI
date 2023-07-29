import flet as ft
import os
import shutil
# Scripts
from Tools import rename_foiles, move_files

class RenameGUI:
    def __init__(self, page):
        self.page = page
        self.setup_widgets()
        self.page.on_route_change = self.route_change
        self.page.on_view_pop = self.view_pop
        self.page.go(self.page.route)

    def setup_widgets(self):
        self.page.title = "Flet Rename Files"
        self.page.window_width = 600
        self.page.window_height = 700
        self.page.window_resizable = False


        # Move bun
        self.get_directory_dialog2 = ft.FilePicker(on_result=self.get_directory_move)
        self.directory_move = ft.Text()
        self.page.overlay.extend([self.get_directory_dialog2])
        # ALTER DIALOG WHEN A SPACE IS EMPTY
        self.get_directory_dialog = ft.FilePicker(on_result=self.get_directory_result)
        self.directory_path = ft.Text()
        self.page.overlay.extend([self.get_directory_dialog])
        #Menu Widgets
        self.rename_go = ft.ElevatedButton("Rename GUI", on_click=lambda _: self.page.go("/rename"))
        self.move_go = ft.ElevatedButton("Move GUI", on_click=lambda _: self.page.go("/move"))
        #Rename Widgets
        self.path_btn = ft.ElevatedButton("Folder",icon=ft.icons.FOLDER_OPEN,
        on_click=lambda _: self.get_directory_dialog.get_directory_path(), disabled=self.page.web,)

        self.re_switch = ft.Switch(label="Sub-Files", value=False)
        self.dir_switch = ft.Switch(label="Folders Mode", value=False, on_change=self.dir_mode)
        self.word_del = ft.TextField(hint_text="Word to delete", width=300)
        self.file_exten = ft.TextField(hint_text="Extension", width=100,disabled=False)
        self.word_new = ft.TextField(hint_text="New Word, empty to delete", width=300)
        # Move Widgets
        self.reversepath = ft.Switch(label="Reverse", value=False)
        self.path_move = ft.ElevatedButton("Folder2",icon=ft.icons.FOLDER_OPEN,
        on_click=lambda _: self.get_directory_dialog2.get_directory_path(), disabled=self.page.web,)



    # Scripts to a
    def rename_script(self, e):
        if self.directory_path.value is None:
            self.open_dlg(e)
        else:
            try:
                rename_foiles(
                    directory_path=self.directory_path.value,
                    re_switch=self.re_switch.value,
                    word_del=self.word_del.value,
                    file_exten=self.file_exten.value,
                    word_new=self.word_new.value,dir_mode=self.dir_switch.value,
                )
            except Exception as ex:
                self.open_dlg(e)
    
    def dir_mode(self, e):
        if self.dir_switch.value == True:
            self.file_exten.disabled = True
        else:
             self.file_exten.disabled = False
        self.page.update()


    def move_files(self, e):
        if self.directory_path.value is None or self.directory_move.value is None or self.directory_path.value == self.directory_move.value :
            self.open_dlg(e)

        try:
            move_files(
                directory_path=self.directory_path.value,
                directory_move=self.directory_move.value,
                reversepath=self.reversepath.value,
                re_switch=self.re_switch.value,
                file_exten=self.file_exten.value,
            )
        except Exception as ex:
            self.open_dlg(e)

            if self.reversepath.value:
                # Swap the values back to their original positions after moving the files
                self.directory_path.value, self.directory_move.value = self.directory_move.value, self.directory_path.value

    #Finish scripts
    def open_dlg(self, e):
        self.dlg = ft.AlertDialog(title=ft.Text("Something is empty wachuchi"), on_dismiss=lambda e: None) # Alert when a textfield is empty
        self.page.dialog = self.dlg
        self.dlg.open = True
        self.page.update()


    def get_directory_result(self, e: ft.FilePickerResultEvent):
        self.directory_path.value = e.path if e.path else "Cancelled"
        self.directory_path.update()

    def get_directory_move(self, e: ft.FilePickerResultEvent):
        self.directory_move.value = e.path if e.path else "Cancelled"
        self.directory_move.update()


    def route_change(self, route):
        self.page.views.clear()
        self.page.views.append(
            ft.View(
                "/",
                [
                    ft.AppBar(title=ft.Text("Flet app"), bgcolor=ft.colors.SURFACE_VARIANT),
                    ft.Row([self.rename_go,self.move_go])
                ],
            )
        )
        if self.page.route == "/rename":
            self.page.views.append(
                ft.View(
                    "/rename",
                    [
                        ft.AppBar(title=ft.Text("Rename GUI"), bgcolor=ft.colors.SURFACE_VARIANT),
                        ft.Row([self.path_btn, self.re_switch,self.dir_switch]),
                        self.directory_path,
                        ft.Row([self.word_del, self.file_exten]),
                        self.word_new,
                        ft.ElevatedButton(text="Action", on_click=self.rename_script),
                    ],
                )
            ),
        elif self.page.route == "/move":
            self.page.views.append(
                ft.View(
                    "/move",
                    [
                        ft.AppBar(title=ft.Text("Move GUI"), bgcolor=ft.colors.SURFACE_VARIANT),
                        ft.Row([self.path_btn ,self.path_move,self.re_switch,self.reversepath]),
                        ft.Row([self.file_exten]),
                        ft.Text('From here: '),self.directory_path,ft.Text('To here: '),self.directory_move,
                        ft.ElevatedButton(text="Action", on_click=self.move_files),

                    ],
                )
            )

        self.page.update()


    def view_pop(self, view):
        self.page.views.pop()
        top_view = self.page.views[-1]
        self.page.go(top_view.route)


ft.app(target=RenameGUI)
