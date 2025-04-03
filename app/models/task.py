from datetime import datetime
from app.extensions import db


class Task(db.Model):
    """
    任务表模型
    对应MySQL表：tasks
    """
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='记录id')
    name = db.Column(db.String(255), nullable=False, default='', comment='任务名称')
    status = db.Column(db.SmallInteger, nullable=False, default=0,
                      comment='状态：0 未开始 1 已暂停 2：结束 3：弃用')
    create_at = db.Column(db.DateTime, nullable=False, default=datetime.now,
                         comment='创建时间')
    update_at = db.Column(db.DateTime, nullable=False,
                         default=datetime.now, onupdate=datetime.now,
                         comment='更新时间')

    def __repr__(self):
        return f'<Task id={self.id} name={self.name} status={self.status}>'

    # 状态常量（可选）
    STATUS_NOT_STARTED = 0
    STATUS_PAUSED = 1
    STATUS_FINISHED = 2
    STATUS_DEPRECATED = 3