from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()

# Example: schedule playlist refresh, transcode jobs, cleanups, etc.
def refresh_active_playlists():
    # logic to update current/next playlist in DB
    pass

def start_jobs():
    scheduler.add_job(refresh_active_playlists, "interval", seconds=60)