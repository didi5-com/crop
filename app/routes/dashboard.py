"""
Dashboard routes for user statistics and overview
"""
from flask import Blueprint, render_template
from flask_login import login_required, current_user
from sqlalchemy import func
from app import db
from app.models.scan import ScanHistory

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/')
@login_required
def index():
    """Main dashboard page"""
    # Get user statistics
    total_scans = ScanHistory.query.filter_by(user_id=current_user.id).count()
    
    # Get recent scans
    recent_scans = ScanHistory.query.filter_by(user_id=current_user.id)\
        .order_by(ScanHistory.timestamp.desc())\
        .limit(5)\
        .all()
    
    # Get most detected diseases
    disease_stats = db.session.query(
        ScanHistory.disease_name,
        func.count(ScanHistory.id).label('count')
    ).filter_by(user_id=current_user.id)\
     .group_by(ScanHistory.disease_name)\
     .order_by(func.count(ScanHistory.id).desc())\
     .limit(5)\
     .all()
    
    # Get crop statistics
    crop_stats = db.session.query(
        ScanHistory.crop_name,
        func.count(ScanHistory.id).label('count')
    ).filter_by(user_id=current_user.id)\
     .group_by(ScanHistory.crop_name)\
     .order_by(func.count(ScanHistory.id).desc())\
     .limit(5)\
     .all()
    
    return render_template(
        'dashboard/index.html',
        total_scans=total_scans,
        recent_scans=recent_scans,
        disease_stats=disease_stats,
        crop_stats=crop_stats
    )
