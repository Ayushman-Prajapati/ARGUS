from django import template

register = template.Library()


@register.filter
def filter_by_source(projects, source_tuple):
    """Filter projects by source type and reference."""
    source_type, source_reference = source_tuple
    return [p for p in projects if p.source_type == source_type and p.source_reference == source_reference]


@register.filter
def security_grade(risk_score):
    """Convert risk score (0-100) to security grade (A-F)."""
    if risk_score >= 90:
        return 'F'
    elif risk_score >= 70:
        return 'E'
    elif risk_score >= 50:
        return 'D'
    elif risk_score >= 30:
        return 'C'
    elif risk_score >= 15:
        return 'B'
    else:
        return 'A'


@register.filter
def security_grade_color(risk_score):
    """Return the color class for a security grade."""
    grade = security_grade(risk_score)
    return {
        'A': 'grade-a',
        'B': 'grade-b',
        'C': 'grade-c',
        'D': 'grade-d',
        'E': 'grade-e',
        'F': 'grade-f',
    }.get(grade, 'grade-a')


@register.filter
def security_grade_label(risk_score):
    """Return the label/description for a security grade."""
    grade = security_grade(risk_score)
    return {
        'A': 'Excellent',
        'B': 'Good',
        'C': 'Fair',
        'D': 'Poor',
        'E': 'Critical',
        'F': 'Failing',
    }.get(grade, 'Excellent')


@register.filter
def format_duration(seconds):
    """Format duration in seconds to human readable string."""
    if seconds is None:
        return '—'
    if seconds < 60:
        return f'{seconds:.1f}s'
    minutes = int(seconds // 60)
    remaining_seconds = seconds % 60
    if remaining_seconds == 0:
        return f'{minutes}m'
    return f'{minutes}m {remaining_seconds:.0f}s'


@register.filter
def abs_value(value):
    """Return absolute value of a number."""
    try:
        return abs(value)
    except (TypeError, ValueError):
        return value