"""
REST API routes for mobile/external integrations
"""
from flask import Blueprint, jsonify, request, current_app
from flask_login import login_required, current_user
from app.models.scan import ScanHistory
from app.models.disease import DiseaseDatabase

api_bp = Blueprint('api', __name__)


@api_bp.route('/scans', methods=['GET'])
@login_required
def get_scans():
    """Get user's scan history as JSON"""
    try:
        scans = ScanHistory.query.filter_by(user_id=current_user.id)\
            .order_by(ScanHistory.timestamp.desc())\
            .all()
        
        return jsonify({
            'success': True,
            'count': len(scans),
            'scans': [scan.to_dict() for scan in scans]
        })
    
    except Exception as e:
        current_app.logger.error(f"API error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to retrieve scans'
        }), 500


@api_bp.route('/scans/<int:scan_id>', methods=['GET'])
@login_required
def get_scan(scan_id):
    """Get specific scan details"""
    try:
        scan = ScanHistory.query.get_or_404(scan_id)
        
        # Check permission
        if scan.user_id != current_user.id and not current_user.is_admin:
            return jsonify({
                'success': False,
                'error': 'Permission denied'
            }), 403
        
        return jsonify({
            'success': True,
            'scan': scan.to_dict()
        })
    
    except Exception as e:
        current_app.logger.error(f"API error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to retrieve scan'
        }), 500


@api_bp.route('/diseases', methods=['GET'])
def get_diseases():
    """Get disease database information"""
    try:
        crop = request.args.get('crop')
        disease = request.args.get('disease')
        
        query = DiseaseDatabase.query
        
        if crop:
            query = query.filter_by(crop_name=crop)
        
        if disease:
            query = query.filter_by(disease_name=disease)
        
        diseases = query.all()
        
        return jsonify({
            'success': True,
            'count': len(diseases),
            'diseases': [d.to_dict() for d in diseases]
        })
    
    except Exception as e:
        current_app.logger.error(f"API error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to retrieve diseases'
        }), 500


@api_bp.route('/stats', methods=['GET'])
@login_required
def get_stats():
    """Get user statistics"""
    try:
        total_scans = ScanHistory.query.filter_by(user_id=current_user.id).count()
        
        return jsonify({
            'success': True,
            'stats': {
                'total_scans': total_scans,
                'username': current_user.username,
                'email': current_user.email
            }
        })
    
    except Exception as e:
        current_app.logger.error(f"API error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to retrieve statistics'
        }), 500
