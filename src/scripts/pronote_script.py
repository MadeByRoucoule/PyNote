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
        except:
            print("Login failed")
            self.settings_script.reset_account()

        self.client_notes = None
        self.client.info.profile_picture.save('src/assets/img/profile_picture.png')
        self.save_pronote_json()

    def save_pronote_json(self):
        data = {}
        data['client_info'] = {
            'name': self.client.info.name
        }
        data['periods'] = []
        period_averages = []
        for period in self.client.periods:
            period_data = {}
            period_data['name'] = period.name
            period_data['grades'] = []
            total_points = 0
            total_coef = 0
            for grade in period.grades:
                try:
                    note = float(grade.grade.replace(',', '.'))
                    out_of = float(grade.out_of.replace(',', '.'))
                    coef = float(grade.coefficient)
                except Exception:
                    continue
                value = note * 20 / out_of
                grade_data = {
                    'subject': grade.subject.name if grade.subject else None,
                    'grade': note,
                    'out_of': out_of,
                    'coefficient': coef,
                    'value': value,
                    'date': grade.date.strftime("%d/%m/%Y") if hasattr(grade, 'date') else ""
                }
                period_data['grades'].append(grade_data)
                total_points += value * coef
                total_coef += coef
            if total_coef:
                average = total_points / total_coef
            else:
                average = None
            period_data['average'] = average
            period_averages.append(average)
            data['periods'].append(period_data)
        valid_averages = [a for a in period_averages if a is not None]
        if valid_averages:
            overall_average = sum(valid_averages) / len(valid_averages)
        else:
            overall_average = None
        data['overall_average'] = overall_average

        self.client_notes = data

        with open('src/assets/json/pronote_data.json', 'w') as file:
            json.dump(data, file, indent=4)