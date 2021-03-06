from authomatic.adapters import WerkzeugAdapter
from flask import flash, make_response, redirect, render_template, request, session, url_for
from flask.ext.login import login_required, login_user, logout_user

from app import app, authomatic, db, login_manager
from .forms import MyForm, WanderingForm
from .models import User, HotDeal


# =========================================================================
# Flask-Login
# =========================================================================

@login_manager.user_loader
def load_user(id):
    user = User.query.filter_by(id=id).first()
    return user


@login_manager.unauthorized_handler
def unauthorized():
    flash('You need to log in first.', 'warning')
    session['next_url'] = request.url
    return redirect(url_for('login', next=request.url))

# =========================================================================
# Authomatic
# =========================================================================

@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/login/<provider_name>', methods=('GET', 'POST'))
def social_login(provider_name):
    response = make_response()
    result = authomatic.login(WerkzeugAdapter(request, response), provider_name)
    if result:
        if result.user:
            result.user.update()
            social_id = '{}_{}'.format(result.provider.name, result.user.id)
            user = User.query.filter_by(social_id=social_id).first()
            if user is None:
                # fix oauth inconsistencies
                if result.provider.name == 'facebook':
                    result.user.picture = result.user.picture.replace('None', result.user.id)
                    result.user.first_name = result.user.name.split(' ')[0]
                    try:
                        result.user.last_name = result.user.name.split(' ')[1]
                    except:
                        result.user.last_name = ''
                elif result.provider.name == 'twitter':
                    result.user.first_name = result.user.name.split(' ')[0]
                    try:
                        result.user.last_name = result.user.name.split(' ')[1]
                    except:
                        result.user.last_name = ''
                user = User(
                    first_name=result.user.first_name,
                    last_name=result.user.last_name,
                    email=result.user.email,
                    picture_url=result.user.picture,
                    social_id=social_id,
                    social_profile_url=result.user.link,
                )
                db.session.add(user)
                db.session.commit()
            login_user(user, remember=True)
        elif result.error:
            flash(result.error.message, 'danger')
            return redirect(url_for('login'))
        return redirect(session.pop('next_url', url_for('index')))
    return response


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

# =========================================================================
# App pages
# =========================================================================

@app.route('/', methods=('GET', 'POST'))
def index():
    wandering_form = WanderingForm()
    if wandering_form.validate_on_submit():
        hot_deals = HotDeal.query.filter(HotDeal.ranking < int(wandering_form.budget_available.data) * int(wandering_form.person_number.data)).order_by(HotDeal.ranking.desc()).all()
        if hot_deals == []:
            flash('There are no deals for the given data, please try again later.', 'danger')
        return render_template('index.html', hot_deals=hot_deals, wandering_form=wandering_form, persons=int(wandering_form.person_number.data))
    return render_template('index.html', wandering_form=wandering_form)


# @app.route('/secret')
# @login_required
# def secret():
#     return render_template('secret.html')

# =========================================================================
# Error pages
# =========================================================================

@app.errorhandler(404)
def error_404(error):
    return (render_template('404.html'), 404)


@app.errorhandler(500)
def error_500(error):
    return (render_template('500.html'), 500)
