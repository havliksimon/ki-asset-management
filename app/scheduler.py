"""
Background scheduler for KI Asset Management.

Runs weekly data refresh on Friday nights (11 PM).
Refreshes all cached data for optimal website performance.
"""

import logging
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

logger = logging.getLogger(__name__)

scheduler = BackgroundScheduler()


def refresh_all_cached_data():
    """
    Refresh all cached data.
    Called automatically every Friday at 11 PM.
    Also warms Neon-optimized caches for public pages.
    """
    logger.info("=" * 60)
    logger.info("Starting weekly data refresh...")
    logger.info("=" * 60)
    
    start_time = datetime.now()
    
    try:
        # Import here to avoid circular imports
        from .utils.overview_cache import invalidate_cache
        from .utils.presentation_export import get_growth_timeline, get_sector_analysis
        from .utils.export_helper import generate_comprehensive_export
        from .utils.neon_cache import warm_public_caches, invalidate_all_public_cache
        
        # 1. Invalidate all caches first
        logger.info("Invalidating all caches...")
        invalidate_cache()
        invalidate_all_public_cache()
        
        # 2. Warm Neon-optimized public caches (NEW)
        logger.info("Warming Neon-optimized public caches...")
        warmed = warm_public_caches()
        logger.info(f"Warmed caches: {', '.join(warmed)}")
        
        # 3. Refresh growth timeline
        logger.info("Refreshing growth timeline...")
        growth_data = get_growth_timeline(use_cache=False)
        logger.info(f"Growth timeline refreshed: {growth_data.get('summary', {})}")
        
        # 4. Refresh sector analysis
        logger.info("Refreshing sector analysis...")
        sector_data = get_sector_analysis(use_cache=False)
        best_count = len(sector_data.get('best_sectors', {}).get('rows', []))
        logger.info(f"Sector analysis refreshed: {best_count} best sectors")
        
        # 5. Refresh comprehensive export
        logger.info("Refreshing comprehensive export...")
        export_data, _, _ = generate_comprehensive_export(force_new=True)
        logger.info(f"Comprehensive export refreshed: {len(export_data) // 1024} KB")
        
        elapsed = (datetime.now() - start_time).total_seconds()
        logger.info("=" * 60)
        logger.info(f"Weekly refresh completed in {elapsed:.1f}s")
        logger.info("=" * 60)
        
    except Exception as e:
        logger.error(f"Error during weekly refresh: {e}")
        logger.exception("Weekly refresh failed")


def init_scheduler(app):
    """Initialize and start the background scheduler."""
    with app.app_context():
        # Schedule weekly refresh for Friday at 11:00 PM
        scheduler.add_job(
            func=refresh_all_cached_data,
            trigger=CronTrigger(day_of_week='fri', hour=23, minute=0),
            id='weekly_data_refresh',
            name='Weekly Data Refresh',
            replace_existing=True
        )
        
        # Also run on startup if it's been more than 7 days since last refresh
        try:
            import os
            cache_dir = os.path.join(app.instance_path, 'overview_cache')
            last_refresh_file = os.path.join(cache_dir, 'last_refresh.txt')
            
            needs_refresh = True
            if os.path.exists(last_refresh_file):
                with open(last_refresh_file, 'r') as f:
                    last_refresh = datetime.fromisoformat(f.read().strip())
                    if datetime.now() - last_refresh < timedelta(days=7):
                        needs_refresh = False
                        logger.info(f"Last refresh was {(datetime.now() - last_refresh).days} days ago, skipping startup refresh")
            
            if needs_refresh:
                logger.info("Triggering initial data refresh on startup...")
                refresh_all_cached_data()
                
            # Save refresh timestamp
            os.makedirs(cache_dir, exist_ok=True)
            with open(last_refresh_file, 'w') as f:
                f.write(datetime.now().isoformat())
                
        except Exception as e:
            logger.warning(f"Error checking last refresh time: {e}")
        
        scheduler.start()
        logger.info("Background scheduler started - weekly refresh scheduled for Friday 11 PM")


def shutdown_scheduler():
    """Shutdown the scheduler gracefully."""
    if scheduler.running:
        scheduler.shutdown()
        logger.info("Background scheduler shut down")
