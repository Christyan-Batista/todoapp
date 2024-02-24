import flet as ft


class Task:
    def __init__(self, name_task, funcdeletetask, updatescreen, updatechangecheckbox):
        self.name = name_task
        self.updatescreen = updatescreen
        self.funcdeletetask = funcdeletetask
        self.updatechangecheckbox = updatechangecheckbox
        self.task = ft.Checkbox(label=self.name, on_change=self.updatechangedcheckbox)
        self.delbutton = ft.IconButton(ft.icons.DELETE_OUTLINE, tooltip='Deletar', on_click=self.deletetask)
        self.editbutton = ft.IconButton(ft.icons.EDIT, tooltip='Editar', on_click=self.edittask)
        self.rowbuttons = ft.Row(controls=[self.editbutton, self.delbutton])
        self.editview = ft.Row(controls=[
                                            ft.TextField(label=str(self.name), expand=1),
                                            ft.IconButton(ft.icons.DONE_OUTLINE_OUTLINED, tooltip='Salvar', on_click=self.save_editchange)
                                        ],
                                visible=False, alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                vertical_alignment=ft.CrossAxisAlignment.CENTER)
        self.view = ft.Row(controls=[self.task, self.rowbuttons], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        self.linha = ft.Column(controls=[self.view,
                                         self.editview])

    def deletetask(self, e):
        self.funcdeletetask(self.linha)

    def edittask(self, e):
        self.editview.visible = True
        self.view.visible = False
        self.updatescreen()
        return

    def save_editchange(self, e):
        self.task.label = str(self.editview.controls[0].value)
        self.editview.visible = False
        self.view.visible = True
        self.updatescreen()
        return

    def updatechangedcheckbox(self, e):
        self.updatechangecheckbox(e)


class App:
    def __init__(self):
        ft.app(target=self.main)

    def main(self, page: ft.Page):
        page.horizontal_alignment = 'center'
        page.title = 'Tarefas'
        page.window_width = 700
        page.window_height = 500
        page.window_resizable = False
        self.page = page
        self.row = self.input_tasks()
        self.taskscolumn = ft.Column()

        self.filter = ft.Tabs(
            selected_index=0, on_change= self.changetabs,
            tabs=[ft.Tab(text="Todas"), ft.Tab(text="Ativas"), ft.Tab(text="Completas")])

        page.add(ft.Column([self.row, ft.Column([self.filter, self.taskscolumn])], width=600))
        self.loadtasksstoraged(page)
        return

    def input_tasks(self):
        self.textfield = ft.TextField(label='Tarefas', value='Insira uma tarefa', on_focus=self.input_task_focus,
                                      on_blur=self.input_task_blur, expand=1)
        self.addbutton = ft.ElevatedButton('Add', icon='add', on_click=self.addnewtask)
        return ft.Row(controls=[
                         self.textfield,
                         self.addbutton],
                      alignment=ft.MainAxisAlignment.CENTER)

    def input_task_focus(self, e):
        if self.textfield.value == 'Insira uma tarefa':
            self.textfield.value = ''
            self.row.update()

    def input_task_blur(self, e):
        if self.textfield.value == '':
            self.textfield.value = 'Insira uma tarefa'
            self.row.update()

    def addnewtask(self, e):
        tasktext = str(self.textfield.value)
        tsk = Task(tasktext, self.deltask, self.update, self.changetabs)
        self.storagetasks(self.page, tasktext)
        self.taskscolumn.controls.append(tsk.linha)
        self.textfield.value = ''
        self.row.update()
        self.taskscolumn.update()
        return

    def deltask(self, task):
        self.taskscolumn.controls.remove(task)
        self.taskscolumn.update()

        taskstocompare = []
        for rows in self.taskscolumn.controls:
            for txt in rows.controls:
                try:
                    taskstocompare.append(str(txt.label))
                except:
                    continue

        self.page.client_storage.set('tasks', taskstocompare)

    def loadtasksstoraged(self, pag: ft.Page):
        if pag.client_storage.contains_key('tasks'):

            for task in pag.client_storage.get('tasks'):
                newtask = Task(str(task), self.deltask, self.update, self.changetabs)
                self.taskscolumn.controls.append(newtask.linha)

            self.taskscolumn.update()
            return
        else:
            pag.client_storage.set('tasks', [])
            return None

    def storagetasks(self, pg: ft.Page, taskname):
        storaged = pg.client_storage.get('tasks')
        storaged.append(taskname)
        pg.client_storage.set('tasks', storaged)
        return

    def changetabs(self, e):
        status = self.filter.tabs[self.filter.selected_index].text
        for task in self.taskscolumn.controls:
            task.visible = (status == 'Todas' or (status == 'Ativas' and not task.controls[0].controls[0].value) or (status == 'Completas' and task.controls[0].controls[0].value))
        self.taskscolumn.update()

    def update(self):
        self.taskscolumn.update()



App()
