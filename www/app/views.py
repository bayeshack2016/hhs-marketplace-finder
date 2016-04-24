from app import app
from flask import render_template, request
from . import search
from wtforms import Form, IntegerField, SelectField, StringField, ValidationError
from wtforms.validators import DataRequired, Length, NumberRange, Optional

class InForm(Form):

    zip_code = StringField('Your zip code', validators=[DataRequired()])

    def validate_zip_code(form, field):
        try:
            int(field.data)
        except:
            raise ValidationError("Not a valid zip code")

    age = IntegerField('Your age', validators=[Optional()])
    sex = SelectField('Your gender', choices=[('decline', 'decline to share'), ('female', 'female'), ('male', 'male'), ('trans', 'transgendered')], validators=[Optional()])
    smoking = SelectField('Your smoking', choices=[('decline', 'decline to share'), ('never did', 'never did'), ('used to', 'used to'), ('still do', 'still do')], validators=[Optional()])
    doctor = StringField('Your doctor', validators=[Optional()])


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
