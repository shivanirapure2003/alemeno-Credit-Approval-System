from datetime import datetime
from .models import Customer, Loan


def calculate_credit_score(customer):
    """Calculate a simple credit score (0-100) for a customer.

    Criteria (weighted):
    - 40% on-time payment ratio
    - 20% recent loan activity (more recent loans slightly reduces score)
    - 40% total loan amount relative to approved limit

    Returns int score between 0 and 100. If current approved debt exceeds
    customer's approved_limit, return 0.
    """
    loans = Loan.objects.filter(customer=customer)
    total_loans = loans.count()
    if total_loans == 0:
        return 100  # No past loans, assume perfect score

    # on-time payments ratio (default True if attribute missing)
    on_time_ratio = sum(1 for l in loans if getattr(l, 'emis_paid_on_time', True)) / total_loans

    # number of loans in current year (use current UTC year)
    current_year = datetime.utcnow().year
    current_year_loans = sum(1 for l in loans if getattr(l, 'created_at', None) and l.created_at.year == current_year)

    # total loan amount and current approved debt
    try:
        total_loan_amount = sum(float(l.amount) for l in loans)
    except Exception:
        total_loan_amount = 0.0

    try:
        current_debt = sum(float(l.amount) for l in loans if l.status == 'APPROVED')
    except Exception:
        current_debt = 0.0

    # approved_limit fallback to 1.0 to avoid division by zero
    try:
        approved_limit = float(getattr(customer, 'approved_limit', 1.0)) or 1.0
    except Exception:
        approved_limit = 1.0

    if current_debt > approved_limit:
        return 0

    recent_penalty = max(0.0, min(1.0, current_year_loans / 10.0))  # scale to [0,1]

    score = int(
        40 * on_time_ratio
        + 20 * (1 - recent_penalty)
        + 40 * max(0.0, 1 - (total_loan_amount / approved_limit))
    )

    return max(0, min(score, 100))


def get_corrected_interest(score, interest_rate):
    """Return (approval: bool, corrected_interest_rate: float).

    Simple policy used by views:
    - score >= 80: approve, reduce rate by 1.0 percentage point (but not below 0)
    - 50 <= score < 80: approve, keep rate
    - score < 50: do not approve, increase rate by 2.0 percentage points
    """
    try:
        base = float(interest_rate)
    except Exception:
        base = 0.0

    if score >= 80:
        corrected = max(0.0, base - 1.0)
        approval = True
    elif score >= 50:
        corrected = base
        approval = True
    else:
        corrected = base + 2.0
        approval = False

    return approval, corrected


def calculate_emi(principal, tenure_months, annual_interest_rate):
    """Calculate monthly EMI rounded to 2 decimal places.

    principal: numeric
    tenure_months: integer months
    annual_interest_rate: percentage (e.g. 12 for 12%)
    """
    try:
        P = float(principal)
    except Exception:
        P = 0.0
    try:
        n = int(tenure_months)
    except Exception:
        n = 1

    r = float(annual_interest_rate) / 100.0 / 12.0  # monthly rate

    if n <= 0:
        return 0.0

    if r == 0:
        emi = P / n
    else:
        emi = P * r * (1 + r) ** n / ((1 + r) ** n - 1)

    return round(emi, 2)
