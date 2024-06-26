from flask import Blueprint, request, redirect, url_for,flash, render_template
from .models import db, Cat, AdoptionNotification, User
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename
from .registercat import upload_folder, allowed_extensions
import os
from datetime import datetime

adoptmeow = Blueprint('adoptmeow',__name__)

#Define route to put cat for adopt
@adoptmeow.route('/put_adopt_cat/<int:cat_id>', methods=['POST'])
@login_required
def put_adopt_cat(cat_id):
    #retrive the cat by ID or return a 404 error if not found
    cat = Cat.query.get_or_404(cat_id)

    #check if current user is the owner of the cat
    if cat.user_id != current_user.id:
        flash('You do not have permission to put this cat up for adoption.', 'danger')
        return redirect(url_for('views.catprofile'))

    #update the cat's status to be available for adoption
    cat.date_put_for_adoption = datetime.utcnow()      #set current time
    cat.available_for_adoption = True                  #set adopt status to True
    db.session.commit()

    flash(f'{cat.cat_name} has been put up for adoption!', 'success')
    return redirect(url_for('views.catprofile'))

#Define route to adopt cat
@adoptmeow.route('/adopt_cat/<int:cat_id>', methods=['POST'])
@login_required
def adopt_cat(cat_id):
    cat = Cat.query.get_or_404(cat_id)

    #check if  current user is trying to adopt their own cat
    if cat.user_id == current_user.id:
        flash('You cannot adopt your own cat.', 'danger')
        return redirect(url_for('views.adoptmeow'))

    #check if cat is still av for adopt
    if not cat.available_for_adoption:
        flash('This cat is no longer available for adoption.', 'danger')
        return redirect(url_for('views.adoptmeow'))
    
    #noti for adopt
    notification = AdoptionNotification(cat_id=cat_id, user_id=cat.user_id, adopter_id=current_user.id, notification_type='adoption')
    db.session.add(notification)
    db.session.commit()

    owner = User.query.get(cat.user_id)
    owner.unread_notification_count +=1

    #update new cat owner and status
    cat.user_id = current_user.id                       # update cat ownership to current user
    cat.available_for_adoption = False                  #set to false
    cat.date_put_for_adoption = None                    #clear date for adopt

    db.session.commit()
    flash(f'Congratulations! You have adopted {cat.cat_name}.', 'success')
    return redirect(url_for('views.catprofile'))

#define route to remove cat from adopt
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
