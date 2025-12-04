from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.list import MDList , TwoLineIconListItem , IconLeftWidget
from datetime import *
from note_database import NoteDatabase
from kivymd.uix.label import MDLabel
from kivymd.uix.menu import MDDropdownMenu
from kivy.core.window import Window

Builder.load_string(""" 

<content>:
    id: dialog
    orientation: "vertical"
    spacing: "12dp"
    size_hint_y: None
    height: "120dp"

    MDTextField:
        id: note_title
        hint_text: "Add Title"
        pos_hint: {"center_x": .5}
        multiline: False

    MDRectangleFlatButton:
        text: "Create Note"
        pos_hint: {"center_x": .5}
        size_hint_x: 1
        on_release: app.add_note(self , note_title.text)

<ask_to_go_back>:
    id: ask_to_go_back_dialog
    orientation: "vertical"
    spacing: "12dp"
    size_hint_y: None
    height: "120dp"

    MDLabel:
        text: "You have unsaved changes. Do you want to save changes?"
        halign: "center"
        font_size: "15sp"
        size_hint_y: .3
        theme_text_color: 'Hint'
    MDBoxLayout:
        orientation: "horizontal"
        spacing: dp(20)
        padding: [dp(12), 0, dp(12), dp(12)]  # left, top, right, bottom
        size_hint: (None , None)
        width: self.minimum_width
        height: self.minimum_height
        pos_hint: {"center_x":.5}

        MDRaisedButton:
            text: "Save Changes"
            md_bg_color: self.theme_cls.primary_color
            size_hint_x: .4
            on_release: app.save_note_and_go_back(self)
        MDRectangleFlatButton:
            text: "Discard Changes"
            size_hint_x: .4
            on_release: root.discard_changes_and_go_back(self)

<Mainscreen>:
    MDTopAppBar:
        title: "Your Notes"
        md_bg_color: self.theme_cls.primary_color
        pos_hint: {"center_y":.95}
        left_action_items: [["dots-vertical", lambda x: app.callback(x)]]

    MDScrollView:
        pos_hint: {"top":.89}

        MDList:
            id: scroll

    MDIconButton:
		icon: "plus"
		theme_icon_color: "Custom"
		md_bg_color: self.theme_cls.primary_color
		pos_hint: {"center_x": .5 , "center_y": .07}
		icon_size: "35sp"
		on_release: root.add_note_window()

<Notescreen>:
    MDTopAppBar:
        id: top_bar
        title: "Note"
        md_bg_color: self.theme_cls.primary_color
        pos_hint: {"center_y":.95}
        left_action_items: [["arrow-left", lambda x: root.ask_before_go_back()]]
    MDTextField:
        id: note_content
        hint_text: "Write Something here..."
        font_size: "20sp"
        size_hint: (.9 , .6)
        pos_hint: {"center_x":.5, "center_y":.58}
        multiline: True
        mode: "rectangle"

    MDBoxLayout:
        orientation: "horizontal"
        spacing: dp(40)
        padding: [0,0,0,0]
        size_hint: (None , None)
        width: self.minimum_width
        height: self.minimum_height
        pos_hint: {"center_x":.5 , "center_y":.1}
        #md_bg_color: (1,1,1,1)
        
        MDFloatingActionButton:
            icon: "content-save"
            md_bg_color: self.theme_cls.primary_color
            on_release: app.save_note_and_go_back()
        MDFloatingActionButton:
            icon: "trash-can"
            md_bg_color: self.theme_cls.primary_color
            theme_icon_color: "Custom"
            icon_color: (1,0,0,1)
            on_release: root.show_confirm_dialog()

""")

class Mainscreen(Screen):
    def add_note_window(self):
        dialog = MDDialog(
            title="Add Note",
            type="custom",
            content_cls=content())
        dialog.open()

class content(BoxLayout):
    pass
class ask_to_go_back(BoxLayout):
    
    def discard_changes_and_go_back(self, instance):
        app = MDApp.get_running_app()
        note_screen = app.root.get_screen("notescreen")
        note_screen.ids.note_content.text = ''
        app.root.current = "mainscreen"
        app.root.transition.direction = "right"
        instance.parent.parent.parent.parent.parent.dismiss()

class Notescreen(Screen):
    def delete_note(self, instance):
        self.note_db = NoteDatabase()
        self.note_db.delete_note(self.ids.top_bar.title)
        app = MDApp.get_running_app()
        mainscreen = app.root.get_screen("mainscreen")
        mainscreen.ids.scroll.clear_widgets()
        app.on_start()
        self.ids.note_content.text = ''
        self.dialog.dismiss()
        self.manager.current = "mainscreen"
        self.manager.transition.direction = "right"

    def show_confirm_dialog(self):
        app = MDApp.get_running_app()
        self.dialog = MDDialog(
            text= "Are you sure, you want to delete this Note",
            title = "INFO",
            buttons= [
            MDRectangleFlatButton(text="CANCEL", theme_text_color="Custom", text_color=app.theme_cls.primary_color,  on_release= lambda x: self.dialog.dismiss()),
            MDRectangleFlatButton(text="DELETE", theme_text_color="Custom", text_color=app.theme_cls.primary_color,  on_release= self.delete_note)
            ],)
        self.dialog.open()
    
    def ask_before_go_back(self):
        self.note_db = NoteDatabase()
        app = MDApp.get_running_app()
        mainscreen = app.root.get_screen("mainscreen")
        if self.ids.note_content.text != '' or not self.ids.note_content.text.strip():
            self.dialog = MDDialog(
                title="Unsaved changes",
                type="custom",
                content_cls=ask_to_go_back())
            specific_note = self.note_db.get_specific_note(self.ids.top_bar.title)
            if specific_note is None:
                self.dialog.open()
                mainscreen.ids.scroll.clear_widgets()
                app.on_start()
            
            elif specific_note[1] is not None and specific_note[1] != self.ids.note_content.text:
                self.dialog.open()

            elif specific_note[1] is not None and specific_note[1] != self.ids.note_content.text and not self.ids.note_content.text.strip():
                self.dialog.open()

            elif specific_note[1] is not None and specific_note[1] == self.ids.note_content.text:
                self.ids.note_content.text = ''
                self.manager.current = "mainscreen"
                self.manager.transition.direction = "right"
            
        else:
            self.ids.note_content.text = ''
            self.manager.current = "mainscreen"
            self.manager.transition.direction = "right"

class MyApp(MDApp):
    
    def build(self):
        self.theme_cls.primary_palette = "DeepPurple"
        self.theme_cls.theme_style = "Dark"
        sm = ScreenManager()
        sm.add_widget(Mainscreen(name="mainscreen"))
        sm.add_widget(Notescreen(name="notescreen"))
        Window.size = (430,600)
        #sm.current = "notescreen"
        self.note_db = NoteDatabase()
        menu_item =[{"viewclass": "OneLineListItem", 
										"text": "About", "height":dp(56), "on_release": lambda: self.show_about()}]
        self.menu = MDDropdownMenu(width_mult=1, items=menu_item)
        return sm
    
    def callback(self, button):
        self.menu.caller = button
        self.menu.open()
    
    def show_about(self):
        self.dialog = MDDialog(
            title="About",
            text="Simple Notes — a minimal, offline note-taking app built with KivyMD.\nCreate, edit, and delete notes locally.\n Version-1.0",
            buttons=[MDRectangleFlatButton(text="CLOSE", on_release=lambda x: self.dialog.dismiss())],
        )
        self.dialog.open()
    
    def on_start(self):
        notes = self.note_db.get_all_notes()
        mainscreen = self.root.get_screen("mainscreen")
        if notes == []:
            label = MDLabel(text="No Notes Yet!, Create one!",
											halign = "center",
											font_style= "H5",
											size_hint_y = None,
											height = "100sp",
											theme_text_color= "Hint")
            mainscreen.ids.scroll.add_widget(label)
        else:
            for note in notes:
                self.note = TwoLineIconListItem(text=note[0],secondary_text=note[2],on_release= lambda x: self.show_note(x))
                self.note.add_widget(IconLeftWidget(icon="note-outline"))
                mainscreen.ids.scroll.add_widget(self.note)
    
    def show_note(self, instance):
        specific_note = self.note_db.get_specific_note(instance.text)
        note_screen = self.root.get_screen("notescreen")
        note_screen.ids.top_bar.title = specific_note[0]
        note_screen.ids.note_content.text = specific_note[1]
        self.root.current = "notescreen"
        self.root.transition.direction = "left"

    def add_note(self, instance, title):
        notes = self.note_db.get_all_notes()
        if title != "" and title not in [notes[0] for notes in notes]:
            note_screen = self.root.get_screen("notescreen")
            note_screen.ids.top_bar.title = title
            self.root.current = "notescreen"
            self.root.transition.direction = "left"
            instance.parent.parent.parent.parent.dismiss()
        else:
            self.dialog_2 = MDDialog(text="You cannot Add same Note again", buttons=[MDRectangleFlatButton(text="OK",on_release=lambda x:self.dialog_2.dismiss())])
            self.dialog_2.open()
    
    def save_note_and_go_back(self, instance=None):
        notescreen = self.root.get_screen("notescreen")
        mainscreen = self.root.get_screen("mainscreen")
        specific_note = self.note_db.get_specific_note(notescreen.ids.top_bar.title)
        if notescreen.ids.note_content.text != "" or not notescreen.ids.note_content.text.strip():
            if specific_note is None:
                time = datetime.now().strftime("%d %b %Y | %I:%M %p")
                self.note_db.add_note(notescreen.ids.top_bar.title, notescreen.ids.note_content.text, time)
                self.note = TwoLineIconListItem(text=notescreen.ids.top_bar.title,secondary_text=time,on_release= lambda x: self.show_note(x))
                self.note.add_widget(IconLeftWidget(icon="note-outline"))
                mainscreen.ids.scroll.add_widget(self.note)
                notescreen.ids.note_content.text = ''
                instance.parent.parent.parent.parent.parent.dismiss() if instance else None
                mainscreen.ids.scroll.clear_widgets()
                self.on_start()
                self.root.current = "mainscreen"
                self.root.transition.direction = "right"
            
            elif specific_note is not None and notescreen.ids.note_content.text == specific_note[1]:
                notescreen.ids.note_content.text = ''
                self.root.current = "mainscreen"
                self.root.transition.direction = "right"
            
            elif specific_note is not None and specific_note[1] != notescreen.ids.note_content.text and notescreen.ids.note_content.text != "":
                time = datetime.now().strftime("%d %b %Y | %I:%M %p")
                self.note_db.update_note(notescreen.ids.top_bar.title, notescreen.ids.note_content.text, time)
                notescreen.ids.note_content.text = ''
                mainscreen.ids.scroll.clear_widgets()
                self.on_start()
                self.root.current = "mainscreen"
                self.root.transition.direction = "right"
                instance.parent.parent.parent.parent.parent.dismiss() if instance else None
            
            elif specific_note is not None and specific_note[1] != notescreen.ids.note_content.text and not notescreen.ids.note_content.text.strip():
                time = datetime.now().strftime("%d %b %Y | %I:%M %p")
                self.note_db.update_note(notescreen.ids.top_bar.title, f"", time)
                notescreen.ids.note_content.text = ''
                mainscreen.ids.scroll.clear_widgets()
                self.on_start()
                self.root.current = "mainscreen"
                self.root.transition.direction = "right"
                instance.parent.parent.parent.parent.parent.dismiss() if instance else None
        else:
            notescreen.ids.note_content.text = ''
            self.root.current = "mainscreen"
            self.root.transition.direction = "right"

if __name__ == "__main__":
    MyApp().run()