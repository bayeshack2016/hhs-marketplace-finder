from app import app
from flask import render_template, request
from . import search
from wtforms import Form, IntegerField, SelectField, StringField, ValidationError
from wtforms.validators import DataRequired, Length, NumberRange, Optional

class InForm(Form):

    zip_code = StringField('Your zip code')

    age = IntegerField('How old are you?', validators=[Optional()])

    sex = SelectField('How do you identify?', choices=[('decline', 'decline to share'), ('female', 'female'), ('male', 'male'), ('trans', 'transgendered')], validators=[Optional()])

    smoking = SelectField('Have you smoked?', choices=[('decline', 'decline to share'), ('never did', 'never did'), ('used to', 'used to'), ('still do', 'still do')], validators=[Optional()])

    physical = SelectField('Do you have a physical condition that affects your everyday quality of life?', choices=[('decline', 'decline to share'), ('no', 'no'), ('yes', 'yes')], validators=[Optional()])

    mental = SelectField('Do you have a mental condition that affects your everyday quality of life?', choices=[('decline', 'decline to share'), ('no', 'no'), ('yes', 'yes')], validators=[Optional()])

    pregnant = SelectField('Are you pregnant, or planning on becoming pregnant?', choices=[('decline', 'decline to share'), ('no', 'no'), ('yes', 'yes')], validators=[Optional()])

    hospital = IntegerField('How many nights did you spend in a hospital last year?', validators=[Optional()])

    education = SelectField('What is the highest educational level you have obtained?', choices=[('decline', 'decline to share'), ('no diploma', 'no diploma'), ('high school or GED', 'high school or GED'), ('college', 'college'), ('postgraduate', 'postgraduate')], validators=[Optional()])

    income = SelectField('How much money did you make last year?', choices=[('decline', 'decline to share'), ('< $20,000', '< $20,000'), ('$20,000 < $45,000', '$20,000 < $45,000'), ('$45,000 < $75,000', '$45,000 < $75,000'), ('> $75,000', '> $75,000')], validators=[Optional()])

    doctor = StringField('If you have a doctor you like, enter their name here', validators=[Optional()])


@app.route('/', methods=['GET', 'POST'])
def index():
    form = InForm(request.form)
    if (request.method == 'POST') & form.validate():
        params = {}
        params['state'] = 'Arkansas'
        params['locals'] = search.get_locals(form.zip_code.data)
        if form.doctor.data:
            fname, lname = search.split_name(form.doctor.data)
            params['plans'] = search.get_plans(fname, lname)
        return render_template('index.html', form=form, **params)
    else:
        print(request.method)
        print(form.validate())
        return render_template('index.html', form=form)
