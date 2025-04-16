import pronotepy.ent
import pronotepy
import json

class PronoteScript:
    def __init__(self, username, password, pronote_link, ent_choice, settings_script):
        self.username = username
        self.password = password
        self.pronote_link = pronote_link
        self.ent_choice = ent_choice
        ent_func = getattr(pronotepy.ent, self.ent_choice, None)

        self.settings_script = settings_script

        try:
            self.client = pronotepy.Client(
                self.pronote_link,
                self.username,
                self.password,
                ent_func
            )
        except Exception as e:
            print("Login failed :", e)
            self.settings_script.reset_account()

        self.client_notes = None
        self.client.info.profile_picture.save('src/assets/img/profile_picture.png')
        self.save_pronote_json()

    def save_pronote_json(self):
        data = {}
        data['client_info'] = {
            'name': self.client.info.name,
            'class': self.client.info.class_name,
            'school': self.client.info.establishment,
        }
        data['periods'] = []
        
        # Variables globales pour le calcul de la moyenne générale sur les 3 premiers trimestres
        global_total_points = 0
        global_total_coef = 0

        for idx, period in enumerate(self.client.periods):
            period_data = {}
            period_data['name'] = period.name
            period_data['grades'] = []
            subject_totals = {}

            total_points = 0
            total_coef = 0
            optionals_to_evaluate = []

            for grade in period.grades:
                try:
                    comment = grade.comment
                    note = float(grade.grade.replace(',', '.'))
                    out_of = float(grade.out_of.replace(',', '.'))
                    coef = float(grade.coefficient)
                except Exception:
                    continue
                value = note * 20 / out_of

                grade_data = {
                    'comment': comment,
                    'subject': grade.subject.name if grade.subject else None,
                    'grade': note,
                    'out_of': out_of,
                    'coefficient': coef,
                    'value': value,
                    'date': grade.date.strftime("%d/%m/%Y") if hasattr(grade, 'date') else "",
                    'optional': grade.is_optionnal
                }
                period_data['grades'].append(grade_data)

                subject_name = grade.subject.name if grade.subject else "Inconnu"
                if subject_name not in subject_totals:
                    subject_totals[subject_name] = {'points': 0, 'coef': 0, 'optionals': []}

                if grade.is_optionnal:
                    # Stockage pour évaluation différée
                    optionals_to_evaluate.append((value, coef))
                    subject_totals[subject_name]['optionals'].append((value, coef))
                else:
                    total_points += value * coef
                    total_coef += coef
                    subject_totals[subject_name]['points'] += value * coef
                    subject_totals[subject_name]['coef'] += coef

            # Évaluation des notes optionnelles pour la moyenne de la période
            current_average = total_points / total_coef if total_coef else 0
            for value, coef in optionals_to_evaluate:
                potential_total_points = total_points + value * coef
                potential_total_coef = total_coef + coef
                new_average = potential_total_points / potential_total_coef
                if new_average > current_average:
                    total_points = potential_total_points
                    total_coef = potential_total_coef
                    current_average = new_average

            average = total_points / total_coef if total_coef else None
            period_data['average'] = average

            # Si la période fait partie des 3 premiers trimestres, on l'inclut dans le calcul global
            if idx < 3:
                global_total_points += total_points
                global_total_coef += total_coef

            # Calcul de la moyenne par matière en prenant en compte les optionnelles
            subject_averages = {}
            for subject, totals in subject_totals.items():
                points = totals['points']
                coef = totals['coef']
                current_subject_avg = points / coef if coef else 0

                for val, c in totals['optionals']:
                    potential_points = points + val * c
                    potential_coef = coef + c
                    new_avg = potential_points / potential_coef
                    if new_avg > current_subject_avg:
                        points = potential_points
                        coef = potential_coef
                        current_subject_avg = new_avg

                subject_averages[subject] = current_subject_avg if coef else None

            period_data['subjects'] = subject_averages
            data['periods'].append(period_data)

        # Calcul de la moyenne générale en intégrant toutes les notes des 3 premiers trimestres
        if global_total_coef:
            overall_average = global_total_points / global_total_coef
        else:
            overall_average = None
        data['overall_average'] = overall_average

        self.client_notes = data

        with open('src/assets/json/pronote_data.json', 'w') as file:
            json.dump(data, file, indent=4)

