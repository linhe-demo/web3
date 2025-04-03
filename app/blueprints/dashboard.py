from flask import Blueprint, render_template, request, jsonify
from flask_jwt_extended import jwt_required

from app.models.task import Task

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/list', methods=['GET'])
def list():
    return render_template('dashboard/index.html')


@dashboard_bp.route('/data', methods=['POST'])
@jwt_required()  # 添加JWT校验装饰器
def data():
    backInfo = []
    for task in Task.query.all():
        backInfo.append({
            "id": task.id,
            "name": task.name,
            "status": task.status,
            "created_at": task.create_at.strftime("%Y-%m-%d %H:%M:%S"),
        })

    return jsonify({
        "code": 200,
        "message": "success",
        "data": {
            "list": backInfo,
            "total": Task.query.count(),
        }
    })


def redirect():
    return render_template('dashboard/redirect.html')
