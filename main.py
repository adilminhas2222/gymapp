import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.uix.dropdown import DropDown
from kivy.uix.textinput import TextInput
from kivy.properties import StringProperty
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.graphics import Rectangle, Color
from kivy.core.text import LabelBase
import kivy.utils
from functools import partial
import datetime
import calendar
import backend
import certifi
import time
import json


class CurrentData:
    current_user = ["", "", "", "", ""]

    def change_user(self, new):
        CurrentData.current_user = new

    def get(self):
        return CurrentData.current_user


class FrontPage(Screen):
    def __init__(self, **kwargs):
        super(FrontPage, self).__init__(**kwargs)

        self.cols = 1

        with self.canvas:
            Color(0.118, 0.137, 0.157, 1)  # set the colour

            # Setting the size and position of canvas
            self.rect = Rectangle(pos=self.center,
                                  size=(self.width * 0.5,
                                        self.height * 0.5))

            # Update the canvas as the screen size change
            self.bind(pos=self.update_rect,
                      size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.x + 8, self.center_y - 700
        self.rect.size = self.width - 100, self.height + 2000


class MainPage(GridLayout, Screen):
    def __init__(self, **kwargs):
        super(MainPage, self).__init__(**kwargs)
        data = backend.MemberData()

        self.page_layout = GridLayout()
        self.page_layout.cols = 2

        self.top_page = GridLayout(cols=3)
        self.top_page.size_hint_y = None
        self.top_page.height = 100

        self.mid_page = GridLayout(cols=1)

        self.cols = 1

        with self.canvas:

            Color(0.118, 0.137, 0.157, 1)  # set the colour

            # Setting the size and position of canvas
            self.rect = Rectangle(pos=self.center,
                                  size=(self.width * 0.5,
                                        self.height * 0.5))

            # Update the canvas as the screen size change
            self.bind(pos=self.update_rect,
                      size=self.update_rect)

        self.refresh_button = Button(text='Refresh', font_size=30, size_hint=[None, None], size=[300, 100],
                                     font_name="Daytona")
        self.refresh_button.bind(on_release=self.refresh)
        self.settings_button = Button(text='Settings', font_size=30, size_hint=[None, None], size=[300, 100],
                                     font_name="Daytona")
        self.settings_button.bind(on_release=self.settings_page)
        self.top_page.add_widget(self.settings_button)
        self.top_page.add_widget(Label())
        self.top_page.add_widget(self.refresh_button)

        self.add_widget(self.top_page)

        self.mid_page.add_widget(Label(text="Paid Members: ", font_size=80, font_name="Daytona"))

        if len(data.accepted) == 0:
            self.mid_page.add_widget(Label(text="No Members Paid", font_size=70, font_name="Daytona"))
        else:
            for dat in data.accepted:
                self.mid_page.add_widget(
                    Label(text=dat[0] + " " + dat[1] + " " + dat[3], font_size=60, font_name="Daytona"))
                # displays first and last name of paid members

        self.add_widget(self.mid_page)

        self.add = Button(text='Add Member', font_size=60, font_name="Daytona")
        self.add.bind(on_release=self.add_page)
        self.page_layout.add_widget(self.add)

        self.find = Button(text='Find Member', font_size=60, font_name="Daytona")
        self.find.bind(on_release=self.find_page)
        self.page_layout.add_widget(self.find)

        self.add_widget(self.page_layout)

    def update_rect(self, *args):
        self.rect.pos = self.center_x - 492, self.center_y - 700
        self.rect.size = self.width - 100, self.height + 2000

    def find_page(self, instance):
        self.manager.transition.direction = "left"
        self.manager.current = "search"

    def add_page(self, instance):
        self.manager.transition.direction = "up"
        self.manager.current = "add"

    def refresh(self, instance):
        data = backend.MemberData()
        self.mid_page.clear_widgets()
        self.mid_page.add_widget(Label(text="Paid Members: ", font_size=80, font_name="Daytona"))

        if len(data.accepted) == 0:
            self.mid_page.add_widget(Label(text="No Members Paid", font_size=70, font_name="Daytona"))
        else:
            for dat in data.accepted:
                self.mid_page.add_widget(
                    Label(text=dat[0] + " " + dat[1] + " " + dat[3], font_size=60, font_name="Daytona"))
                # displays first and last name of paid members

    def settings_page(self, instance):
        self.manager.transition.direction = "down"
        self.manager.current = "settings"

class AddMember(GridLayout, Screen):
    def __init__(self, **kwargs):
        super(AddMember, self).__init__(**kwargs)

        self.page_layout = GridLayout()  # add custom_pay
        self.page_layout.cols = 2

        self.page_bottom = GridLayout()
        self.page_bottom.cols = 2

        self.cols = 1

        with self.canvas:
            Color(0.118, 0.137, 0.157, 1)  # set the colour

            # Setting the size and position of canvas
            self.rect = Rectangle(pos=self.center,
                                  size=(self.width * 0.5,
                                        self.height * 0.5))

            # Update the canvas as the screen size change
            self.bind(pos=self.update_rect,
                      size=self.update_rect)

        self.page_layout.add_widget(Label(text="First Name:", font_size=50, bold=True, font_name="Daytona"))
        self.fname = TextInput(multiline=False)
        self.page_layout.add_widget(self.fname)
        self.page_layout.add_widget(Label(text="Last Name:", font_size=50, bold=True, font_name="Daytona"))
        self.lname = TextInput(multiline=False)
        self.page_layout.add_widget(self.lname)
        self.page_layout.add_widget(Label(text="Phone:", font_size=50, bold=True, font_name="Daytona"))
        self.phone = TextInput(multiline=False)
        self.page_layout.add_widget(self.phone)
        self.submet = Button(text='Submit', font_size=70, font_name="Daytona")
        self.submet.bind(on_release=self.add_member)
        self.page_layout.add_widget(self.submet)

        self.dropdown = DropDown()
        options = ["Gym", "MMA Course", "kids class", "None"]

        for op in options:
            btn = Button(text=op, size_hint_y=None, height=50, width=100, font_name="Daytona")
            btn.bind(on_release=lambda btn: self.dropdown.select(btn.text))
            self.dropdown.add_widget(btn)

        self.mainbutton = Button(text='Membership Type', size_hint=(0.8, 1), font_size=50, font_name="Daytona")
        self.mainbutton.bind(on_release=self.dropdown.open)
        self.dropdown.bind(on_select=lambda instance, x: setattr(self.mainbutton, 'text', x))
        self.page_layout.add_widget(self.mainbutton)
        self.add_widget(self.page_layout)

        self.back = Button(text='Go Back', font_size=80, size_hint_y=0.6, font_name="Daytona")
        self.back.bind(on_release=self.goback)
        self.add_widget(self.back)

    def goback(self, instance):
        self.manager.transition.direction = "down"
        self.manager.current = "main"

    def add_member(self, instance):
        data = backend.MemberData()
        date = str(datetime.datetime.now())
        month = int(date[5:7])
        year = int(date[2:4])
        new_date = str(add_months(datetime.date(year + 2000, month, 28), -1))
        data.new_member(self.fname.text, self.lname.text, self.phone.text, self.mainbutton.text,
                        new_date[5:7] + '/' + new_date[2:4])

        backend.reset_table()

        self.fname.text = ''
        self.lname.text = ''
        self.phone.text = ''
        self.mainbutton.text = 'Membership Type'

    def update_rect(self, *args):
        self.rect.pos = self.center_x - 492, self.center_y - 700
        self.rect.size = self.width - 100, self.height + 2000


class SearchPage(GridLayout, Screen):
    def __init__(self, **kwargs):
        super(SearchPage, self).__init__(**kwargs)

        self.editing = False
        self.removing = False
        self.edit_list = []  # used to hold the textinput objects
        self.member_search = []
        self.members_indexa = []
        self.members_indexr = []

        self.sqlresults = GridLayout(cols=1, spacing=150, size_hint_y=None)
        self.sqlresults.bind(minimum_height=self.sqlresults.setter('height'))

        self.page_layout = GridLayout(cols=2)

        self.button_parent = GridLayout(cols=1)

        self.top_page = GridLayout(cols=3)
        self.top_page.size_hint_y = None
        self.top_page.height = 100

        self.cols = 1

        with self.canvas:
            Color(0.118, 0.137, 0.157, 1)  # set the colour

            # Setting the size and position of canvas
            self.rect = Rectangle(pos=self.center,
                                  size=(self.width * 0.5,
                                        self.height * 0.5))

            # Update the canvas as the screen size change
            self.bind(pos=self.update_rect,
                      size=self.update_rect)

        self.remove = Button(text='Delete Member', font_size=30, size_hint=[None, None], size=[300, 100],
                             font_name="Daytona")
        self.remove.bind(on_release=self.removemember)
        self.top_page.add_widget(self.remove)
        self.top_page.add_widget(Label())
        self.edit = Button(text='Edit Membership', font_size=30, size_hint=[None, None], size=[300, 100],
                           font_name="Daytona")
        self.edit.bind(on_release=self.editmember)
        self.top_page.add_widget(self.edit)
        self.add_widget(self.top_page)
        self.add_widget(Label(text="Search name, phone number or membership",
                              size_hint=[1, None], size=[1000, 150], font_size=28, font_name="Daytona"))

        self.detail = TextInput(multiline=False, size_hint=[1, 1])
        self.page_layout.add_widget(self.detail)
        self.submet = Button(text='Submit', font_size=70, size=[50, 200], font_name="Daytona")
        self.submet.bind(on_release=self.filter)
        self.page_layout.add_widget(self.submet)
        self.page_layout.size_hint_y = None
        self.page_layout.height = 200
        self.add_widget(self.page_layout)

        self.scroll = ScrollView(size_hint=(1, 0.8), scroll_distance=10,
                                 scroll_timeout=20)  # for height: deploy Window.height/2
        self.scroll.add_widget(self.sqlresults)
        self.add_widget(self.scroll)

        self.go_back = Button(text='Go Back', font_size=50, size_hint_y=0.5, font_name="Daytona")
        self.go_back.bind(on_release=self.goback)
        self.add_widget(self.go_back)

    def goback(self, instance):
        self.editing = False
        self.removing = False
        self.sqlresults.clear_widgets()
        self.member_search = []
        self.manager.transition.direction = "right"
        self.manager.current = "main"

    def editmember(self, instance):
        self.editing = not self.editing
        self.sqlresults.clear_widgets()
        self.find_member(instance=instance)

    def removemember(self, instance):
        self.removing = not self.removing
        self.sqlresults.clear_widgets()
        self.find_member(instance=instance)

    def update_rect(self, *args):
        self.rect.pos = self.center_x - 492, self.center_y - 700
        self.rect.size = self.width - 100, self.height + 2000

    def filter(self, instance):
        data = backend.MemberData()
        self.member_search = []
        self.members_indexa = []
        self.members_indexr = []

        attribute = self.detail.text

        self.detail.text = ''

        for ind, d in enumerate(data.accepted):
            if attribute.lower() == '':
                self.member_search.append(d)
                self.members_indexa.append(ind)
            elif attribute.lower() in d[0].lower() or attribute.lower() in d[1].lower() or attribute in d[2] or \
                    attribute.lower() in d[3].lower():
                self.member_search.append(d)
                self.members_indexa.append(ind)

        for ind, d in enumerate(data.rejected):
            if attribute.lower() == '':
                self.member_search.append(d)
                self.members_indexr.append(ind)
            elif attribute.lower() in d[0].lower() or attribute.lower() in d[1].lower() or attribute in d[2] or \
                    attribute.lower() in d[3].lower():
                self.member_search.append(d)
                self.members_indexr.append(ind)

        self.find_member(instance=instance)

    def find_member(self, instance):
        self.sqlresults.clear_widgets()
        self.results_obtained = False
        self.edit_list = []
        date = str(datetime.datetime.now())
        month = date[5:7]
        year = date[2:4]
        current_date = month + '/' + year

        if len(self.member_search) == 0:
            self.sqlresults.add_widget(Label(text="Not Registered"))
        else:
            self.result_rows = GridLayout(cols=4, spacing=20)
            self.result_rows.height = 80
            self.results_obtained = True
            titlesize = 52  # mobile 10
            textsize = 50  # mobile 8
            fontname = "Daytona"
            results_size = [50, 110]
            self.result_rows.add_widget(
                Label(text="Name", font_size=titlesize, font_name=fontname, size_hint_y=None, size=results_size))
            self.result_rows.add_widget(
                Label(text="Phone", font_size=titlesize, font_name=fontname, size_hint_y=None, size=results_size))
            self.result_rows.add_widget(
                Label(text="Membership", font_size=titlesize, font_name=fontname, size_hint_y=None, size=results_size))
            self.sqlresults.add_widget(self.result_rows)
            if self.editing:
                self.result_rows.add_widget(
                    Label(text="Save Details", font_size=titlesize, font_name=fontname, size_hint_y=None,
                          size=results_size))
            else:
                self.result_rows.add_widget(
                    Label(text="Payment", font_size=titlesize, font_name=fontname, size_hint_y=None, size=results_size))
            for m in self.member_search:
                self.result_rows = GridLayout(cols=4, spacing=20)
                if self.editing:
                    if m[6] is None:  # parse custom_pay text
                        temp_text = ''
                    else:
                        temp_text = str(m[6])
                    self.fname = TextInput(multiline=False, text=m[0], font_size=textsize, font_name=fontname,
                                           size_hint_y=None, size=(50, 75))
                    self.lname = TextInput(multiline=False, text=m[1], font_size=textsize, font_name=fontname,
                                           size_hint_y=None, size=(50, 75))
                    self.phone = TextInput(multiline=False, text=m[2], font_size=textsize-8, font_name=fontname,
                                           size_hint_y=None, size=results_size)
                    self.custom_pay = TextInput(multiline=False, text=temp_text, font_size=textsize, font_name=fontname,
                                                size_hint=(0.5, None), size=(10, results_size[1]))
                    self.membutton = Button(text=m[3], size_hint=(1, None), font_size=textsize-6, font_name=fontname,
                                            size=(40, results_size[1]))
                    self.membutton.bind(on_release=partial(self.mem_change, m))
                    self.edit_list.append([m[5], self.fname, self.lname, self.phone, self.custom_pay])
                    subframe = GridLayout(cols=2)
                    nameframe = GridLayout(cols=1)

                    nameframe.add_widget(self.fname)
                    nameframe.add_widget(self.lname)
                    self.result_rows.add_widget(nameframe)
                    self.result_rows.add_widget(self.phone)
                    subframe.add_widget(self.membutton)
                    subframe.add_widget(self.custom_pay)
                    self.result_rows.add_widget(subframe)
                    self.save_button = Button(text="Save", size_hint=(0.8, 1), font_size=textsize, font_name=fontname,
                                              size_hint_y=None, size=results_size)
                    self.save_button.bind(on_release=partial(self.edit_mem, m))
                    self.result_rows.add_widget(self.save_button)
                else:
                    if m[6] is None:  # parse custom_pay text
                        temp_text = ''
                    else:
                        temp_text = " - " + str(m[6])
                    self.names = GridLayout(cols=1, spacing=40, size_hint_y=None)
                    self.names.add_widget(
                        Label(text=m[0], font_size=textsize, font_name=fontname, size_hint_y=None, size=(100, 10)))
                    self.names.add_widget(
                        Label(text=m[1], font_size=textsize, font_name=fontname, size_hint_y=None, size=(100, 10)))
                    self.result_rows.add_widget(self.names)
                    self.result_rows.add_widget(
                        Label(text=m[2], font_size=textsize-8, font_name=fontname, size_hint_y=None, size=results_size))
                    self.result_rows.add_widget(
                        Label(text=m[3] + temp_text, font_size=textsize-6, font_name=fontname, size_hint_y=None,
                              size=results_size))
                    if self.removing:
                        self.memremove = Button(text="Delete", size_hint=(0.8, 1), font_size=textsize,
                                                font_name=fontname, size_hint_y=None, size=results_size)
                        self.memremove.bind(on_release=partial(self.mem_remove, m))
                        self.result_rows.add_widget(self.memremove)
                if not self.editing and not self.removing:
                    if m[4] == current_date or m[3] == "MMA Course" and m[4] > current_date:
                        self.payment = Button(text='Paid', font_size=textsize, font_name=fontname,
                                              background_color=(0, 1, 0, 1), size_hint_y=None, size=results_size)
                        self.payment.bind(on_release=partial(self.unpay_month, m))
                        self.result_rows.add_widget(self.payment)
                    else:
                        self.payment = Button(text='Not Paid', font_size=textsize, font_name=fontname,
                                              background_color=(1, 0, 0, 1), size_hint_y=None, size=results_size)
                        self.payment.bind(on_release=partial(self.pay_month, m))
                        self.result_rows.add_widget(self.payment)
                if self.results_obtained:
                    self.sqlresults.add_widget(self.result_rows)
            self.result_rows = GridLayout(cols=4, spacing=20)
            self.result_rows.add_widget(Label())
            self.sqlresults.add_widget(self.result_rows)

    def reset_search(self, instance):
        user_data = backend.MemberData()
        self.sqlresults.clear_widgets()
        self.member_search = []

        for i in self.members_indexa:
            self.member_search.append(user_data.accepted[i])

        for i in self.members_indexr:
            self.member_search.append(user_data.rejected[i])

        self.find_member(instance=instance)

    def edit_mem(self, instance, userdata):
        user_data = backend.MemberData()

        for e in self.edit_list:
            if e[0] == instance[5]:
                user_data.update_details(e[1].text, e[2].text, e[3].text, e[4].text, e[0])
                break

        user_data.getdata()
        self.reset_search(instance=instance)

    def mem_change(self, instance, userdata):
        user_data = backend.MemberData()
        options = ["Gym", "MMA Course", "kids class", "None"]
        index = 0
        for ind, op in enumerate(options):
            if op == instance[3]:
                index = ind
        if index == 3:
            index = 0
        else:
            index += 1

        user_data.update_membership(instance[0], instance[1], options[index])
        user_data.getdata()
        self.reset_search(instance=instance)

    def mem_remove(self, instance, userdata):
        data = backend.MemberData()
        data.remove_member(instance[0], instance[1])
        data.getdata()
        self.filter(instance=instance)

    def pay_month(self, instance, userdata):
        data = CurrentData()
        user_data = backend.MemberData()
        data.change_user(instance)
        if data.current_user[3] == "MMA Course":
            with open('settings.json') as json_file:
                settings = json.load(json_file)
            month = settings["Course_end"][0:2]
            year = settings["Course_end"][3:5]
        else:
            date = str(datetime.datetime.now())
            month = date[5:7]
            year = date[2:4]
        user_data.update_paid(data.current_user[0], data.current_user[1], month + '/' + year)
        user_data.getdata()
        self.members_indexa.append(len(self.members_indexa))
        self.members_indexr.pop(-1)
        self.reset_search(instance=instance)

    def unpay_month(self, instance, userdata):
        data = CurrentData()
        user_data = backend.MemberData()
        data.change_user(instance)
        date = str(datetime.datetime.now())
        month = int(date[5:7])
        year = int(date[2:4])
        new_date = str(add_months(datetime.date(year + 2000, month, 28), -1))
        user_data.update_paid(data.current_user[0], data.current_user[1], new_date[5:7] + '/' + new_date[2:4])
        user_data.getdata()
        self.members_indexr.append(len(self.members_indexr))
        self.members_indexa.pop(-1)
        self.reset_search(instance=instance)


class MyApp(App):
    def build(self):
        backend.initialisation()  # run on separate thread
        frontfile = Builder.load_file("front.kv")
        user_data = backend.MemberData()
        return frontfile


class SettingsPage(GridLayout, Screen, Widget):
    def __init__(self, **kwargs):
        super(SettingsPage, self).__init__(**kwargs)
        data = backend.MemberData()
        user = CurrentData()

        self.cols = 1

        self.page_layout = GridLayout(cols=3, spacing=5)

        self.cell = GridLayout(cols=1, spacing=5)

        self.cell.add_widget(Label(text="MMA", font_size=50, bold=True, font_name="Daytona"))
        self.cell.add_widget(Label(text="course", font_size=50, bold=True, font_name="Daytona"))
        self.cell.add_widget(Label(text="end:", font_size=50, bold=True, font_name="Daytona"))

        self.page_layout.add_widget(self.cell)

        self.dropdown_month = DropDown()

        for month in range(12):
            month += 1
            month_text = str(month)
            btn = Button(text=month_text, size_hint_y=None, height=50, width=100, font_name="Daytona")
            btn.bind(on_release=lambda btn: self.dropdown_month.select(btn.text))
            self.dropdown_month.add_widget(btn)

        self.month_set = Button(text='Month', size_hint=(0.8, 1), font_size=50, font_name="Daytona")
        self.month_set.bind(on_release=self.dropdown_month.open)
        self.dropdown_month.bind(on_select=lambda instance, x: setattr(self.month_set, 'text', x))
        self.page_layout.add_widget(self.month_set)

        self.dropdown_year = DropDown()

        for year in range(5):
            year += 22
            year_text = "20" + str(year)
            btn = Button(text=year_text, size_hint_y=None, height=50, width=100, font_name="Daytona")
            btn.bind(on_release=lambda btn: self.dropdown_year.select(btn.text))
            self.dropdown_year.add_widget(btn)

        self.year_set = Button(text='Year', size_hint=(0.8, 1), font_size=50, font_name="Daytona")
        self.year_set.bind(on_release=self.dropdown_year.open)
        self.dropdown_year.bind(on_select=lambda instance, x: setattr(self.year_set, 'text', x))
        self.page_layout.add_widget(self.year_set)

        self.submet = Button(text='Submit', font_size=70, font_name="Daytona", size_hint_y=None, height=200)
        self.submet.bind(on_release=self.change_settings)

        self.add_widget(self.page_layout)

        self.add_widget(self.submet)

        self.back = Button(text='Go Back', font_size=80, size_hint_y=0.6, font_name="Daytona")
        self.back.bind(on_release=self.goback)
        self.add_widget(self.back)

    def goback(self, instance):
        self.manager.transition.direction = "up"
        self.manager.current = "main"

    def change_settings(self, instance):
        month = self.month_set.text
        year = self.year_set.text[2:4]
        if len(str(month)) == 1:
            month = "0" + str(month)

        print(month)
        print(year)

        data = {
            "Course_end": month+"/"+year
        }

        with open('settings.json', 'w') as f:
            json.dump(data, f)


class WindowManager(ScreenManager):
    pass


def add_months(sourcedate, months):
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month // 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year, month)[1])
    return datetime.date(year, month, day)


MyApp().run()

# to do:

# current : gym_app8
# line 408 need to properly move the index from search indexa to indexr in pay_month
# on search page dont change aws rds until exit page for faster button presses

# adjust for mobile:
# search font size
# search scrollview height

# notes:
# tutorial: https://www.youtube.com/watch?v=bMHK6NDVlCM
# package for mobile: https://realpython.com/mobile-app-kivy-python/ or
# https://towardsdatascience.com/3-ways-to-convert-python-app-into-apk-77f4c9cd55af
# check https://kivy.org/doc/stable/api-kivy.core.text.html

# MMAadm1n
