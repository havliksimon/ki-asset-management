from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from sqlalchemy import desc, func
from datetime import date, timedelta

from ..extensions import db
from ..models import Analysis, PerformanceCalculation, Company, StockPrice, analysis_analysts, User, ActivityLog, CsvUpload, Vote, PortfolioPurchase, BenchmarkPrice
from ..utils.performance import PerformanceCalculator
from ..utils.sector_helper import get_company_sector, get_sector_distribution

analyst_bp = Blueprint('analyst', __name__, template_folder='../templates/analyst')

@analyst_bp.before_request
def before_request():
    if not current_user.is_authenticated:
        flash('Please log in to access this page.', 'warning')
        return redirect(url_for('auth.login'))
    if current_user.is_admin:
        # Admins can also view analyst pages, but we may redirect to admin dashboard?
        pass

def generate_ai_insights(performance, comparison_data):
    """Generate AI-powered insights based on performance data."""
    insights = []
    
    if performance.get('avg_return') is None:
        insights.append({
            'type': 'Getting Started',
            'text': 'Complete your first approved analysis to start tracking your performance!'
        })
        return insights
    
    avg_return = performance['avg_return']
    win_rate = performance.get('win_rate', 0)
    team_avg = comparison_data.get('team_avg', 0)
    spy_diff = comparison_data.get('spy_diff', 0)
    
    # Performance vs benchmarks
    if avg_return > team_avg:
        insights.append({
            'type': 'Performance',
            'text': f"Great job! You're outperforming the team average by {avg_return - team_avg:.1f}%. Keep up the good work!"
        })
    elif avg_return < team_avg - 5:
        insights.append({
            'type': 'Improvement Opportunity',
            'text': f"Your returns are below the team average. Consider reviewing your stock selection criteria or position sizing."
        })
    
    # Benchmark comparison
    if spy_diff > 5:
        insights.append({
            'type': 'Alpha Generation',
            'text': f"You're beating the S&P 500 by {spy_diff:.1f}%! You're generating significant alpha."
        })
    elif spy_diff < -10:
        insights.append({
            'type': 'Risk Management',
            'text': f"Consider reviewing your risk management. The S&P 500 is outperforming your picks by {abs(spy_diff):.1f}%."
        })
    
    # Win rate insights
    if win_rate >= 70:
        insights.append({
            'type': 'Consistency',
            'text': f"Excellent win rate of {win_rate:.0f}%! You're consistently picking winning stocks."
        })
    elif win_rate < 40 and performance['num_analyses'] >= 5:
        insights.append({
            'type': 'Win Rate',
            'text': f"Your win rate is {win_rate:.0f}%. Focus on improving your conviction level before making recommendations."
        })
    
    # Portfolio concentration advice
    if performance['num_analyses'] < 3:
        insights.append({
            'type': 'Diversification',
            'text': "You have fewer than 3 approved analyses. Consider building more positions for better diversification."
        })
    
    return insights[:3]  # Limit to top 3 insights


def calculate_stock_impacts(analyst_id):
    """Calculate the impact of each stock on the analyst's portfolio."""
    calculator = PerformanceCalculator()
    
    # Get all approved analyses for this analyst
    analyses = db.session.query(Analysis).join(
        analysis_analysts, Analysis.id == analysis_analysts.c.analysis_id
    ).filter(
        analysis_analysts.c.user_id == analyst_id,
        analysis_analysts.c.role == 'analyst',
        Analysis.status == 'On Watchlist'
    ).all()
    
    if not analyses:
        return []
    
    # Calculate returns and weights
    stock_data = []
    total_return_sum = 0
    
    for analysis in analyses:
        # Skip other events
        if calculator._is_other_event(analysis.company):
            continue
            
        pc = PerformanceCalculation.query.filter_by(
            analysis_id=analysis.id
        ).order_by(PerformanceCalculation.calculation_date.desc()).first()
        
        if pc and pc.return_pct is not None:
            stock_data.append({
                'analysis_id': analysis.id,
                'name': analysis.company.name,
                'ticker': analysis.company.ticker_symbol or 'N/A',
                'return_pct': float(pc.return_pct),
                'analysis_date': analysis.analysis_date
            })
            total_return_sum += float(pc.return_pct)
    
    if not stock_data:
        return []
    
    # Calculate weights and contributions
    n_stocks = len(stock_data)
    equal_weight = 1.0 / n_stocks if n_stocks > 0 else 0
    
    for stock in stock_data:
        stock['weight'] = equal_weight
        # Contribution = weight * return, normalized to show actual impact
        stock['contribution'] = equal_weight * stock['return_pct']
    
    # Sort by absolute contribution (impact)
    stock_data.sort(key=lambda x: abs(x['contribution']), reverse=True)
    
    return stock_data[:10]  # Top 10 by impact


def get_analysis_ids_for_filter(filter_type):
    """
    Get analysis IDs based on filter type.
    
    Filter types:
    - purchased: Only purchased stocks
    - board_approved: Board approved (more yes votes than no)
    - all_approved: All approved by analysts (On Watchlist)
    - approved_neutral: Approved + neutral
    - all: All stocks
    """
    if filter_type == 'purchased':
        purchases = PortfolioPurchase.query.all()
        return [p.analysis_id for p in purchases]
    
    elif filter_type == 'board_approved':
        analyses = []
        for analysis in Analysis.query.filter_by(status='On Watchlist').all():
            votes_yes = Vote.query.filter_by(analysis_id=analysis.id, vote=True).count()
            votes_no = Vote.query.filter_by(analysis_id=analysis.id, vote=False).count()
            if votes_yes > votes_no:
                analyses.append(analysis.id)
        return analyses
    
    elif filter_type == 'all_approved':
        return [a.id for a in Analysis.query.filter_by(status='On Watchlist').all()]
    
    elif filter_type == 'approved_neutral':
        return [a.id for a in Analysis.query.filter(Analysis.status.in_(['On Watchlist', 'Neutral'])).all()]
    
    else:  # all
        return [a.id for a in Analysis.query.filter(Analysis.status.in_(['On Watchlist', 'Neutral', 'Refused'])).all()]


def get_portfolio_performance_for_analyses(analysis_ids):
    """Calculate portfolio performance for a list of analysis IDs."""
    if not analysis_ids:
        return {
            'num_positions': 0,
            'total_return': None,
            'annualized_return': None,
            'start_date': None,
            'benchmark_spy': None,
            'benchmark_ftse': None,
            'benchmark_eems': None
        }
    
    analyses = Analysis.query.filter(Analysis.id.in_(analysis_ids)).all()
    
    total_return = 0.0
    annualized_return = 0.0
    count = 0
    earliest_date = None
    
    for analysis in analyses:
        perf = PerformanceCalculation.query.filter_by(
            analysis_id=analysis.id
        ).order_by(PerformanceCalculation.calculation_date.desc()).first()
        
        if perf:
            ret = float(perf.return_pct)
            total_return += ret
            
            # Calculate annualized return
            days = (date.today() - analysis.analysis_date).days
            if days > 365:
                annualized = ((1 + ret / 100) ** (365 / days) - 1) * 100
            else:
                annualized = ret
            annualized_return += annualized
            
            count += 1
            
            if earliest_date is None or analysis.analysis_date < earliest_date:
                earliest_date = analysis.analysis_date
    
    if count == 0:
        return {
            'num_positions': 0,
            'total_return': None,
            'annualized_return': None,
            'start_date': None,
            'benchmark_spy': None,
            'benchmark_ftse': None,
            'benchmark_eems': None
        }
    
    avg_return = total_return / count
    avg_annualized = annualized_return / count
    
    # Calculate benchmark returns for the same period
    from ..admin.routes import get_cached_benchmark_return
    days = (date.today() - earliest_date).days if earliest_date else 365
    
    return {
        'num_positions': count,
        'total_return': round(avg_return, 2),
        'annualized_return': round(avg_annualized, 2),
        'start_date': earliest_date.isoformat() if earliest_date else None,
        'benchmark_spy': round(get_cached_benchmark_return('SPY', days), 2),
        'benchmark_ftse': round(get_cached_benchmark_return('VT', days), 2),
        'benchmark_eems': round(get_cached_benchmark_return('EEMS', days), 2)
    }


def get_portfolio_series_for_analyses(analysis_ids, years=None):
    """Get portfolio time series data for a list of analysis IDs."""
    import pandas as pd
    
    if not analysis_ids:
        return None
    
    analyses = Analysis.query.filter(Analysis.id.in_(analysis_ids)).all()
    
    if not analyses:
        return None
    
    # Sort by analysis date
    analyses = sorted(analyses, key=lambda x: x.analysis_date)
    earliest_entry = analyses[0].analysis_date
    
    if years:
        end_date = date.today()
        start_date = end_date - timedelta(days=365*years)
        if start_date < earliest_entry:
            start_date = earliest_entry
    else:
        start_date = earliest_entry
        end_date = date.today()
    
    # Create monthly date points
    dates = pd.date_range(start=start_date, end=end_date, freq='MS')
    if len(dates) < 3:
        dates = pd.date_range(start=start_date, end=end_date, periods=6)
    
    portfolio_series = []
    date_labels = []
    
    for d in dates:
        date_str = d.strftime('%Y-%m-%d')
        date_labels.append(date_str)
        current_date = d.date()
        
        # Get all stocks that have entered by this date
        active_analyses = [a for a in analyses if a.analysis_date <= current_date]
        
        if not active_analyses:
            portfolio_series.append(0)
            continue
        
        # Calculate equal-weighted average return
        total_return = 0
        count = 0
        
        for analysis in active_analyses:
            company = Company.query.get(analysis.company_id)
            if not company or not company.ticker_symbol:
                continue
            
            # Get price at analysis date
            entry_price = StockPrice.query.filter(
                StockPrice.company_id == company.id,
                StockPrice.date <= analysis.analysis_date
            ).order_by(StockPrice.date.desc()).first()
            
            # Get price at current chart date
            current_price = StockPrice.query.filter(
                StockPrice.company_id == company.id,
                StockPrice.date <= current_date
            ).order_by(StockPrice.date.desc()).first()
            
            if entry_price and current_price and float(entry_price.close_price) > 0:
                ret = ((float(current_price.close_price) - float(entry_price.close_price)) / 
                       float(entry_price.close_price)) * 100
                total_return += ret
                count += 1
        
        if count > 0:
            portfolio_series.append(round(total_return / count, 2))
        else:
            portfolio_series.append(0)
    
    # Get benchmark series
    from ..admin.routes import _get_benchmark_series_from_cache
    spy_series = _get_benchmark_series_from_cache(dates, 'SPY')
    vt_series = _get_benchmark_series_from_cache(dates, 'VT')
    eems_series = _get_benchmark_series_from_cache(dates, 'EEMS')
    
    return {
        'dates': date_labels,
        'portfolio_series': portfolio_series,
        'spy_series': spy_series,
        'vt_series': vt_series,
        'eems_series': eems_series,
    }


def get_sector_statistics(analysis_ids, use_cached_only=True):
    """Get sector statistics for a list of analyses - uses cached data only to avoid blocking."""
    from ..utils.sector_helper import get_company_sector_async, get_sector_stats_cache_info
    
    sector_returns = {}
    sector_counts = {}
    
    analyses = Analysis.query.filter(Analysis.id.in_(analysis_ids)).all()
    
    for analysis in analyses:
        company = Company.query.get(analysis.company_id)
        if not company:
            continue
        
        # Use async/non-blocking version that returns cached data immediately
        sector = get_company_sector_async(company)
        if not sector:
            sector = 'Unknown'
        
        perf = PerformanceCalculation.query.filter_by(
            analysis_id=analysis.id
        ).order_by(PerformanceCalculation.calculation_date.desc()).first()
        
        if perf:
            ret = float(perf.return_pct)
            
            if sector not in sector_returns:
                sector_returns[sector] = []
                sector_counts[sector] = 0
            
            sector_returns[sector].append(ret)
            sector_counts[sector] += 1
    
    # Calculate statistics per sector
    sector_stats = []
    for sector, returns in sector_returns.items():
        if returns:
            avg_return = sum(returns) / len(returns)
            positive_count = sum(1 for r in returns if r > 0)
            positive_ratio = (positive_count / len(returns)) * 100
            
            # Calculate risk (standard deviation)
            if len(returns) > 1:
                mean = avg_return
                variance = sum((r - mean) ** 2 for r in returns) / len(returns)
                risk = variance ** 0.5
            else:
                risk = 0
            
            sector_stats.append({
                'sector': sector,
                'count': sector_counts[sector],
                'avg_return': round(avg_return, 2),
                'positive_ratio': round(positive_ratio, 2),
                'risk': round(risk, 2),
                'min_return': round(min(returns), 2),
                'max_return': round(max(returns), 2)
            })
    
    # Sort by different metrics
    by_return = sorted(sector_stats, key=lambda x: x['avg_return'], reverse=True)[:5]
    by_risk = sorted(sector_stats, key=lambda x: x['risk'], reverse=True)[:5]
    
    # Get cache info
    cache_info = get_sector_stats_cache_info()
    
    return {
        'all_sectors': sector_stats,
        'top_by_return': by_return,
        'top_by_risk': by_risk,
        'sector_counts': sector_counts,
        'cache_info': cache_info
    }


def get_cached_benchmark_return(ticker, days):
    """
    Calculate benchmark return using cached BenchmarkPrice data.
    Falls back to approximate calculation if no cached data.
    """
    try:
        end_date = date.today()
        start_date = end_date - timedelta(days=days)
        
        start_price = BenchmarkPrice.query.filter(
            BenchmarkPrice.ticker == ticker,
            BenchmarkPrice.date <= start_date
        ).order_by(BenchmarkPrice.date.desc()).first()
        
        end_price = BenchmarkPrice.query.filter(
            BenchmarkPrice.ticker == ticker,
            BenchmarkPrice.date <= end_date
        ).order_by(BenchmarkPrice.date.desc()).first()
        
        if start_price and end_price:
            return ((float(end_price.close_price) - float(start_price.close_price)) / 
                    float(start_price.close_price)) * 100
    except Exception as e:
        pass
    
    # Fallback to approximate calculation
    annual_returns = {'SPY': 10.0, 'VT': 9.0, 'EEMS': 7.0}
    annual = annual_returns.get(ticker, 8.0)
    years = days / 365.0
    return ((1 + annual/100) ** years - 1) * 100


def _get_benchmark_series_from_cache(dates, ticker):
    """
    Get benchmark return series from cached BenchmarkPrice data.
    Falls back to synthetic data if cache is empty.
    """
    series = []
    
    if not dates:
        return series
    
    first_date = dates[0].date() if hasattr(dates[0], 'date') else dates[0]
    base_price = BenchmarkPrice.query.filter(
        BenchmarkPrice.ticker == ticker,
        BenchmarkPrice.date <= first_date
    ).order_by(BenchmarkPrice.date.desc()).first()
    
    if base_price is None:
        bp = BenchmarkPrice.query.filter(
            BenchmarkPrice.ticker == ticker,
            BenchmarkPrice.date >= first_date
        ).order_by(BenchmarkPrice.date.asc()).first()
        if bp:
            base_price = float(bp.close_price)
    
    if base_price is None:
        approx_prices = {'SPY': 400.0, 'VT': 100.0, 'EEMS': 50.0}
        base_price = approx_prices.get(ticker, 100.0)
    
    for i, d in enumerate(dates):
        current_date = d.date() if hasattr(d, 'date') else d
        price = BenchmarkPrice.query.filter(
            BenchmarkPrice.ticker == ticker,
            BenchmarkPrice.date <= current_date
        ).order_by(BenchmarkPrice.date.desc()).first()
        
        if price:
            ret = ((float(price.close_price) - base_price) / base_price) * 100
            series.append(round(ret, 2))
        else:
            if i == 0:
                series.append(0.0)
            else:
                annual = {'SPY': 10.0, 'VT': 9.0, 'EEMS': 7.0}.get(ticker, 8.0)
                days_diff = (dates[i] - dates[i-1]).days if i > 0 else 30
                trend = (annual / 365.0) * days_diff
                series.append(round(series[-1] + trend, 2))
    
    return series


def get_analyst_rankings():
    """Get various analyst rankings."""
    calculator = PerformanceCalculator()
    
    # Get all analysts performance
    all_perfs = calculator.get_all_analysts_performance()
    
    # 1. Top 5 by board approved analyses
    board_approved_counts = []
    for user in User.query.all():
        count = db.session.query(Analysis).join(
            analysis_analysts, Analysis.id == analysis_analysts.c.analysis_id
        ).filter(
            analysis_analysts.c.user_id == user.id,
            analysis_analysts.c.role == 'analyst',
            Analysis.status == 'On Watchlist'
        ).count()
        board_approved_counts.append({
            'analyst_id': user.id,
            'analyst_name': user.full_name or user.email.split('@')[0],
            'count': count
        })
    top_board_approved = sorted(board_approved_counts, key=lambda x: x['count'], reverse=True)[:5]
    
    # 2. Top 5 by total analyses (approved + neutral + refused)
    total_counts = []
    for user in User.query.all():
        count = db.session.query(Analysis).join(
            analysis_analysts, Analysis.id == analysis_analysts.c.analysis_id
        ).filter(
            analysis_analysts.c.user_id == user.id,
            analysis_analysts.c.role == 'analyst',
            Analysis.status.in_(['On Watchlist', 'Neutral', 'Refused'])
        ).count()
        total_counts.append({
            'analyst_id': user.id,
            'analyst_name': user.full_name or user.email.split('@')[0],
            'count': count
        })
    top_total = sorted(total_counts, key=lambda x: x['count'], reverse=True)[:5]
    
    # 3. Top 5 by win rate (min 3 analyses)
    win_rates = []
    for perf in all_perfs:
        if perf['num_analyses'] >= 3 and perf['win_rate'] is not None:
            win_rates.append({
                'analyst_id': perf['analyst_id'],
                'analyst_name': perf['analyst_name'],
                'win_rate': perf['win_rate'],
                'num_analyses': perf['num_analyses']
            })
    top_win_rate = sorted(win_rates, key=lambda x: x['win_rate'], reverse=True)[:5]
    
    # 4. Top 5 by performance
    top_performance = sorted(
        [p for p in all_perfs if p['avg_return'] is not None],
        key=lambda x: x['avg_return'],
        reverse=True
    )[:5]
    
    return {
        'top_board_approved': top_board_approved,
        'top_total': top_total,
        'top_win_rate': top_win_rate,
        'top_performance': top_performance
    }


@analyst_bp.route('/')
@login_required
def dashboard():
    """Analyst dashboard with personal statistics."""
    # If admin, include admin dashboard data
    if current_user.is_admin:
        from ..models import User, ActivityLog, CsvUpload, Company
        
        # Gather admin stats
        total_users = User.query.count()
        active_users = User.query.filter_by(is_active=True).count()
        admin_users = User.query.filter_by(is_admin=True).count()
        
        total_analyses = Analysis.query.count()
        approved_analyses_count = Analysis.query.filter_by(status='On Watchlist').count()
        
        total_companies = Company.query.count()
        csv_uploads = CsvUpload.query.count()
        
        # Recent activity
        recent_activity = ActivityLog.query.order_by(ActivityLog.timestamp.desc()).limit(10).all()
        
        admin_stats = {
            'total_users': total_users,
            'active_users': active_users,
            'admin_users': admin_users,
            'total_analyses': total_analyses,
            'approved_analyses': approved_analyses_count,
            'total_companies': total_companies,
            'csv_uploads': csv_uploads
        }
    else:
        admin_stats = None
        recent_activity = None
    
    calculator = PerformanceCalculator()
    
    # Count analyses where user is analyst (role 'analyst')
    my_analyses = db.session.query(Analysis).join(
        analysis_analysts, Analysis.id == analysis_analysts.c.analysis_id
    ).filter(
        analysis_analysts.c.user_id == current_user.id,
        analysis_analysts.c.role == 'analyst'
    ).all()
    
    approved = [a for a in my_analyses if a.status == 'On Watchlist']
    
    # Calculate performance
    perf = calculator.get_analyst_performance(current_user.id)
    
    # Get all analysts performance for comparison
    all_perfs = calculator.get_all_analysts_performance()
    
    # Calculate team average and find best analyst
    returns = [p['avg_return'] for p in all_perfs if p['avg_return'] is not None]
    team_avg_return = sum(returns) / len(returns) if returns else 0
    best_analyst_return = max(returns) if returns else 0
    
    # Find user's rank
    analyst_rank = 1
    total_analysts = len(all_perfs)
    for i, p in enumerate(all_perfs, 1):
        if p['analyst_id'] == current_user.id:
            analyst_rank = i
            break
    
    # Get benchmark comparisons
    spy_return = 15.0  # S&P 500 approximate
    vt_return = 12.0   # FTSE All-World approximate
    
    user_return = perf.get('avg_return') or 0
    benchmark_comparison = {
        'spy_diff': user_return - spy_return,
        'vt_diff': user_return - vt_return
    }
    
    comparison_data = {
        'team_avg': team_avg_return,
        'spy_diff': benchmark_comparison['spy_diff'],
        'vt_diff': benchmark_comparison['vt_diff']
    }
    
    # Generate AI insights
    ai_insights = generate_ai_insights(perf, comparison_data)
    
    # Calculate stock impacts
    stock_impacts = calculate_stock_impacts(current_user.id)
    
    # Recent analyses
    recent = db.session.query(Analysis).join(
        analysis_analysts, Analysis.id == analysis_analysts.c.analysis_id
    ).filter(
        analysis_analysts.c.user_id == current_user.id
    ).order_by(desc(Analysis.analysis_date)).limit(10).all()
    
    return render_template('analyst/dashboard.html',
                           total_analyses=len(my_analyses),
                           approved_analyses=len(approved),
                           performance=perf,
                           recent_analyses=recent,
                           team_avg_return=team_avg_return,
                           best_analyst_return=best_analyst_return,
                           analyst_rank=analyst_rank,
                           total_analysts=total_analysts,
                           benchmark_comparison=benchmark_comparison,
                           ai_insights=ai_insights,
                           stock_impacts=stock_impacts,
                           admin_stats=admin_stats,
                           recent_activity=recent_activity)


@analyst_bp.route('/performance')
@login_required
def performance():
    """Detailed performance view for the logged‑in analyst."""
    annualized = request.args.get('annualized', 'false').lower() == 'true'
    calculator = PerformanceCalculator()
    perf = calculator.get_analyst_performance(current_user.id, annualized=annualized)
    
    # Get list of analyses with performance calculations
    analyses = db.session.query(Analysis).join(
        analysis_analysts, Analysis.id == analysis_analysts.c.analysis_id
    ).filter(
        analysis_analysts.c.user_id == current_user.id,
        analysis_analysts.c.role == 'analyst',
        Analysis.status == 'On Watchlist'
    ).all()
    
    # Attach latest performance calculation for each analysis
    analysis_data = []
    for a in analyses:
        pc = PerformanceCalculation.query.filter_by(
            analysis_id=a.id
        ).order_by(PerformanceCalculation.calculation_date.desc()).first()
        annualized_return = None
        if pc and annualized:
            annualized_return = calculator._annualize_return(
                float(pc.return_pct), a.analysis_date, pc.calculation_date
            )
        analysis_data.append({
            'analysis': a,
            'performance': pc,
            'company': a.company,
            'annualized_return': annualized_return
        })
    
    return render_template('analyst/performance.html',
                           performance=perf,
                           analysis_data=analysis_data,
                           annualized=annualized)


@analyst_bp.route('/overview')
@login_required
def overview():
    """
    Overview page with portfolio charts, sector statistics, and analyst rankings.
    Uses 7-day caching for fast filter switching.
    """
    from ..utils.overview_cache import (
        get_cached_overview_data, save_overview_cache, 
        get_cache_status, should_use_cache
    )
    
    # Get filter from request
    current_filter = request.args.get('filter', 'board_approved')
    force_refresh = request.args.get('refresh') == 'true' and current_user.is_admin
    
    # Check if we have valid cached data
    cache_data = None
    if not force_refresh:
        cache_data = get_cached_overview_data(current_filter)
    
    if cache_data:
        # Use cached data
        portfolio_performance = cache_data['portfolio_performance']
        series_all = cache_data['series_all']
        series_1y = cache_data['series_1y']
        sector_stats = cache_data['sector_stats']
        analyst_rankings = cache_data['analyst_rankings']
        positive_ratio = cache_data['positive_ratio']
        total_with_perf = cache_data['total_positions']
        from_cache = True
    else:
        # Calculate fresh data
        # Get analysis IDs based on filter
        analysis_ids = get_analysis_ids_for_filter(current_filter)
        
        # Get portfolio performance
        portfolio_performance = get_portfolio_performance_for_analyses(analysis_ids)
        
        # Get portfolio series data
        series_all = get_portfolio_series_for_analyses(analysis_ids, years=None)
        series_1y = get_portfolio_series_for_analyses(analysis_ids, years=1)
        
        # Get sector statistics
        sector_stats = get_sector_statistics(analysis_ids)
        
        # Get analyst rankings
        analyst_rankings = get_analyst_rankings()
        
        # Calculate positive return ratio
        analyses = Analysis.query.filter(Analysis.id.in_(analysis_ids)).all()
        positive_count = 0
        total_with_perf = 0
        
        for analysis in analyses:
            perf = PerformanceCalculation.query.filter_by(
                analysis_id=analysis.id
            ).order_by(PerformanceCalculation.calculation_date.desc()).first()
            
            if perf:
                total_with_perf += 1
                if float(perf.return_pct) > 0:
                    positive_count += 1
        
        positive_ratio = (positive_count / total_with_perf * 100) if total_with_perf > 0 else 0
        
        # Save to cache
        cache_data = {
            'portfolio_performance': portfolio_performance,
            'series_all': series_all,
            'series_1y': series_1y,
            'sector_stats': sector_stats,
            'analyst_rankings': analyst_rankings,
            'positive_ratio': round(positive_ratio, 2),
            'total_positions': total_with_perf
        }
        save_overview_cache(current_filter, cache_data)
        from_cache = False
    
    # Get cache status for admin
    cache_status = get_cache_status() if current_user.is_admin else None
    
    return render_template('analyst/overview.html',
                           current_filter=current_filter,
                           portfolio_performance=portfolio_performance,
                           series_all=series_all,
                           series_1y=series_1y,
                           sector_stats=sector_stats,
                           analyst_rankings=analyst_rankings,
                           positive_ratio=positive_ratio,
                           total_positions=total_with_perf,
                           from_cache=from_cache,
                           cache_status=cache_status)


@analyst_bp.route('/analyses')
@login_required
def analyses():
    """List all analyses where the user is involved (as analyst or opponent)."""
    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    analyses_query = db.session.query(Analysis).join(
        analysis_analysts, Analysis.id == analysis_analysts.c.analysis_id
    ).filter(
        analysis_analysts.c.user_id == current_user.id
    ).order_by(desc(Analysis.analysis_date))
    
    pagination = analyses_query.paginate(page=page, per_page=per_page)
    
    return render_template('analyst/analyses.html', pagination=pagination)
