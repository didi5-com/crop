"""
Scanner routes for crop image upload and disease detection
"""
import os
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from app import db
from app.models.scan import ScanHistory
from app.utils.file_handler import save_upload_image, get_image_url
from app.services.disease_detector import analyze_crop_image

scanner_bp = Blueprint('scanner', __name__)


@scanner_bp.route('/')
@login_required
def index():
    """Scanner upload page"""
    return render_template('scanner/upload.html')


@scanner_bp.route('/upload', methods=['POST'])
@login_required
def upload():
    """Handle image upload and disease detection"""
    try:
        # Check if file is present
        if 'image' not in request.files:
            flash('No image file provided', 'danger')
            return redirect(url_for('scanner.index'))
        
        file = request.files['image']
        
        if file.filename == '':
            flash('No image selected', 'danger')
            return redirect(url_for('scanner.index'))
        
        # Save uploaded image
        image_path = save_upload_image(file, compress=True)
        
        if not image_path:
            flash('Invalid image file. Please upload a valid image (PNG, JPG, JPEG, GIF)', 'danger')
            return redirect(url_for('scanner.index'))
        
        # Get full path for AI analysis
        full_image_path = os.path.join(
            current_app.config['UPLOAD_FOLDER'],
            os.path.basename(image_path)
        )
        
        # Analyze image using AI
        detection_result = analyze_crop_image(full_image_path)
        
        if not detection_result:
            flash('Failed to analyze image. Please try again.', 'danger')
            return redirect(url_for('scanner.index'))
        
        # Save scan to database
        scan = ScanHistory(
            user_id=current_user.id,
            image_path=image_path,
            crop_name=detection_result.get('crop_name'),
            disease_name=detection_result.get('disease_name'),
            confidence=detection_result.get('confidence'),
            symptoms=detection_result.get('symptoms'),
            causes=detection_result.get('causes'),
            treatment=detection_result.get('treatment'),
            prevention=detection_result.get('prevention'),
            fertilizers=detection_result.get('fertilizers')
        )
        
        db.session.add(scan)
        db.session.commit()
        
        flash('Image analyzed successfully!', 'success')
        return redirect(url_for('scanner.result', scan_id=scan.id))
    
    except Exception as e:
        current_app.logger.error(f"Error in upload: {str(e)}")
        flash('An error occurred while processing your image. Please try again.', 'danger')
        return redirect(url_for('scanner.index'))


@scanner_bp.route('/result/<int:scan_id>')
@login_required
def result(scan_id):
    """Display scan result"""
    scan = ScanHistory.query.get_or_404(scan_id)
    
    # Ensure user can only view their own scans
    if scan.user_id != current_user.id and not current_user.is_admin:
        flash('You do not have permission to view this scan', 'danger')
        return redirect(url_for('dashboard.index'))
    
    return render_template('scanner/result.html', scan=scan)


@scanner_bp.route('/history')
@login_required
def history():
    """View scan history"""
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    scans = ScanHistory.query.filter_by(user_id=current_user.id)\
        .order_by(ScanHistory.timestamp.desc())\
        .paginate(page=page, per_page=per_page, error_out=False)
    
    return render_template('scanner/history.html', scans=scans)


@scanner_bp.route('/delete/<int:scan_id>', methods=['POST'])
@login_required
def delete_scan(scan_id):
    """Delete a scan from history"""
    scan = ScanHistory.query.get_or_404(scan_id)
    
    # Ensure user can only delete their own scans
    if scan.user_id != current_user.id and not current_user.is_admin:
        flash('You do not have permission to delete this scan', 'danger')
        return redirect(url_for('scanner.history'))
    
    try:
        # Delete image file
        from app.utils.file_handler import delete_image
        delete_image(scan.image_path)
        
        # Delete database record
        db.session.delete(scan)
        db.session.commit()
        
        flash('Scan deleted successfully', 'success')
    except Exception as e:
        current_app.logger.error(f"Error deleting scan: {str(e)}")
        flash('An error occurred while deleting the scan', 'danger')
    
    return redirect(url_for('scanner.history'))
