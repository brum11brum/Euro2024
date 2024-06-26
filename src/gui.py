import tkinter as tk
import ttkbootstrap as ttk
from tkinter.scrolledtext import ScrolledText

from src import connector


class App:
    def __init__(self):
        self.root = ttk.Window(themename='superhero')
        self.root.geometry('1200x800')
        self.root.title('Am I THAT good')
        self.root.iconbitmap('gronkjer_profile.ico')

        self.guys_list = [
            'Both',
            'Gronkjer',
            'El Comentarista'
        ]
        self.name = tk.StringVar(value=self.guys_list[0])
        self.stage = [1, 2, 3, 4, 5, 6, 7]
        self.stage1 = tk.BooleanVar(value=True)
        self.stage2 = tk.BooleanVar(value=True)
        self.stage3 = tk.BooleanVar(value=True)
        self.stage4 = tk.BooleanVar(value=True)
        self.stage5 = tk.BooleanVar(value=True)
        self.stage6 = tk.BooleanVar(value=True)
        self.stage7 = tk.BooleanVar(value=True)

        self.missingi = []
        self.percentage = ttk.StringVar(value='0%')

        self.home_stats_var = tk.StringVar(value='0/0')
        self.away_stats_var = tk.StringVar(value='0/0')
        self.draws_stats_var = tk.StringVar(value='0/0')
        self.exact_results_stats_var = tk.StringVar(value='0/0')

        self.choosing_frame = ttk.Frame(self.root)
        self.name_box = ttk.Combobox(self.choosing_frame, values=self.guys_list, textvariable=self.name)
        self.name_box.pack(side='left')
        self.name_box.bind('<<ComboboxSelected>>', self.refresh_results)
        self.stages_frame = ttk.Frame(self.choosing_frame)
        ttk.Label(self.stages_frame, text='Faza:').pack(side='left')
        self.stage1_check = ttk.Checkbutton(
            self.stages_frame, text='1', variable=self.stage1, onvalue=True, offvalue=False,
            command=self.refresh_results)
        self.stage2_check = ttk.Checkbutton(
            self.stages_frame, text='2', variable=self.stage2, onvalue=True, offvalue=False,
            command=self.refresh_results)
        self.stage3_check = ttk.Checkbutton(
            self.stages_frame, text='3', variable=self.stage3, onvalue=True, offvalue=False,
            command=self.refresh_results)
        self.stage4_check = ttk.Checkbutton(
            self.stages_frame, text='4', variable=self.stage4, onvalue=True, offvalue=False,
            command=self.refresh_results)
        self.stage5_check = ttk.Checkbutton(
            self.stages_frame, text='5', variable=self.stage5, onvalue=True, offvalue=False,
            command=self.refresh_results)
        self.stage6_check = ttk.Checkbutton(
            self.stages_frame, text='6', variable=self.stage6, onvalue=True, offvalue=False,
            command=self.refresh_results)
        self.stage7_check = ttk.Checkbutton(
            self.stages_frame, text='7', variable=self.stage7, onvalue=True, offvalue=False,
            command=self.refresh_results)

        self.stage1_check.pack(side='left', padx=10)
        self.stage2_check.pack(side='left', padx=10)
        self.stage3_check.pack(side='left', padx=10)
        self.stage4_check.pack(side='left', padx=10)
        self.stage5_check.pack(side='left', padx=10)
        self.stage6_check.pack(side='left', padx=10)
        self.stage7_check.pack(side='left', padx=10)

        self.stages_frame.pack(side='left', padx=80)

        self.add_prediction_button = ttk.Button(
            self.choosing_frame, text='Dodaj typ', command=self.add_new_prediction)
        self.add_prediction_button.pack(side='left', padx=10)
        self.add_prediction_button = ttk.Button(
            self.choosing_frame, text='Dodaj mecz', command=self.add_new_game)
        self.add_prediction_button.pack(side='left', padx=10)

        self.choosing_frame.pack(pady=20, padx=20)

        self.missing_frame = ttk.Frame(self.root)
        self.missing_display = ttk.Treeview(self.missing_frame, columns=['game', 'date'], show='headings', height=5)
        self.missing_display.heading('game', text='game')
        self.missing_display.heading('date', text='date')
        self.missing_display.pack(side='left')
        self.missing_buttons = ttk.Frame(self.missing_frame)
        ttk.Button(self.missing_buttons, text='dodaj wynik', command=self.add_results).pack(pady=10)
        ttk.Button(self.missing_buttons, text='odśwież', command=self.refresh_missing).pack(pady=10)
        self.missing_buttons.pack(side='left', padx=40)
        self.missing_frame.pack()

        self.bottom_frame = ttk.Frame(self.root)
        self.left_results = ttk.Frame(self.bottom_frame)
        self.predictions_display = ttk.Treeview(self.left_results, columns=['game', 'predicted', 'actual', 'hit'], show='headings', height=40)
        self.predictions_display.heading('game', text='game')
        self.predictions_display.heading('predicted', text='predicted')
        self.predictions_display.heading('actual', text='actual')
        self.predictions_display.heading('hit', text='hit')
        self.predictions_display.pack(side='left')
        self.left_results.pack(side='left', expand=True, fill='both')
        self.right_results = ttk.Frame(self.bottom_frame)
        ttk.Label(
            self.right_results,
            textvariable=self.percentage,
            font=('Ariel', 48)
        ).pack(ipady=150, ipadx=150, expand=True, fill='both')
        self.additional_stats_frame = ttk.Frame(self.right_results)
        self.home_stats = ttk.Frame(self.additional_stats_frame)
        ttk.Label(self.home_stats, text="home: ").pack(side='left')
        ttk.Label(self.home_stats, textvariable=self.home_stats_var).pack(side='left')
        self.home_stats.pack()
        self.away_stats = ttk.Frame(self.additional_stats_frame)
        ttk.Label(self.away_stats, text="away: ").pack(side='left')
        ttk.Label(self.away_stats, textvariable=self.away_stats_var).pack(side='left')
        self.away_stats.pack()
        self.draws_stats = ttk.Frame(self.additional_stats_frame)
        ttk.Label(self.draws_stats, text="draws: ").pack(side='left')
        ttk.Label(self.draws_stats, textvariable=self.draws_stats_var).pack(side='left')
        self.draws_stats.pack()
        self.exact_results_stats = ttk.Frame(self.additional_stats_frame)
        ttk.Label(self.exact_results_stats, text="exact: ").pack(side='left')
        ttk.Label(self.exact_results_stats, textvariable=self.exact_results_stats_var).pack(side='left')
        self.exact_results_stats.pack()
        self.additional_stats_frame.pack()
        self.right_results.pack(side='left', expand=True, fill='both')
        self.bottom_frame.pack(expand=True, fill='both', padx=40, pady=40)

        self.refresh_missing()
        self.refresh_results()

    def refresh_missing(self):
        self.missingi = connector.check_missing()
        self.missing_display.delete(*self.missing_display.get_children())
        for item in self.missingi:
            record = f'{item[1]}-{item[2]}', item[3]
            self.missing_display.insert('', tk.END, values=record)

    def get_table_predictions(self, results: list[tuple]):
        self.predictions_display.delete(*self.predictions_display.get_children())
        for item in results:
            self.predictions_display.insert('', tk.END, values=item)

    def set_additional_stats(self, additional_stats: dict) -> None:
        home_res = f"{additional_stats['hits']['home']}/{additional_stats['miss']['home']}"
        away_res = f"{additional_stats['hits']['away']}/{additional_stats['miss']['away']}"
        draws_res = f"{additional_stats['hits']['draw']}/{additional_stats['miss']['draw']}"
        exact_results_res = f"{additional_stats['hits']['exact_result']}/{additional_stats['miss']['exact_result']}"
        self.home_stats_var.set(home_res)
        self.away_stats_var.set(away_res)
        self.draws_stats_var.set(draws_res)
        self.exact_results_stats_var.set(exact_results_res)

    def refresh_results(self, event=None):
        name = self.name.get()
        stage = []
        if self.stage1.get():
            stage.append('1')
        if self.stage2.get():
            stage.append('2')
        if self.stage3.get():
            stage.append('3')
        if self.stage4.get():
            stage.append('4')
        if self.stage5.get():
            stage.append('5')
        if self.stage6.get():
            stage.append('6')
        if self.stage7.get():
            stage.append('7')
        results, additional_stats = connector.show_results(name, stage)
        self.set_additional_stats(additional_stats)
        count_hits: int = (additional_stats['hits']['home'] +
                           additional_stats['hits']['away'] +
                           additional_stats['hits']['draw'])
        self.get_table_predictions(results)

        if results:
            percentage = f"{(count_hits/len(results))*100:.2f}%"
            self.percentage.set(percentage)

    def add_results(self):
        miss_ind = self.missing_display.selection()[0]
        values = self.missing_display.item(miss_ind)['values'][0].split('-')
        home, away = values
        UpdateResults(self.root, home, away)
        self.refresh_missing()

    def add_new_prediction(self):
        NewPrediction(self.root)

    def add_new_game(self):
        AddGame(self.root)

    def run(self):
        self.root.mainloop()


class NewPrediction(ttk.Toplevel):
    def __init__(self, root):
        self.root = root
        super().__init__(self.root)
        self.teams = connector.fetch_teams()
        self.home_team = tk.StringVar(value=self.teams[0])
        self.away_team = tk.StringVar(value=self.teams[1])
        self.date = tk.StringVar(value='2024-06-23')
        self.guys = ['Gronkjer', 'El Comentarista']
        self.better = tk.StringVar(value=self.guys[0])
        self.errors = tk.StringVar(value='')

        self.teams_frame = ttk.Frame(self)
        ttk.Combobox(self.teams_frame, values=self.teams, textvariable=self.home_team).pack(side='left', padx=40)
        ttk.Combobox(self.teams_frame, values=self.teams, textvariable=self.away_team).pack(side='left', padx=40)
        self.teams_frame.pack()
        self.results_frame = ttk.Frame(self)
        self.home_goals = ttk.Spinbox(self.results_frame, from_=0, to=40)
        self.home_goals.pack(side='left', padx=40)
        self.home_goals.set(0)
        self.away_goals = ttk.Spinbox(self.results_frame, from_=0, to=40)
        self.away_goals.pack(side='left', padx=40)
        self.away_goals.set(0)
        self.results_frame.pack()
        self.rest_frame = ttk.Frame(self)
        self.date_given = ttk.DateEntry(self.rest_frame, dateformat=r"%y-%m-%d")
        self.date_given.pack(side='left')
        ttk.Label(self.rest_frame, text="faza:").pack(side='left')
        self.stage = ttk.Spinbox(self.rest_frame, from_=1, to=7)
        self.stage.pack(side='left')
        self.stage.set(1)
        self.whoisresponsible = ttk.Combobox(self.rest_frame, values=self.guys, textvariable=self.better)
        self.whoisresponsible.pack()
        self.rest_frame.pack()
        ttk.Button(self, text='DODAJ DO BAZY', command=self.add_record).pack(side='left')
        ttk.Label(self, textvariable=self.errors).pack()

    def add_record(self):
        date = '20' + self.date_given.entry.get()
        home = self.home_goals.get()
        away = self.away_goals.get()
        home_team = self.home_team.get()
        away_team = self.away_team.get()
        stage_str = self.stage.get()
        try:
            stage = int(stage_str)
        except ValueError:
            self.errors.set('Coś nie tak z fazą')
            return
        who = self.better.get()
        checker = connector.new_predicition(
            who, home, away, home_team, away_team, stage, date
        )
        if checker:
            self.errors.set(checker)


class AddGame(ttk.Toplevel):
    def __init__(self, root):
        self.root = root
        super().__init__(self.root)
        self.teams = connector.fetch_teams()
        self.home_team = tk.StringVar(value=self.teams[0])
        self.away_team = tk.StringVar(value=self.teams[1])
        self.date = tk.StringVar(value='2024-06-23')
        self.errors = tk.StringVar(value='')

        self.teams_frame = ttk.Frame(self)
        ttk.Combobox(self.teams_frame, values=self.teams, textvariable=self.home_team).pack(side='left', padx=40)
        ttk.Combobox(self.teams_frame, values=self.teams, textvariable=self.away_team).pack(side='left', padx=40)
        self.teams_frame.pack()
        self.rest_frame = ttk.Frame(self)
        self.date_given = ttk.DateEntry(self.rest_frame, dateformat=r"%y-%m-%d")
        self.date_given.pack(side='left')
        ttk.Button(self.teams_frame, text='DODAJ DO BAZY', command=self.add_record).pack(side='left')
        self.rest_frame.pack()
        ttk.Label(self, textvariable=self.errors).pack()

    def add_record(self):
        date = '20' + self.date_given.entry.get()
        home_team = self.home_team.get()
        away_team = self.away_team.get()
        checker = connector.add_new_game_to_db(home_team, away_team, date)
        if checker:
            self.errors.set(checker)
        else:
            self.errors.set(f"added {home_team}-{away_team} to database")


class UpdateResults(ttk.Toplevel):
    def __init__(
            self,
            root,
            home_team,
            away_team
    ):
        self.root = root
        super().__init__(self.root)

        self.home_team = home_team
        self.away_team = away_team

        self.home_frame = ttk.Frame(self)
        ttk.Label(self.home_frame, text=home_team).pack(side='left')
        self.home_goals = ttk.Spinbox(self.home_frame, from_=0, to=40)
        self.home_goals.pack(side='left', padx=40)
        self.home_frame.pack(pady=10)
        self.home_goals.set(0)

        self.away_frame = ttk.Frame(self)
        ttk.Label(self.away_frame, text=away_team).pack(side='left')
        self.away_goals = ttk.Spinbox(self.away_frame, from_=0, to=40)
        self.away_goals.pack(side='left', padx=40)
        self.away_frame.pack(pady=10)
        self.away_goals.set(0)

        ttk.Button(self, text='aktualizuj', command=self.update_record).pack(pady=20)

    def update_record(self):
        connector.update_old_game(self.home_team, self.away_team, self.home_goals.get(), self.away_goals.get())
        self.destroy()
