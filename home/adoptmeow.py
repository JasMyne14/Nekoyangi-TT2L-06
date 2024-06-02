from flask import Blueprint, request, redirect, url_for,flash, render_template
from .models import db, Cat
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename
from .registercat import upload_folder, allowed_extensions
import os

adoptmeow = Blueprint('adoptmeow',__name__)

@adoptmeow.route('/put_adopt_cat/<int:cat_id>', methods=['POST'])
@login_required
def put_adopt_cat(cat_id):
    cat = Cat.query.get_or_404(cat_id)

    if cat.user_id != current_user.id:
        flash('You do not have permission to put this cat up for adoption.', 'danger')
        return redirect(url_for('views.catprofile'))

    cat.available_for_adoption = True
    db.session.commit()

    flash(f'{cat.cat_name} has been put up for adoption!', 'success')
    return redirect(url_for('views.catprofile'))

@adoptmeow.route('/adopt_cat/<int:cat_id>', methods=['POST'])
@login_required
def adopt_cat(cat_id):
    cat = Cat.query.get_or_404(cat_id)

    if cat.user_id == current_user.id:
        flash('You cannot adopt your own cat.', 'danger')
        return redirect(url_for('adoptmeow.adoptmeow'))

    if not cat.available_for_adoption:
        flash('This cat is no longer available for adoption.', 'danger')
        return redirect(url_for('adoptmeow.adoptmeow'))

    cat.user_id = current_user.id # update cat ownership to current user
    cat.available_for_adoption = False
    db.session.commit()

    flash(f'Congratulations! You have adopted {cat.cat_name}.', 'success')
    return redirect(url_for('views.catprofile'))

@adoptmeow.route('/remove_adopt/<int:cat_id>', methods=['POST'])
@login_required
def remove_adopt_cat(cat_id):
    cat = Cat.query.get_or_404(cat_id)
    if cat.user_id == current_user.id:
        cat.available_for_adoption = False
        db.session.commit()
        flash(f'Your cat, {cat.cat_name}  has been removed from adoption.', 'success')
    else:
        flash('You can only remove your own cat from adoption.', 'danger')
    return redirect(url_for('views.catprofile'))
