"""
Admin routes for user and system management
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from functools import wraps
from app import db
from app.models.user import User
from app.models.scan import ScanHistory
from app.models.disease import DiseaseDatabase

admin_bp = Blueprint('admin', __name__)


def admin_required(f):
    """Decorator to require admin access"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('You do not have permission to access this page', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function


@admin_bp.route('/')
@login_required
@admin_required
def index():
    """Admin dashboard"""
    total_users = User.query.count()
    total_scans = ScanHistory.query.count()
    total_diseases = DiseaseDatabase.query.count()
    
    recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()
    recent_scans = ScanHistory.query.order_by(ScanHistory.timestamp.desc()).limit(10).all()
    
    return render_template(
        'admin/index.html',
        total_users=total_users,
        total_scans=total_scans,
        total_diseases=total_diseases,
        recent_users=recent_users,
        recent_scans=recent_scans
    )


@admin_bp.route('/users')
@login_required
@admin_required
def users():
    """Manage users"""
    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    users = User.query.order_by(User.created_at.desc())\
        .paginate(page=page, per_page=per_page, error_out=False)
    
    return render_template('admin/users.html', users=users)


@admin_bp.route('/users/delete/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    """Delete a user"""
    if user_id == current_user.id:
        flash('You cannot delete your own account', 'danger')
        return redirect(url_for('admin.users'))
    
    user = User.query.get_or_404(user_id)
    
    try:
        db.session.delete(user)
        db.session.commit()
        flash(f'User {user.username} deleted successfully', 'success')
    except Exception as e:
        db.session.rollback()
        flash('An error occurred while deleting the user', 'danger')
    
    return redirect(url_for('admin.users'))


@admin_bp.route('/users/toggle-admin/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def toggle_admin(user_id):
    """Toggle admin status for a user"""
    if user_id == current_user.id:
        flash('You cannot modify your own admin status', 'danger')
        return redirect(url_for('admin.users'))
    
    user = User.query.get_or_404(user_id)
    
    try:
        user.is_admin = not user.is_admin
        db.session.commit()
        
        status = 'granted' if user.is_admin else 'revoked'
        flash(f'Admin access {status} for {user.username}', 'success')
    except Exception as e:
        db.session.rollback()
        flash('An error occurred while updating user status', 'danger')
    
    return redirect(url_for('admin.users'))


@admin_bp.route('/scans')
@login_required
@admin_required
def scans():
    """View all scans"""
    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    scans = ScanHistory.query.order_by(ScanHistory.timestamp.desc())\
        .paginate(page=page, per_page=per_page, error_out=False)
    
    return render_template('admin/scans.html', scans=scans)


@admin_bp.route('/diseases')
@login_required
@admin_required
def diseases():
    """Manage disease database"""
    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    diseases = DiseaseDatabase.query.order_by(DiseaseDatabase.crop_name)\
        .paginate(page=page, per_page=per_page, error_out=False)
    
    return render_template('admin/diseases.html', diseases=diseases)
